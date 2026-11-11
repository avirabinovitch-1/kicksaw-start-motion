#!/usr/bin/env bash
# Org guard for the Kicksaw Project Start Motion plugin.
#
# Runs before every shell command Claude or one of the plugin's agents is about to run. It reads the tool call
# as JSON on stdin and looks only at Salesforce CLI commands (sf, sfdx).
#
#   deny  commands that read or change client records, delete metadata from an org, delete an org,
#         uninstall a package, run anonymous Apex, or call the org's API directly
#   ask   commands that save a change to an org (a deploy without --dry-run, a quick deploy, a package install):
#         the person sees the command and must confirm it themselves
#   pass  everything else (retrieve, validate, dry-run deploys, running tests, org display and list)
#
# It needs nothing but bash, sed and grep. It does not know whether an org is a sandbox or production; that check
# is in the agents and the stage commands. This is the backstop for when they get it wrong.

input="$(cat)"


decide() {  # decide <deny|ask> <reason>
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
  exit 0
}

# One command per line: split on &&, ||, ;, | and the escaped newlines inside the JSON. awk, because the sed
# on a Mac does not take a newline in a replacement.
segments="$(printf '%s' "$input" | awk '{gsub(/\\n/,"\n"); gsub(/&&|\|\||;|\|/,"\n"); print}')"

# Not a Salesforce CLI command: nothing to say.
printf '%s\n' "$segments" | grep -qE '(^|[^[:alnum:]_-])(sf|sfdx)[[:space:]]' || exit 0

SF='(^|[^[:alnum:]_-])(sf|sfdx)[[:space:]]+'

deny_if() {  # deny_if <regex> <reason>
  printf '%s\n' "$segments" | grep -qiE "$1" && decide deny "$2"
}

deny_if "${SF}(data[[:space:]]|force:data)" \
  "Start Motion org guard: sf data commands read or change client records. The kit works on configuration only. If records need loading, cleaning or deleting, a person does that outside the kit."
deny_if "${SF}api[[:space:]]+request" \
  "Start Motion org guard: direct API requests to an org are blocked, because they can read or delete records and metadata."
deny_if "${SF}force:apex:execute" \
  "Start Motion org guard: anonymous Apex is blocked, because it can change or delete records."
if printf '%s\n' "$segments" | grep -iE "${SF}apex[[:space:]]+run" | grep -qivE "apex[[:space:]]+run[[:space:]]+test"; then
  decide deny "Start Motion org guard: anonymous Apex is blocked, because it can change or delete records. Running tests (sf apex run test) is allowed."
fi
deny_if "(--pre-destructive-changes|--post-destructive-changes|--destructive-changes|--purge-on-delete)" \
  "Start Motion org guard: deleting metadata from an org is blocked. The builder may prepare the destructive change in the branch; a person applies it by hand after reading what it removes."
deny_if "${SF}(project[[:space:]]+delete[[:space:]]+source|force:source:delete)" \
  "Start Motion org guard: deleting metadata from an org is blocked. A person applies a deletion by hand after reading what it removes."
deny_if "${SF}(org[[:space:]]+delete|force:org:delete)" \
  "Start Motion org guard: deleting an org is blocked."
deny_if "${SF}(package[[:space:]]+uninstall|force:package:uninstall)" \
  "Start Motion org guard: uninstalling a package is blocked."

SAVE_REASON="Start Motion org guard: this command saves changes to a Salesforce org. Check the target org is a sandbox and that this is the deploy you asked for. Production deployments are never run by the kit; a person runs them."

# A deploy that saves: deploy start without --dry-run, quick, resume, and the older sfdx forms without a check-only flag.
if printf '%s\n' "$segments" | grep -iE "${SF}project[[:space:]]+deploy[[:space:]]+start" | grep -qivE -- "--dry-run"; then
  decide ask "$SAVE_REASON"
fi
if printf '%s\n' "$segments" | grep -qiE "${SF}project[[:space:]]+deploy[[:space:]]+(quick|resume)"; then
  decide ask "$SAVE_REASON"
fi
if printf '%s\n' "$segments" | grep -iE "${SF}(force:source:deploy|force:mdapi:deploy)" | grep -qivE -- "(--checkonly|[[:space:]]-c([[:space:]]|$))"; then
  decide ask "$SAVE_REASON"
fi
if printf '%s\n' "$segments" | grep -qiE "${SF}(force:source:push|package[[:space:]]+install|force:package:install)"; then
  decide ask "$SAVE_REASON"
fi

exit 0
