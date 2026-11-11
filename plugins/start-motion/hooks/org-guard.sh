#!/usr/bin/env bash
# Org guard for the Kicksaw Project Start Motion plugin.
#
# Runs before every shell command Claude or one of the plugin's agents is about to run. It reads the tool call
# as JSON on stdin and looks only at Salesforce CLI commands (sf, sfdx).
#
#   deny  commands that change, load, export or delete client records; anonymous Apex; direct API calls;
#         deleting metadata from an org (except the undo of a rejected task, below); deleting an org;
#         uninstalling a package; any saving deploy or removal aimed at an org that is not a sandbox
#   ask   the person sees the command and confirms it themselves:
#           a query that returns client records
#           a deploy that saves to a sandbox (deploy without --dry-run, quick deploy, package install)
#           the undo of a rejected task: a removal whose list is at .start-motion/undo/<task ID>/ and holds
#           only what that task's branch created (checked by skills/build/scripts/undo-task.sh), in a sandbox
#   pass  everything else: retrieve, validate, dry runs, test runs, org display and list, and queries about
#         configuration (--use-tooling-api)
#
# Needs bash, awk, grep and sed, plus git and the Salesforce CLI for the two checks that use them.

input="$(cat)"
here="$(cd "$(dirname "$0")" && pwd)"

decide() {  # decide <deny|ask> <reason>
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
  exit 0
}

# One command per line: split on &&, ||, ;, | and the escaped newlines inside the JSON. awk, because the sed
# on a Mac does not take a newline in a replacement.
# The JSON head up to the command's opening quote is dropped first, so every line starts where a command starts.
segments="$(printf '%s' "$input" | awk '{sub(/^[{].*"command"[[:space:]]*:[[:space:]]*"/,""); gsub(/\\n/,"\n"); gsub(/&&|\|\||;|\|/,"\n"); print}')"

# Not a Salesforce CLI command: nothing to say.
printf '%s\n' "$segments" | grep -qE '(^|[^[:alnum:]_-])(sf|sfdx)[[:space:]]' || exit 0

# sf or sfdx where a command starts: at the start of a line, after env assignments, after npx, exec, sudo, time,
# command or xargs, by a path, or inside $( ), ( ), backticks or bash -c / sh -c. A message or path that only
# mentions sf (a commit message, ls sf-project) is not a command.
PRE='([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+)*((npx|exec|sudo|time|command|xargs)[[:space:]]+)*([^[:space:]"]*/)?'
SF="(^[[:space:]]*|[\$]?[(][[:space:]]*|\`[[:space:]]*|(ba|z)?sh[[:space:]]+-c[[:space:]]+[\\]?[\"'][[:space:]]*)${PRE}(sf|sfdx)[[:space:]]+"
has() { printf '%s\n' "$segments" | grep -qiE -- "$1"; }
deny_if() { has "$1" && decide deny "$2"; }

# The org a command names, and what kind of org it is: sandbox, production or unknown.
org_alias() {
  printf '%s\n' "$1" | sed -nE 's/.*(--target-org|--targetusername|[[:space:]]-o|[[:space:]]-u)[[:space:]=]+([^[:space:]"\\]+).*/\2/p' | head -1
}
org_kind() {  # org_kind <alias>
  [ -n "$1" ] || { echo unknown; return; }
  command -v sf >/dev/null 2>&1 || { echo unknown; return; }
  url="$(sf org display --target-org "$1" --json 2>/dev/null | grep -oE '"instanceUrl"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1)"
  [ -n "$url" ] || { echo unknown; return; }
  if printf '%s' "$url" | grep -qiE '\.sandbox\.|\.scratch\.|-dev-ed\.|\.develop\.'; then echo sandbox; else echo production; fi
}

# ---------------------------------------------------------------- records
data_lines="$(printf '%s\n' "$segments" | grep -iE "${SF}(data[[:space:]]|force:data)")"
if [ -n "$data_lines" ]; then
  writes="$(printf '%s\n' "$data_lines" | grep -ivE "(data[[:space:]]+(query|get[[:space:]]+record)|force:data:soql:query|force:data:record:get)")"
  [ -n "$writes" ] && decide deny "Start Motion org guard: this command changes, loads, exports or deletes client records. The kit works on configuration only. If records need loading, cleaning or deleting, a person does that outside the kit."
  records="$(printf '%s\n' "$data_lines" | grep -ivE -- "(--use-tooling-api|[[:space:]]-t([[:space:]]|$))")"
  [ -n "$records" ] && decide ask "Start Motion org guard: this query returns client records into the conversation. Confirm only if you asked for it and the fields it reads are ones you are comfortable sharing here. Queries about configuration (--use-tooling-api) pass without this question."
fi
deny_if "${SF}api[[:space:]]+request" \
  "Start Motion org guard: direct API requests to an org are blocked, because they can read or delete records and metadata."
deny_if "${SF}force:apex:execute" \
  "Start Motion org guard: anonymous Apex is blocked, because it can change or delete records."
if printf '%s\n' "$segments" | grep -iE "${SF}apex[[:space:]]+run" | grep -qivE "apex[[:space:]]+run[[:space:]]+test"; then
  decide deny "Start Motion org guard: anonymous Apex is blocked, because it can change or delete records. Running tests (sf apex run test) is allowed."
fi

# ---------------------------------------------------------------- removing metadata
deny_if "(--purge-on-delete)" \
  "Start Motion org guard: purging deleted metadata is blocked. Removed fields stay recoverable in Setup for 15 days."
deny_if "${SF}(project[[:space:]]+delete[[:space:]]+source|force:source:delete)" \
  "Start Motion org guard: deleting metadata from an org is blocked. A rejected task is undone with /start-motion:build (undo); anything else is removed by a person."
deny_if "${SF}(org[[:space:]]+delete|force:org:delete)" "Start Motion org guard: deleting an org is blocked."
deny_if "${SF}(package[[:space:]]+uninstall|force:package:uninstall)" "Start Motion org guard: uninstalling a package is blocked."

destructive="$(printf '%s\n' "$segments" | grep -iE -- "--(pre-|post-)?destructive-changes")"
if [ -n "$destructive" ]; then
  NO="Start Motion org guard: deleting metadata from an org is blocked."
  [ "$(printf '%s\n' "$destructive" | grep -c .)" = "1" ] || decide deny "$NO One removal per command."
  file="$(printf '%s\n' "$destructive" | sed -nE 's/.*--(pre-|post-)?destructive-changes[[:space:]=]+([^[:space:]"\\]+).*/\2/p')"
  printf '%s' "$file" | grep -qE '(^|/)\.start-motion/undo/[A-Za-z0-9._-]+/destructiveChanges\.xml$' \
    || decide deny "$NO The only removal the kit runs is the undo of a rejected task, from the list /start-motion:build prepares at .start-motion/undo/<task ID>/."
  cwd="$(printf '%s' "$input" | grep -oE '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:[[:space:]]*"(.*)"/\1/')"
  [ -n "$cwd" ] && cd "$cwd" 2>/dev/null
  why="$(bash "$here/../skills/build/scripts/undo-task.sh" verify "$file" 2>&1)" \
    || decide deny "$NO The undo list did not pass its check: $(printf '%s' "$why" | tr '\n"\\' '   ' | cut -c1-300)"
  alias="$(org_alias "$destructive")"
  [ "$(org_kind "$alias")" = "sandbox" ] \
    || decide deny "$NO The target org (${alias:-none named}) could not be confirmed as a sandbox. An undo runs only against a sandbox named with --target-org."
  decide ask "Start Motion org guard: this removes from the sandbox $alias only what the rejected task created (the list is in $(dirname "$file")/undo-list.txt). Nothing that was there before the task is touched. Removed fields stay recoverable in Setup for 15 days. Confirm to remove."
fi

# ---------------------------------------------------------------- deploys that save
saving=""
s="$(printf '%s\n' "$segments" | grep -iE "${SF}project[[:space:]]+deploy[[:space:]]+start" | grep -ivE -- "--dry-run")"; [ -n "$s" ] && saving="$s"
s="$(printf '%s\n' "$segments" | grep -iE "${SF}project[[:space:]]+deploy[[:space:]]+(quick|resume)")"; [ -n "$s" ] && saving="$s"
s="$(printf '%s\n' "$segments" | grep -iE "${SF}(force:source:deploy|force:mdapi:deploy)" | grep -ivE -- "(--checkonly|[[:space:]]-c([[:space:]]|[\\\"']|$))")"; [ -n "$s" ] && saving="$s"
s="$(printf '%s\n' "$segments" | grep -iE "${SF}(force:source:push|package[[:space:]]+install|force:package:install)")"; [ -n "$s" ] && saving="$s"
if [ -n "$saving" ]; then
  alias="$(org_alias "$(printf '%s\n' "$saving" | head -1)")"
  case "$(org_kind "$alias")" in
    production) decide deny "Start Motion org guard: ${alias} is not a sandbox. The kit never saves changes to a production org. A person runs production deployments, outside the kit." ;;
    sandbox)    decide ask "Start Motion org guard: this saves changes to the sandbox ${alias}. Confirm it is the deploy you asked for." ;;
    *)          decide ask "Start Motion org guard: this saves changes to a Salesforce org (${alias:-no org named}), and the guard could not confirm it is a sandbox. Check the org before you confirm. The kit never deploys to production." ;;
  esac
fi

exit 0
