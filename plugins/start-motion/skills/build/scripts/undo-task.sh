#!/usr/bin/env bash
# Undo for a rejected build task (Kicksaw Project Start Motion, /start-motion:build).
#
# A task that was deployed to the sandbox for a by-hand check and then rejected leaves its change behind.
# This script works out, from git alone, exactly what that one task added and changed, so it can be taken
# back out. It never looks at the org and never decides anything: the list comes from the repo.
#
#   undo-task.sh prepare <task ID> [main branch]   writes .start-motion/undo/<task ID>/ in the repo:
#                                                    destructiveChanges.xml  what this task created (to remove)
#                                                    package.xml             the empty manifest that goes with it
#                                                    restore.txt             files this task changed (redeploy main's copy)
#                                                    by-hand.txt             what it created that this script cannot name
#                                                    undo-list.txt           the same, in words, for the person
#   undo-task.sh verify <path to destructiveChanges.xml> [main branch]
#                                                  exit 0 only when every member in the file is something the
#                                                  task's branch created and main does not have. The org guard
#                                                  calls this before it lets a removal through.
#
# Limits, on purpose: only a task whose branch is not merged into main; only files the branch ADDED
# (never something main already has); never records. Merged work is removed by a new, named task.
set -u

die() { echo "undo-task: $*" >&2; exit 1; }

mode="${1:-}"; [ -n "$mode" ] || die "usage: undo-task.sh prepare <task ID> [main] | verify <destructiveChanges.xml> [main]"

git rev-parse --show-toplevel >/dev/null 2>&1 || die "not inside a git repo"
root="$(git rev-parse --show-toplevel)"
cd "$root" || die "cannot open the repo"

# members <task ID> <main>: prints "Type<TAB>Member" for every metadata file the task branch added,
# and "BYHAND<TAB>path" for added metadata it cannot name.
members() {
  local task="$1" main="$2" branch="task/$1"
  git rev-parse --verify --quiet "$branch" >/dev/null || die "no branch $branch"
  git rev-parse --verify --quiet "$main" >/dev/null || die "no branch $main"
  if git merge-base --is-ancestor "$branch" "$main"; then
    die "$branch is already merged into $main. Merged work is not undone here; removing it is a new, named task."
  fi
  git diff --name-only --diff-filter=A "$main...$branch" | while IFS= read -r f; do
    case "$f" in
      docs/*|.start-motion/*|*.md) continue ;;
    esac
    base="${f##*/}"
    case "$f" in
      */objects/*/fields/*.field-meta.xml)
        obj="${f%/fields/*}"; obj="${obj##*/}"; printf 'CustomField\t%s.%s\n' "$obj" "${base%.field-meta.xml}" ;;
      */objects/*/validationRules/*.validationRule-meta.xml)
        obj="${f%/validationRules/*}"; obj="${obj##*/}"; printf 'ValidationRule\t%s.%s\n' "$obj" "${base%.validationRule-meta.xml}" ;;
      */objects/*/recordTypes/*.recordType-meta.xml)
        obj="${f%/recordTypes/*}"; obj="${obj##*/}"; printf 'RecordType\t%s.%s\n' "$obj" "${base%.recordType-meta.xml}" ;;
      */objects/*/listViews/*.listView-meta.xml)
        obj="${f%/listViews/*}"; obj="${obj##*/}"; printf 'ListView\t%s.%s\n' "$obj" "${base%.listView-meta.xml}" ;;
      */objects/*/compactLayouts/*.compactLayout-meta.xml)
        obj="${f%/compactLayouts/*}"; obj="${obj##*/}"; printf 'CompactLayout\t%s.%s\n' "$obj" "${base%.compactLayout-meta.xml}" ;;
      */objects/*/*.object-meta.xml)   printf 'CustomObject\t%s\n' "${base%.object-meta.xml}" ;;
      */flows/*.flow-meta.xml)         printf 'Flow\t%s\n' "${base%.flow-meta.xml}" ;;
      */classes/*.cls)                 printf 'ApexClass\t%s\n' "${base%.cls}" ;;
      */classes/*.cls-meta.xml)        : ;;
      */triggers/*.trigger)            printf 'ApexTrigger\t%s\n' "${base%.trigger}" ;;
      */triggers/*.trigger-meta.xml)   : ;;
      */permissionsets/*.permissionset-meta.xml) printf 'PermissionSet\t%s\n' "${base%.permissionset-meta.xml}" ;;
      */layouts/*.layout-meta.xml)     printf 'Layout\t%s\n' "${base%.layout-meta.xml}" ;;
      */flexipages/*.flexipage-meta.xml) printf 'FlexiPage\t%s\n' "${base%.flexipage-meta.xml}" ;;
      */tabs/*.tab-meta.xml)           printf 'CustomTab\t%s\n' "${base%.tab-meta.xml}" ;;
      */quickActions/*.quickAction-meta.xml) printf 'QuickAction\t%s\n' "${base%.quickAction-meta.xml}" ;;
      *) printf 'BYHAND\t%s\n' "$f" ;;
    esac
  done | sort -u
}

case "$mode" in
  prepare)
    task="${2:-}"; main="${3:-main}"
    printf '%s' "$task" | grep -qE '^[A-Za-z0-9._-]+$' || die "task ID must be letters, numbers, dots, dashes or underscores"
    list="$(members "$task" "$main")" || exit 1
    out=".start-motion/undo/$task"; mkdir -p "$out"
    created="$(printf '%s\n' "$list" | grep -v '^BYHAND' | grep -v '^$' || true)"
    printf '%s\n' "$list" | grep '^BYHAND' | cut -f2 > "$out/by-hand.txt" || true
    git diff --name-only --diff-filter=MR "$main...task/$task" | grep -vE '^(docs/|\.start-motion/)|\.md$' > "$out/restore.txt" || true
    {
      echo '<?xml version="1.0" encoding="UTF-8"?>'
      echo '<Package xmlns="http://soap.sforce.com/2006/04/metadata">'
      printf '%s\n' "$created" | cut -f1 | grep -v '^$' | sort -u | while IFS= read -r type; do
        echo '    <types>'
        printf '%s\n' "$created" | awk -F'\t' -v t="$type" '$1==t {print "        <members>" $2 "</members>"}'
        echo "        <name>$type</name>"
        echo '    </types>'
      done
      echo '</Package>'
    } > "$out/destructiveChanges.xml"
    printf '<?xml version="1.0" encoding="UTF-8"?>\n<Package xmlns="http://soap.sforce.com/2006/04/metadata">\n    <version>62.0</version>\n</Package>\n' > "$out/package.xml"
    {
      echo "Undo for task $task (branch task/$task, not merged into $main)"
      echo
      echo "Created by this task, to be removed from the sandbox:"
      if [ -n "$created" ]; then printf '%s\n' "$created" | awk -F'\t' '{print "  " $1 ": " $2}'; else echo "  nothing"; fi
      echo
      echo "Changed by this task, to be put back to the $main version:"
      if [ -s "$out/restore.txt" ]; then sed 's/^/  /' "$out/restore.txt"; else echo "  nothing"; fi
      echo
      echo "Created by this task but not removable by this script (remove by hand):"
      if [ -s "$out/by-hand.txt" ]; then sed 's/^/  /' "$out/by-hand.txt"; else echo "  nothing"; fi
    } > "$out/undo-list.txt"
    cat "$out/undo-list.txt"
    ;;
  verify)
    file="${2:-}"; main="${3:-main}"
    [ -f "$file" ] || die "no such file: $file"
    task="$(printf '%s' "$file" | sed -nE 's#^(.*/)?\.start-motion/undo/([A-Za-z0-9._-]+)/destructiveChanges\.xml$#\2#p')"
    [ -n "$task" ] || die "the file is not at .start-motion/undo/<task ID>/destructiveChanges.xml"
    allowed="$(members "$task" "$main" | grep -v '^BYHAND')" || exit 1
    # every (type, member) pair in the file must be in the allowed list
    bad="$(awk '
      /<types>/ {n=0}
      /<members>/ {m=$0; sub(/.*<members>/,"",m); sub(/<\/members>.*/,"",m); mem[n++]=m}
      /<name>/ {t=$0; sub(/.*<name>/,"",t); sub(/<\/name>.*/,"",t); for(i=0;i<n;i++) print t "\t" mem[i]}
    ' "$file" | while IFS= read -r pair; do
      printf '%s\n' "$allowed" | grep -qxF "$pair" || echo "$pair"
    done)"
    if [ -n "$bad" ]; then
      echo "undo-task: these are not things task $task created, so they will not be removed:" >&2
      printf '%s\n' "$bad" | sed 's/^/  /' >&2
      exit 1
    fi
    grep -q '<members>\*</members>' "$file" && die "wildcards are not allowed in an undo"
    exit 0
    ;;
  *) die "unknown mode: $mode" ;;
esac
