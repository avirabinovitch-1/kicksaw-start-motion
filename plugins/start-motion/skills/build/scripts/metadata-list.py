"""Lists the Salesforce metadata a branch changed, one Type/Member per line, for the Jira story's Metadata field.

The Metadata field on Kicksaw stories holds one line per component, in the form the team already uses on HLS:
    CustomObject/Note__c
    CustomField/Note__c.Matter__c
    Layout/Case-Matter Layout
    Flow/Audit_Before_Save_Set_Matter_Owner
The list comes from git, never from reading or remembering the org, so it always matches what the pull request holds.

Run in the client's repo:
    python3 -I metadata-list.py list <base> <branch>          what the branch added or changed, against base
    python3 -I metadata-list.py list <base> <branch> --removed what the branch deleted (goes in Build/Solution Details, not Metadata)
    python3 -I metadata-list.py merge <field.txt> <new.txt>   the story's field after this task: what is there, then any new lines
    python3 -I metadata-list.py drop <field.txt> <task.txt> <kept.txt>
                                                              take an undone task's lines out, keeping any line another task
                                                              of the story still needs (kept.txt: the other tasks' lists)
Files that are not metadata (docs/, scripts, config) are skipped. A metadata path the script cannot name is printed to
stderr as "not named: <path>" so a person can add it by hand; it never guesses.
"""
import json, os, subprocess, sys

# folder -> metadata type, for components that are one file (or one bundle folder) each
TOP = {
    'applications': 'CustomApplication', 'approvalProcesses': 'ApprovalProcess', 'assignmentRules': 'AssignmentRules',
    'aura': 'AuraDefinitionBundle', 'autoResponseRules': 'AutoResponseRules', 'classes': 'ApexClass',
    'components': 'ApexComponent', 'connectedApps': 'ConnectedApp', 'contentassets': 'ContentAsset',
    'customMetadata': 'CustomMetadata', 'customPermissions': 'CustomPermission', 'dashboards': 'Dashboard',
    'duplicateRules': 'DuplicateRule', 'email': 'EmailTemplate', 'escalationRules': 'EscalationRules',
    'externalCredentials': 'ExternalCredential', 'flexipages': 'FlexiPage', 'flows': 'Flow',
    'globalValueSets': 'GlobalValueSet', 'groups': 'Group', 'labels': 'CustomLabels', 'layouts': 'Layout',
    'letterhead': 'Letterhead', 'lwc': 'LightningComponentBundle', 'matchingRules': 'MatchingRules',
    'namedCredentials': 'NamedCredential', 'pages': 'ApexPage', 'permissionsetgroups': 'PermissionSetGroup',
    'permissionsets': 'PermissionSet', 'profiles': 'Profile', 'queues': 'Queue', 'quickActions': 'QuickAction',
    'remoteSiteSettings': 'RemoteSiteSetting', 'reportTypes': 'ReportType', 'reports': 'Report', 'roles': 'Role',
    'sharingRules': 'SharingRules', 'staticresources': 'StaticResource', 'standardValueSets': 'StandardValueSet',
    'tabs': 'CustomTab', 'triggers': 'ApexTrigger', 'workflows': 'Workflow', 'settings': 'Settings',
    'customNotificationTypes': 'CustomNotificationType', 'notificationTypeConfig': 'NotificationTypeConfig',
    'pathAssistants': 'PathAssistant', 'listViews': 'ListView', 'objectTranslations': 'CustomObjectTranslation',
}
# objects/<Object>/<child folder>/<Name>.<suffix>-meta.xml -> type, member Object.Name
CHILD = {
    'fields': 'CustomField', 'recordTypes': 'RecordType', 'validationRules': 'ValidationRule',
    'compactLayouts': 'CompactLayout', 'listViews': 'ListView', 'webLinks': 'WebLink', 'fieldSets': 'FieldSet',
    'businessProcesses': 'BusinessProcess', 'sharingReasons': 'SharingReason', 'indexes': 'Index',
}
BUNDLES = {'aura', 'lwc', 'staticresources', 'contentassets'}
FOLDERED = {'reports', 'dashboards', 'email', 'documents'}


def package_dirs():
    try:
        cfg = json.load(open('sfdx-project.json', encoding='utf-8'))
        return [p['path'].strip('/') for p in cfg.get('packageDirectories', []) if p.get('path')]
    except (OSError, ValueError):
        return ['force-app']


def name_of(path, pkgs):
    """Type/Member for one source-format path, None when the path is not metadata, '?' when it is but cannot be named."""
    if not any(path == p or path.startswith(p + '/') for p in pkgs):
        return None
    parts = path.split('/')
    # find the metadata folder: the first segment that is a known folder (skips main/default and similar)
    for i, seg in enumerate(parts):
        if seg == 'objects' and len(parts) > i + 1:
            obj = parts[i + 1]
            rest = parts[i + 2:]
            if len(rest) == 1 and rest[0].endswith('.object-meta.xml'):
                return 'CustomObject/' + obj
            if len(rest) == 2 and rest[0] in CHILD:
                return '%s/%s.%s' % (CHILD[rest[0]], obj, rest[1].split('.')[0])
            return '?'
        if seg in TOP:
            kind = TOP[seg]
            rest = parts[i + 1:]
            if not rest:
                return '?'
            if seg in BUNDLES:
                return '%s/%s' % (kind, rest[0].split('.')[0])
            if seg in FOLDERED:
                if len(rest) == 1:
                    return '%sFolder/%s' % (kind, rest[0].split('.')[0])
                return '%s/%s/%s' % (kind, '/'.join(rest[:-1]), rest[-1].split('.')[0])
            if seg == 'customMetadata':
                return 'CustomMetadata/' + rest[-1].replace('.md-meta.xml', '')
            if seg == 'settings':
                return 'Settings/' + rest[-1].split('.')[0]
            f = rest[-1]
            if f.endswith('-meta.xml') and seg in ('classes', 'triggers', 'pages', 'components'):
                f = f[:-len('-meta.xml')]
            stem = f
            for suf in ('.cls', '.trigger', '.page', '.component'):
                if stem.endswith(suf):
                    stem = stem[:-len(suf)]
                    break
            else:
                # Layout names keep their spaces and dashes: "Case-Matter Layout.layout-meta.xml"
                stem = stem.rsplit('.', 2)[0] if stem.endswith('-meta.xml') else stem.split('.')[0]
            return '%s/%s' % (kind, stem)
    return '?'


def changed(base, branch):
    out = subprocess.run(['git', 'diff', '--name-status', '--no-renames', '%s...%s' % (base, branch)],
                         capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        status, _, path = line.partition('\t')
        yield status[:1], path


def cmd_list(base, branch, removed):
    pkgs, seen, out = package_dirs(), set(), []
    for status, path in changed(base, branch):
        if (status == 'D') != removed:
            continue
        n = name_of(path, pkgs)
        if n is None:
            continue
        if n == '?':
            print('not named: ' + path, file=sys.stderr)
            continue
        if n not in seen:
            seen.add(n)
            out.append(n)
    # the order a reader builds in: data model, then pages, then automation, then access
    order = ['CustomObject', 'CustomField', 'RecordType', 'BusinessProcess', 'ValidationRule', 'CompactLayout',
             'GlobalValueSet', 'StandardValueSet', 'Layout', 'FlexiPage', 'QuickAction', 'CustomTab', 'ListView',
             'Flow', 'ApexClass', 'ApexTrigger', 'LightningComponentBundle', 'PermissionSet', 'PermissionSetGroup',
             'Profile']
    rank = lambda n: (order.index(n.split('/')[0]) if n.split('/')[0] in order else len(order), n.lower())
    print('\n'.join(sorted(out, key=rank)))


def lines(path):
    return [l.strip() for l in open(path, encoding='utf-8').read().splitlines() if l.strip()]


def cmd_merge(field, new):
    have = lines(field) if os.path.exists(field) else []
    seen = set(have)
    print('\n'.join(have + [n for n in lines(new) if n not in seen and not seen.add(n)]))


def cmd_drop(field, task, kept):
    keep = set(lines(kept)) if os.path.exists(kept) else set()
    gone = set(lines(task)) - keep
    print('\n'.join(l for l in lines(field) if l not in gone))


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == 'list':
        return cmd_list(a[1], a[2], '--removed' in a)
    if len(a) == 3 and a[0] == 'merge':
        return cmd_merge(a[1], a[2])
    if len(a) == 4 and a[0] == 'drop':
        return cmd_drop(a[1], a[2], a[3])
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
