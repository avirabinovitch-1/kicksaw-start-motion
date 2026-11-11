# Copy of plugins/start-motion/shared/build-review.py, written by scripts/sync-agents.py. Do not edit here.
"""Builds the SA's design and build review page: one HTML page per client build plan.

What it is for: the SA is accountable for every component built. This page shows, in one place, what is being created
or changed in the org and why: the stories it serves, the rules (decisions) that shape it, where it differs from the
stories, a data model diagram, the flows, every object, field, record type, rule, automation, page, action and
permission set with its details and status, who can do what, the build tasks, open questions and checks. It is modeled
on Ben Bolding's Fred Hutch epic designs (Notion), with diagrams added.

Two inputs:
- content.json, written by the stage command from the design, the build plan, the Decisions tab and the stories
  (the shape is in references/build-review.md). Planned components live there until they are built.
- the client's repo: every component that differs between --base (the org as it was read, usually the org reader's
  commit or main when the plan was written) and each --head (main, and any open task branches). Details are read from
  the metadata files themselves, so the page never says more than the repo holds.

Run in the client's repo:
    python3 -I build-review.py --content content.json --base <ref> --head main [--head task/E1.2-T1 ...] --out build-review.html
Without a repo (planning in Claude chat from the plan alone): leave out --base and --head.
"""
import argparse, html, json, os, re, subprocess, sys, xml.etree.ElementTree as ET
from datetime import date

NS = '{http://soap.sforce.com/2006/04/metadata}'
E = lambda s: html.escape('' if s is None else str(s), quote=True)


def md(s):
    """**bold**, `code` and [text](url) in content text, escaped first."""
    s = E(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2">\1</a>', s)
    return s


# ---------- reading the repo ----------

def git(*a):
    return subprocess.run(['git'] + list(a), capture_output=True, text=True).stdout


def show(ref, path):
    r = subprocess.run(['git', 'show', '%s:%s' % (ref, path)], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def xml(text):
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    return root


def t(node, tag):
    if node is None:
        return None
    x = node.find(NS + tag)
    return x.text if x is not None else None


def field_details(root):
    ftype = t(root, 'type') or ('Formula' if t(root, 'formula') else '')
    bits = []
    if t(root, 'formula'):
        f = ' '.join((t(root, 'formula') or '').split())
        bits.append('Formula (%s): %s' % (ftype or 'value', f[:140] + ('…' if len(f) > 140 else '')))
    elif ftype in ('Lookup', 'MasterDetail'):
        bits.append('%s to %s' % ('Master-detail' if ftype == 'MasterDetail' else 'Lookup', t(root, 'referenceTo')))
    elif ftype == 'Summary':
        op = t(root, 'summaryOperation') or ''
        bits.append('Roll-up %s of %s' % (op.lower(), t(root, 'summarizedField') or t(root, 'summaryForeignKey') or ''))
    else:
        n = t(root, 'length') or t(root, 'precision')
        bits.append(ftype + ('(%s)' % n if n else ''))
    vals = [t(v, 'fullName') for v in root.iter(NS + 'value') if t(v, 'fullName')]
    if vals:
        bits.append(', '.join(vals[:12]) + (' and %d more' % (len(vals) - 12) if len(vals) > 12 else ''))
    if t(root, 'required') == 'true':
        bits.append('required')
    if t(root, 'externalId') == 'true':
        bits.append('external ID')
    if t(root, 'unique') == 'true':
        bits.append('unique')
    return ftype, '; '.join(b for b in bits if b), t(root, 'referenceTo')


def describe(kind, member, text):
    """A one-line plain description of a component from its metadata file."""
    root = xml(text) if text else None
    if root is None:
        return {}
    out = {'label': t(root, 'label') or t(root, 'masterLabel')}
    if kind == 'CustomField':
        ftype, det, ref = field_details(root)
        h = t(root, 'inlineHelpText') or t(root, 'description')
        out.update(details=det + ('. Help: "%s"' % h if h else ''), ftype=ftype, ref=ref)
    elif kind == 'CustomObject':
        out['details'] = '; '.join(x for x in [
            'sharing %s' % t(root, 'sharingModel') if t(root, 'sharingModel') else '',
            'name %s' % (t(root.find(NS + 'nameField'), 'type') or '') if root.find(NS + 'nameField') is not None else '',
            'history on' if t(root, 'enableHistory') == 'true' else '',
            'reports on' if t(root, 'enableReports') == 'true' else ''] if x)
    elif kind == 'ValidationRule':
        out['details'] = 'Blocks save when: %s. Message: "%s"' % (
            (t(root, 'errorConditionFormula') or '').strip().replace('\n', ' ')[:220], t(root, 'errorMessage') or '')
    elif kind == 'Flow':
        st = root.find(NS + 'start')
        trig = ' '.join(x for x in [t(st, 'triggerType'), t(st, 'recordTriggerType'), t(st, 'object')] if x)
        out['details'] = '; '.join(x for x in [t(root, 'processType'), trig and 'starts ' + trig, t(root, 'status')] if x)
        out['object'] = t(st, 'object')
        out['trigger'] = (t(st, 'recordTriggerType') or t(st, 'triggerType') or '').strip()
    elif kind == 'RecordType':
        out['details'] = 'active' if t(root, 'active') == 'true' else 'inactive'
    elif kind == 'FlexiPage':
        out['details'] = '; '.join(x for x in [t(root, 'type'), t(root, 'sobjectType')] if x)
        out['object'] = t(root, 'sobjectType')
    elif kind == 'QuickAction':
        out['details'] = '; '.join(x for x in [t(root, 'type'), t(root, 'flowDefinition') and 'runs ' + t(root, 'flowDefinition')] if x)
    elif kind == 'PermissionSet':
        objs = [(t(o, 'object'), ''.join(l for l, k in (('C', 'allowCreate'), ('R', 'allowRead'), ('E', 'allowEdit'),
                ('D', 'allowDelete')) if t(o, k) == 'true')) for o in root.iter(NS + 'objectPermissions')]
        flds = [(t(f, 'field'), 'Edit' if t(f, 'editable') == 'true' else 'Read' if t(f, 'readable') == 'true' else '')
                for f in root.iter(NS + 'fieldPermissions')]
        out['objects'] = [o for o in objs if o[0]]
        out['fields'] = [f for f in flds if f[0]]
        out['details'] = '%d objects, %d fields' % (len(out['objects']), len(out['fields']))
    elif kind == 'ApexClass' or kind == 'ApexTrigger':
        out['details'] = 'API %s' % (t(root, 'apiVersion') or '')
    elif kind == 'ListView':
        cols = [c.text for c in root.iter(NS + 'columns')]
        out['details'] = 'columns: ' + ', '.join(cols[:8]) if cols else ''
    return out


def all_flows(head):
    """Every record-triggered flow in the head's tree, existing ones included: (object, trigger) -> [flow names]."""
    out = {}
    for path in git('ls-tree', '-r', '--name-only', head).splitlines():
        if not path.endswith('.flow-meta.xml'):
            continue
        root = xml(show(head, path) or '')
        st = root.find(NS + 'start') if root is not None else None
        if st is None or not t(st, 'object') or t(root, 'status') not in (None, 'Active'):
            continue
        key = (t(st, 'object'), '%s %s' % (t(st, 'triggerType') or '', t(st, 'recordTriggerType') or ''))
        out.setdefault(key, []).append(os.path.basename(path).replace('.flow-meta.xml', ''))
    return out


def inventory(base, heads):
    """Every component that differs between base and each head, with what changed and its details."""
    try:
        import importlib.util
        here = os.path.dirname(os.path.abspath(__file__))
        cand = [os.path.join(here, 'metadata-list.py'), os.path.join(here, '..', '..', 'build', 'scripts', 'metadata-list.py'),
                os.path.join(here, '..', 'skills', 'build', 'scripts', 'metadata-list.py')]
        spec = importlib.util.spec_from_file_location('ml', next(p for p in cand if os.path.exists(p)))
        ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
    except StopIteration:
        sys.exit('metadata-list.py not found next to this script')
    pkgs = ml.package_dirs()
    rows = {}
    for head in heads:
        status = 'Merged' if head in ('main', 'master', 'origin/main') else 'Built'
        for line in git('diff', '--name-status', '--no-renames', '%s...%s' % (base, head)).splitlines():
            st, _, path = line.partition('\t')
            name = ml.name_of(path, pkgs)
            if not name or name == '?':
                continue
            kind, member = name.split('/', 1)
            r = rows.get(name)
            if r and r['status'] == 'Merged':
                continue
            change = 'Removed' if st.startswith('D') else ('Changed' if show(base, path) is not None else 'New')
            text = show(head, path) if change != 'Removed' else show(base, path)
            info = describe(kind, member, text) if path.endswith('.xml') else {}
            prev = rows.get(name, {})
            rows[name] = dict(prev, type=kind, member=member, change=prev.get('change') if prev.get('change') == 'New' else change,
                              status=status, branch=head, path=path, **{k: v for k, v in info.items() if v})
    return rows


# ---------- diagrams ----------

def obj_of(r):
    """The object a component belongs to, for grouping."""
    k, m = r['type'], r['member']
    if k == 'CustomObject':
        return m
    if k in ('CustomField', 'RecordType', 'ValidationRule', 'CompactLayout', 'ListView', 'WebLink', 'FieldSet', 'BusinessProcess'):
        return m.split('.', 1)[0]
    if k == 'QuickAction' and '.' in m:
        return m.split('.', 1)[0]
    if k == 'Layout':
        return m.split('-', 1)[0]
    if r.get('object'):
        return r['object']
    return None


def short_type(r):
    d = r.get('details') or ''
    if r['type'] != 'CustomField':
        return ''
    if d.startswith('Formula'):
        return 'formula'
    if d.startswith('Roll-up'):
        return 'roll-up'
    m = re.match(r'(Lookup|Master-detail) to (\w+)', d)
    if m:
        return ('→ ' if m.group(1) == 'Lookup' else '⇒ ') + m.group(2)
    return (r.get('ftype') or d.split(';')[0].split('(')[0]).strip().lower()


def erd(rows, content):
    """Entity boxes with their new and changed fields; each relationship drawn from its field to the parent."""
    ents = {}
    for r in rows.values():
        if r['type'] == 'CustomObject':
            ents.setdefault(r['member'], {'state': r['change'], 'label': r.get('label') or r['member'], 'fields': []})
    for r in sorted(rows.values(), key=lambda r: r['member']):
        if r['type'] != 'CustomField':
            continue
        o, f = r['member'].split('.', 1)
        ents.setdefault(o, {'state': 'Existing', 'label': o.replace('__c', '').replace('_', ' '), 'fields': []})
        ref = r.get('ref')
        if not ref:
            m = re.match(r'(?i)(lookup|master-detail) to (\w+)', r.get('details') or '')
            ref = m.group(2) if m else None
        md_ = r.get('ftype') == 'MasterDetail' or (r.get('details') or '').startswith('Master-detail')
        ents[o]['fields'].append({'name': f, 'type': short_type(r), 'ref': ref, 'md': md_, 'change': r['change'], 'status': r['status']})
        if ref:
            ents.setdefault(ref, {'state': 'Existing', 'label': ref.replace('__c', '').replace('_', ' '), 'fields': []})
    for m in content.get('solution_map') or []:
        if m.get('later_only') and m.get('object'):
            fl = []
            if m.get('parent'):
                fl.append({'name': m.get('parent_field') or m['parent'], 'type': '⇒ ' + m['parent'], 'ref': m['parent'], 'md': True, 'change': 'Later', 'status': 'Planned'})
            ents.setdefault(m['object'], {'state': 'Later', 'label': m.get('label') or m['object'].replace('__c', '').replace('_', ' '), 'fields': fl})
    if not ents:
        return ''
    parents = {o: {f['ref'] for f in e['fields'] if f['ref'] and f['ref'] != o} for o, e in ents.items()}
    level = {}

    def lv(o, seen=()):
        if o in level:
            return level[o]
        if o in seen or not parents.get(o):
            level[o] = 0
            return 0
        level[o] = 1 + max(lv(p, seen + (o,)) for p in parents[o] if p in ents)
        return level[o]
    for o in ents:
        lv(o)
    cols = {}
    for o in sorted(ents, key=lambda x: (ents[x]['state'] == 'Existing', x)):
        cols.setdefault(level[o], []).append(o)
    MAXF, BW, GX, GY, PAD, HH, RH = 10, 290, 100, 28, 12, 44, 19
    hgt = lambda o: HH + max(1, min(len(ents[o]['fields']), MAXF + 1)) * RH + 8
    pos, ncols = {}, max(cols) + 1
    for c, names in cols.items():
        y = PAD + 18
        for o in names:
            pos[o] = (PAD + c * (BW + GX), y)
            y += hgt(o) + GY
    W = PAD * 2 + ncols * BW + (ncols - 1) * GX
    H = max(pos[o][1] + hgt(o) for o in ents) + PAD
    out = ['<svg viewBox="0 0 %d %d" style="max-width:%dpx" role="img" aria-label="Data model: %d objects, their new fields and how they relate" class="dia erd">' % (W, H, W, len(ents)),
           '<defs><marker id="one" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path d="M2,1 L11,6 L2,11" fill="none" stroke="currentColor" stroke-width="1.3"/></marker></defs>']
    for c in sorted(cols):
        out.append('<text x="%d" y="%d" class="dl">%s</text>' % (PAD + c * (BW + GX), PAD + 6, 'PARENTS' if c == 0 else 'CHILDREN' if c == 1 else 'CHILDREN · LEVEL %d' % c))
    rowy = {}
    for o, (x, y) in pos.items():
        for i, f in enumerate(ents[o]['fields'][:MAXF]):
            rowy[(o, f['name'])] = y + HH + i * RH + RH / 2 + 4
    # relationship lines first, so boxes sit on top
    k = 0
    for o, e in ents.items():
        for f in e['fields'][:MAXF]:
            p = f['ref']
            if not p or p not in pos or p == o:
                continue
            (cx, cy), (px, py) = pos[o], pos[p]
            y1 = rowy[(o, f['name'])]
            y2 = py + 22
            if cx > px:
                x1, x2 = cx, px + BW
                mx = x2 + 20 + (k % 4) * 9
                d = 'M%d,%.1f H%d V%.1f H%d' % (x1, y1, mx, y2, x2)
            else:
                x1, x2 = cx + BW, px + BW
                mx = max(x1, x2) + 18 + (k % 4) * 9
                d = 'M%d,%.1f H%d V%.1f H%d' % (x1, y1, mx, y2, x2)
            k += 1
            out.append('<path d="%s" class="rel%s" marker-end="url(#one)"%s/>' % (d, ' md' if f['md'] and f['change'] != 'Later' else '', ' stroke-dasharray="4 3"' if f['change'] in ('Removed', 'Later') else ''))
    for o, (x, y) in pos.items():
        e, h = ents[o], hgt(o)
        cls = {'New': 'bn', 'Changed': 'bc', 'Later': 'bl'}.get(e['state'], 'be')
        tag = {'New': 'NEW', 'Changed': 'CHANGED', 'Later': 'LATER EPIC'}.get(e['state'], 'STANDARD' if not o.endswith('__c') else 'EXISTING')
        out.append('<g class="%s"><rect x="%d" y="%d" width="%d" height="%d" rx="6" class="box"/><rect x="%d" y="%d" width="%d" height="%d" rx="6" class="hd"/><rect x="%d" y="%d" width="%d" height="8" class="hd"/>' % (cls, x, y, BW, h, x, y, BW, HH - 6, x, y + HH - 14, BW))
        out.append('<text x="%d" y="%d" class="bt">%s</text><text x="%d" y="%d" class="bs">%s</text><text x="%d" y="%d" class="tg" text-anchor="end">%s</text>' % (
            x + 10, y + 18, E(e['label'][:24]), x + 10, y + 32, E(o[:34]), x + BW - 10, y + 18, tag))
        fl = e['fields']
        if not fl:
            out.append('<text x="%d" y="%d" class="fe">%s</text>' % (x + 10, y + HH + 14, 'built in a later epic' if e['state'] == 'Later' else 'no new fields'))
        for i, f in enumerate(fl[:MAXF]):
            fy = y + HH + i * RH + 14
            mark = {'New': '+', 'Changed': '~', 'Removed': '−', 'Later': '·'}.get(f['change'], '')
            out.append('<text x="%d" y="%d" class="fm %s">%s</text><text x="%d" y="%d" class="fn%s">%s</text><text x="%d" y="%d" class="ft" text-anchor="end">%s</text>' % (
                x + 10, fy, {'New': 'pn', 'Changed': 'pc', 'Removed': 'pr'}.get(f['change'], ''), mark, x + 22, fy,
                ' fw' if f['status'] in ('Planned', 'Waits') else '', E(f['name'] if len(f['name']) <= 27 else f['name'][:25] + '…'), x + BW - 10, fy, E(f['type'][:16])))
        if len(fl) > MAXF:
            out.append('<text x="%d" y="%d" class="fe">and %d more, in Every component</text>' % (x + 22, y + HH + MAXF * RH + 14, len(fl) - MAXF))
        out.append('</g>')
    out.append('</svg>')
    return ('<figure class="fig">%s<figcaption><span class="key"><i class="kb bn"></i>New object</span><span class="key"><i class="kb bc"></i>Changed</span>'
            '<span class="key"><i class="kb be"></i>Existing</span>%s<span class="key">+ new field, ~ changed field, italic not built yet</span>'
            '<span class="key">→ lookup, ⇒ master-detail</span></figcaption></figure>') % (''.join(out), '<span class="key"><i class="kb bl"></i>Later epic</span>' if any(e['state'] == 'Later' for e in ents.values()) else '')


def flow_svg(flow, i):
    steps = flow.get('steps') or []
    if not steps:
        return ''
    per, BW, BH, GX, GY, PAD = 4, 200, 78, 30, 34, 6
    nrow = (len(steps) + per - 1) // per
    cols_used = min(per, len(steps))
    W = PAD * 2 + cols_used * BW + (cols_used - 1) * GX
    H = PAD * 2 + nrow * BH + (nrow - 1) * GY
    out = ['<svg viewBox="0 0 %d %d" style="max-width:%dpx" role="img" aria-label="%s, in %d steps" class="dia flow">' % (W, H, W, E(flow.get('name')), len(steps)),
           '<defs><marker id="ar%d" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>' % i]
    def at(n):
        r, c = divmod(n, per)
        if r % 2:
            c = per - 1 - c
        return PAD + c * (BW + GX), PAD + r * (BH + GY), r, c
    for n in range(len(steps) - 1):
        x, y, r, c = at(n); x2, y2, r2, c2 = at(n + 1)
        if r2 == r:
            a, b = (x + BW, x2) if c2 > c else (x, x2 + BW)
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="fl" marker-end="url(#ar%d)"/>' % (a, y + BH / 2, b, y + BH / 2, i))
        else:
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="fl" marker-end="url(#ar%d)"/>' % (x + BW / 2, y + BH, x2 + BW / 2, y2, i))
    for n, s in enumerate(steps):
        x, y, _, _ = at(n)
        auto = (s.get('actor') or '').lower() in ('system', 'flow', 'automation', 'salesforce')
        out.append('<g class="%s"><rect x="%d" y="%d" width="%d" height="%d" rx="8"/>' % ('fs' if auto else 'fp', x, y, BW, BH))
        out.append('<circle cx="%d" cy="%d" r="10" class="nb"/><text x="%d" y="%d" class="nt" text-anchor="middle">%d</text>' % (x + 18, y + 18, x + 18, y + 22, n + 1))
        out.append('<text x="%d" y="%d" class="ac">%s</text>' % (x + 34, y + 22, E((s.get('actor') or '').upper()[:24])))
        words, line, lines = (s.get('text') or '').split(), '', []
        for w in words:
            if len(line) + len(w) + 1 > 28:
                lines.append(line); line = w
            else:
                line = (line + ' ' + w).strip()
        lines.append(line)
        for kk, ln in enumerate(lines[:3]):
            out.append('<text x="%d" y="%d" class="st2">%s</text>' % (x + 12, y + 42 + kk * 15, E(ln + ('…' if kk == 2 and len(lines) > 3 else ''))))
        out.append('</g>')
    out.append('</svg>')
    return '<figure class="fig">%s<figcaption><span class="key"><i class="kb fp"></i>A person</span><span class="key"><i class="kb fs"></i>The system</span></figcaption></figure>' % ''.join(out)


# ---------- the page ----------

GROUPS = [
    ('Data model', ['CustomObject', 'CustomField', 'RecordType', 'BusinessProcess', 'GlobalValueSet', 'StandardValueSet', 'CustomMetadata']),
    ('Rules', ['ValidationRule', 'DuplicateRule', 'MatchingRules']),
    ('Automation', ['Flow', 'ApexClass', 'ApexTrigger', 'Workflow', 'ApprovalProcess', 'AssignmentRules']),
    ('Pages and actions', ['FlexiPage', 'Layout', 'CompactLayout', 'QuickAction', 'ListView', 'CustomTab', 'LightningComponentBundle', 'CustomApplication']),
    ('Access', ['PermissionSet', 'PermissionSetGroup', 'Profile', 'SharingRules', 'Queue', 'Group', 'Role']),
    ('Reporting', ['ReportType', 'Report', 'Dashboard', 'ReportFolder', 'DashboardFolder']),
]
FRIENDLY = {'CustomObject': 'Object', 'CustomField': 'Field', 'RecordType': 'Record type', 'ValidationRule': 'Validation rule',
            'Flow': 'Flow', 'ApexClass': 'Apex class', 'ApexTrigger': 'Apex trigger', 'FlexiPage': 'Lightning page', 'Layout': 'Page layout',
            'CompactLayout': 'Compact layout', 'QuickAction': 'Action', 'ListView': 'List view', 'CustomTab': 'Tab',
            'PermissionSet': 'Permission set', 'PermissionSetGroup': 'Permission set group', 'LightningComponentBundle': 'Lightning component',
            'CustomMetadata': 'Custom metadata record', 'GlobalValueSet': 'Global value set', 'ReportType': 'Report type', 'Profile': 'Profile'}
ORDER_IN_OBJ = ['CustomObject', 'CustomField', 'RecordType', 'BusinessProcess', 'ValidationRule', 'CompactLayout', 'Layout', 'FlexiPage',
                'QuickAction', 'ListView', 'Flow', 'ApexTrigger', 'ApexClass']


def group_of(kind):
    for g, kinds in GROUPS:
        if kind in kinds:
            return g
    return 'Other'


def table(head, rows, cls=''):
    if not rows:
        return ''
    return '<div class="tw"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        cls, ''.join('<th>%s</th>' % E(h) for h in head),
        ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows))


def chip(s):
    k = {'New': 'cn', 'Changed': 'cc', 'Removed': 'cr', 'Planned': 'cp', 'Built': 'cb', 'Merged': 'cm',
         'Waits': 'cw', 'Decided': 'cm', 'Proposed': 'cw', 'Existing': 'cp', 'Handed back': 'cr'}.get(s, 'cp')
    return '<span class="chip %s">%s</span>' % (k, E(s))


def api(name):
    """API name in code style, breakable after underscores and dots instead of mid-word."""
    return '<code>%s</code>' % E(name).replace('_', '_<wbr>').replace('.', '.<wbr>')


def logo():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, '..', '..', 'kickoff', 'brand', 'logo-full-color.svg'), os.path.join(here, '..', 'skills', 'kickoff', 'brand', 'logo-full-color.svg')):
        if os.path.exists(p):
            svg = open(p, encoding='utf-8').read()
            return svg.replace('<svg ', '<svg class="logo" role="img" aria-label="Kicksaw" ', 1)
    return '<span class="wordmark">kicksaw</span>'


def plain_chip(sv):
    if sv in ('Waits', 'Handed back'):
        return '<span class="wt">%s</span>' % E(sv)
    return '<span class="sv">%s</span>' % E(sv)


def page(c, rows):
    jira = (c.get('jira_base') or '').rstrip('/')
    jl = lambda key: '<a href="%s/browse/%s">%s</a>' % (E(jira), E(key), E(key)) if jira and key else E(key)
    dec_url = c.get('decisions_url')
    dl = lambda d: '<a href="%s">%s</a>' % (E(dec_url), E(d)) if dec_url else E(d)
    for p in c.get('planned') or []:
        name = '%s/%s' % (p['type'], p['member'])
        r = rows.get(name)
        meta = {k: p[k] for k in ('story', 'task', 'decision', 'why', 'waits', 'object') if p.get(k)}
        if r:
            r.update({k: v for k, v in meta.items() if not r.get(k)})
        else:
            rows[name] = dict(type=p['type'], member=p['member'], change=p.get('change', 'New'),
                              status='Waits' if p.get('waits') else 'Planned', details=p.get('details', ''),
                              label=p.get('label'), ref=p.get('ref'), ftype=p.get('ftype'), **meta)
    allrows = list(rows.values())
    count = lambda f: sum(1 for r in allrows if f(r))

    # decisions: decided ones shape the design; open ones are what the SA still owes
    decs = list(c.get('decisions') or [])
    for r in c.get('rules') or []:  # older content files
        decs.append(dict(r, status='Decided', chosen=r.get('rule'), q=r.get('q') or ''))
    decided = [d for d in decs if d.get('status', 'Decided') == 'Decided']
    open_ = [d for d in decs if d.get('status') == 'Proposed']

    # what the page finds on its own
    found, nofls = [], []
    granted = {f for r in allrows if r['type'] == 'PermissionSet' for f, _ in r.get('fields') or []}
    obj_granted = {o for r in allrows if r['type'] == 'PermissionSet' for o, a in r.get('objects') or [] if 'R' in a}
    for r in allrows:
        built = r['status'] in ('Built', 'Merged')
        d = r.get('details') or ''
        if built and r['type'] == 'CustomField' and r['change'] == 'New' and r['member'] not in granted and 'required' not in d and not d.startswith('Master-detail'):
            nofls.append(r['member'])
        if built and r['type'] == 'CustomObject' and r['change'] == 'New' and r['member'] not in obj_granted:
            found.append('`%s` is new and no permission set in this build grants read on it.' % r['member'])
    if nofls:
        found.insert(0, '%d new field%s that no permission set in this build grants, so only administrators see %s: %s.' % (
            len(nofls), 's' if len(nofls) > 1 else '', 'them' if len(nofls) > 1 else 'it', ', '.join('`%s`' % f for f in nofls)))
    if c.get('planned'):
        orphan = [r['member'] for r in allrows if r['status'] in ('Built', 'Merged') and not r.get('story') and not r.get('task')
                  and r['type'] not in ('PermissionSet', 'Profile', 'Layout', 'FlexiPage', 'ListView', 'CompactLayout')]
        if orphan:
            found.append('%d component%s in the repo that the build plan does not name: %s. Each needs a story and task, or comes out.' % (
                len(orphan), 's are' if len(orphan) > 1 else ' is', ', '.join('`%s`' % o for o in orphan[:15]) + (' and more' if len(orphan) > 15 else '')))
    for k, names in (c.get('_flows') or {}).items():
        if len(names) > 1:
            o, trig = k.split('|')
            found.append('%d active flows run on `%s` at the same moment (%s): %s. Say how they work together, or fold them into one.' % (
                len(names), o, trig.strip(), ', '.join('`%s`' % n for n in names)))

    openrows = []
    KIND = {'SA call': 'Decide', 'Recommended': 'Confirm', 'Client call': 'With the client'}
    for d in open_:
        opts = ' or '.join(o.get('name') for o in d.get('options') or [] if o.get('name'))
        lean = ' Claude recommends %s.' % d['recommended'] if d.get('recommended') else ''
        openrows.append([dl(d.get('id')), KIND.get(d.get('kind'), 'Decide'), md(d.get('q')) + ('<div class="muted">%s.%s</div>' % (E(opts), E(lean)) if opts or lean else '')])
    for n in c.get('needs_you') or []:
        openrows.append(['', E(n.get('kind')), md(n.get('text'))])
    for f in found:
        openrows.append(['', '<span class="wt">Found in the build</span>', md(f)])

    nav, body = [], []

    def sec(anchor, title, inner, lede=None):
        if not inner:
            return
        nav.append('<a href="#%s">%s</a>' % (anchor, E(title)))
        body.append('<section id="%s"><h2>%s</h2>%s%s</section>' % (anchor, E(title), '<p class="sl">%s</p>' % md(lede) if lede else '', inner))

    sec('open', 'Open for the SA', table(['', 'What', 'Item'], openrows, 'open'),
        'Everything here is waiting on a person. Once the SA has worked through it, this section is gone and the decisions below are complete.')
    sec('stories', 'Stories this design serves', table(['Story', 'What the design gives it'],
        [[jl(s_.get('key')) + ' ' + md(s_.get('title')), md(s_.get('gives'))] for s_ in c.get('stories') or []], 'two'))
    sec('differences', 'Where the design differs from the stories', table(['#', 'Story says', 'The design does', 'Recommendation'],
        [[E(d.get('n')), md(d.get('says')), md(d.get('does')), md(d.get('rec'))] for d in c.get('differences') or []]),
        'Each row is a story criterion the design does not meet as written. It closes when the story is reworded or the design changes.')
    sec('decisions', 'Decisions that shape the design', '<ol class="rules">%s</ol>' % ''.join(
        '<li><b>%s</b> %s%s <span class="muted">(%s%s%s)</span></li>' % (
            md(d.get('chosen') or d.get('rule')), md(d.get('why') or ''),
            ' Considered: %s.' % md(d['considered']) if d.get('considered') else '',
            E(d.get('by') or ''), ', ' + E(d.get('date')) if d.get('date') else '', ', <span class="nw">%s</span>' % dl(d.get('id')) if d.get('id') else '')
        for d in decided) if decided else '',
        ('%d still open, listed under Open for the SA.' % len(open_)) if open_ else None)
    sec('today', 'Today and after', table(['Area', 'Today', 'After this build'],
        [[md(x.get('area')), md(x.get('today')), md(x.get('after'))] for x in c.get('today') or []]))
    objs = [r for r in allrows if r['type'] == 'CustomObject']
    children = {}
    for r in allrows:
        if r['type'] == 'CustomField' and (r.get('details') or '').startswith('Master-detail'):
            m = re.match(r'Master-detail to (\w+)', r['details'])
            if m:
                children.setdefault(m.group(1), []).append(r['member'].split('.')[0])
    sec('data-model', 'Data model', erd(rows, c) + table(['Object', 'Relationships', 'Notes'],
        [['%s<br>%s' % (E(r.get('label') or r['member']), api(r['member'])),
          '<br>'.join(['%s %s' % (api(x['member'].split('.', 1)[1]), E((x.get('details') or '').split(';')[0].replace('Lookup to', '→').replace('Master-detail to', '⇒')))
                       for x in allrows if x['type'] == 'CustomField' and x['member'].startswith(r['member'] + '.') and re.match(r'(Lookup|Master-detail) to', x.get('details') or '')]
                      + ['Parent of %s' % api(ch) for ch in children.get(r['member'], [])]) or '<span class="muted">None</span>',
          md(r.get('why') or '') + ('<div class="muted">%s</div>' % E(r.get('details')) if r.get('details') else '')] for r in objs], 'objt'))
    smap = c.get('solution_map') or []
    if smap:
        epics = []
        for m in smap:
            for e in m.get('epics') or {}:
                if e not in epics:
                    epics.append(e)
        sec('solution-map', 'Across the whole solution', table(['Object'] + epics + ['Automation owner'],
            [[api(m.get('object') or '')] + [md((m.get('epics') or {}).get(e, '')) for e in epics] + [md(m.get('owner') or '')] for m in smap], 'smap'),
            'Every epic that uses the objects in this build, from the design\'s Solution map. This build takes only what its stories need, in the shape the later epics need.')
    sec('flows', 'How it works', ''.join(
        '<h3>%s</h3>%s%s' % (md(f.get('name')), flow_svg(f, i),
            table(['When', 'What happens'], [[md(o.get('when')), md(o.get('then'))] for o in f.get('outcomes') or []], 'two'))
        for i, f in enumerate(c.get('flows') or [])))
    autos = c.get('automation') or []
    sec('automation', 'Automation', table(['Automation', 'Type', 'Runs when', 'What it does', 'Beside it on the same object and moment'],
        [['%s<div class="muted">%s</div>' % (api(a.get('name') or ''), E(rows.get('Flow/' + (a.get('name') or ''), {}).get('status') or a.get('status') or ('Existing' if 'xisting' in (a.get('type') or '') else 'Planned'))),
          E(a.get('type')), md(a.get('runs_when')), md(a.get('does')), md(a.get('beside') or 'Nothing')] for a in autos], 'auto'))
    sec('pages', 'Pages, layouts and actions', table(['Page or action', 'Object', 'What the user sees'],
        [[md(p.get('name')), api(p.get('object') or ''), md(p.get('shows'))] for p in c.get('pages') or []]))
    ps = [r for r in allrows if r['type'] == 'PermissionSet' and r.get('objects')]
    acc = '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(a) for a in c.get('access') or []) if c.get('access') else ''
    if ps:
        pobjs = sorted({o for r in ps for o, _ in r['objects']})
        acc += table(['Object'] + [r.get('label') or r['member'] for r in ps],
                     [[api(o)] + [E(' '.join({'C': 'Create', 'R': 'Read', 'E': 'Edit', 'D': 'Delete'}[l] for l in dict(r['objects']).get(o, '')) or 'None') for r in ps] for o in pobjs], 'mx')
        newf = [r['member'] for r in allrows if r['type'] == 'CustomField' and r['change'] == 'New' and r['status'] in ('Built', 'Merged')]
        if newf:
            acc += table(['New field'] + [r.get('label') or r['member'] for r in ps],
                         [[api(f)] + [(lambda v: E(v) if v else '<span class="wt">None</span>')(dict(r.get('fields') or []).get(f, '')) for r in ps] for f in newf], 'mx')
        acc += '<p class="muted">From the permission set files in the repo.</p>'
    sec('access', 'Who can do what', acc)
    sec('reporting', 'Reporting', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(x) for x in c.get('reporting') or []) if c.get('reporting') else '')

    byobj = {}
    for r in allrows:
        o = obj_of(r) or ('Access' if group_of(r['type']) == 'Access' else 'Reporting' if group_of(r['type']) == 'Reporting' else 'Other')
        byobj.setdefault(o, []).append(r)
    order = sorted(byobj, key=lambda o: (o in ('Access', 'Reporting', 'Other'), not any(x['type'] == 'CustomObject' and x['change'] == 'New' for x in byobj[o]), o))
    inv = []
    for o in order:
        items = sorted(byobj[o], key=lambda r: (ORDER_IN_OBJ.index(r['type']) if r['type'] in ORDER_IN_OBJ else 99, r['member'].lower()))
        lab = next((x.get('label') for x in items if x['type'] == 'CustomObject' and x.get('label')), None) or (o.replace('__c', '').replace('_', ' ') if o not in ('Access', 'Reporting', 'Other') else o)
        inv.append('<tr class="gh" data-o="%s"><td colspan="5">%s%s</td></tr>' % (E(o), E(lab), ' <span class="muted">%s</span>' % api(o) if o not in ('Access', 'Reporting', 'Other') else ''))
        for r in items:
            label = r.get('label')
            nm = r['member'].split('.', 1)[1] if '.' in r['member'] and r['type'] != 'Report' else r['member']
            name = ('%s<br>' % E(label) if label and label != r['member'] else '') + api(nm)
            trace = ' · '.join('<span class="nw">%s</span>' % x for x in [jl(r['story']) if r.get('story') else '', E(r.get('task') or ''), dl(r['decision']) if r.get('decision') else ''] if x)
            det = md(r.get('why') or '') + ('<div class="muted">%s</div>' % md(r['details']) if r.get('details') and r.get('why') else md(r.get('details') or '') if not r.get('why') else '')
            st = r['status'] + (' on ' + r['waits'] if r.get('waits') else '')
            inv.append('<tr data-g="%s" data-c="%s" data-s="%s" data-o="%s"><td>%s</td><td>%s%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                E(group_of(r['type'])), E(r['change']), E(r['status']), E(o), name, E(FRIENDLY.get(r['type'], r['type'])),
                '' if r['change'] == 'New' else ', <span class="wt">%s</span>' % E(r['change'].lower()), det, trace or '<span class="wt">Not in the plan</span>', plain_chip(st)))
    filt = '<div class="filt">%s%s<input id="q" type="search" placeholder="Search"></div>' % (
        '<select id="fg" aria-label="Kind"><option value="">Every kind</option>%s</select>' % ''.join('<option>%s</option>' % E(g) for g, _ in GROUPS),
        '<select id="fs" aria-label="Status"><option value="">Any status</option><option>Planned</option><option>Waits</option><option>Built</option><option>Merged</option></select>')
    sec('components', 'Fields, objects and settings', filt + '<div class="tw"><table id="inv"><colgroup><col style="width:24%%"><col style="width:14%%"><col><col style="width:17%%"><col style="width:11%%"></colgroup><thead><tr><th>Component</th><th>Type</th><th>Details</th><th>Story, task, decision</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(inv) if allrows else '',
        'Every component this build creates or changes, by object. Built ones are described from their metadata files; the rest from the build plan.')
    changed = [r for r in allrows if r['change'] in ('Changed', 'Removed')]
    sec('changes', 'Changes to what is already in the org', table(['Component', 'Change', 'What changes, and what depends on it'],
        [[api('%s/%s' % (r['type'], r['member'])), E(r['change']) + (', by hand' if r['change'] == 'Removed' else ''), md(r.get('why') or r.get('details') or '')] for r in changed]))
    sec('build', 'The build', table(['Task', 'Story', 'Holds', 'Waits on', 'Status'],
        [[E(x.get('id')), jl(x.get('story')), md(x.get('holds')), md(x.get('waits') or 'Nothing'),
          plain_chip(x.get('status', 'Planned')) + (' · <a href="%s">pull request</a>' % E(x['pr']) if x.get('pr') else '')] for x in c.get('tasks') or []]))
    sec('open-questions', 'Open questions', table(['#', 'Question', 'Owner', 'Blocks'],
        [[E(q.get('n')), md(q.get('q')), E(q.get('owner')), md(q.get('blocks'))] for q in c.get('open_questions') or []]))
    sec('checks', 'Verification items', '<ol>%s</ol>' % ''.join('<li>%s</li>' % md(v) for v in c.get('checks') or []) if c.get('checks') else '',
        'What a person checks by hand in the sandbox before the work is merged.')
    sec('not-built', 'Not built', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(v) for v in c.get('not_built') or []) if c.get('not_built') else '')
    sec('sources', 'Sources', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(v) for v in c.get('sources') or []) if c.get('sources') else '')
    sec('change-log', 'Change log', table(['Date', 'Change'], [[E(x.get('date')), md(x.get('change'))] for x in c.get('changelog') or []], 'two'))

    st_ = [(k, count(lambda r, k=k: r['status'] == k)) for k in ('Merged', 'Built', 'Planned', 'Waits')]
    statline = '%d components: %s.' % (len(allrows), ', '.join('%d %s' % (v, k.lower() if k != 'Waits' else 'waiting') for k, v in st_ if v)) if allrows else ''
    openline = ('<a href="#open">%d item%s open for the SA</a>' % (len(openrows), '' if len(openrows) == 1 else 's')) if openrows else 'Nothing open for the SA'
    head = ('<header>%s<div class="eyebrow">Design and build review · %s</div><h1>%s</h1>'
            '<p class="meta">%s</p><p class="lede">%s</p><p class="status">%s %s</p></header>') % (
        logo(), E(c.get('client')), E(c.get('title') or 'Design and build review'),
        ' · '.join(md(x) for x in [c.get('status'), 'SA: ' + c['sa'] if c.get('sa') else '', 'as of ' + (c.get('as_of') or str(date.today())), c.get('links')] if x),
        md(c.get('summary')), E(statline), openline)
    return TEMPLATE.replace('%%TITLE%%', E('%s · %s' % (c.get('client'), c.get('title') or 'Design and build review'))).replace(
        '%%NAV%%', ''.join(nav)).replace('%%HEAD%%', head).replace('%%BODY%%', ''.join(body))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<style>
:root{--fg:#37352f;--ink:#03355e;--muted:#787774;--line:#e9e9e7;--soft:#f7f7f5;--blue:#0071b9;--warn:#b5532f;--bg:#fff}
@media (prefers-color-scheme:dark){:root{--fg:#e3e2e0;--ink:#ffffff;--muted:#9b9a97;--line:#373737;--soft:#252525;--blue:#5aa9e6;--warn:#e8906f;--bg:#191919}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.wrap{display:grid;grid-template-columns:220px minmax(0,1fr);max-width:1240px;margin:0 auto}
nav{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:56px 12px 40px 24px;font-size:13.5px}
nav a{display:block;color:var(--muted);text-decoration:none;padding:3px 8px;border-radius:4px;line-height:1.4}nav a:hover{background:var(--soft);color:var(--fg)}
nav a.cur{color:var(--fg);background:var(--soft)}
main{padding:48px 48px 120px 24px;min-width:0;max-width:1000px}
header{margin-bottom:8px}.logo{height:18px;width:auto;display:block;margin-bottom:28px}.wordmark{font-weight:700;color:var(--ink);display:block;margin-bottom:24px}
.eyebrow{font-size:13px;color:var(--muted)}h1{font-size:32px;line-height:1.2;margin:4px 0 6px;color:var(--ink);font-weight:700}
.meta{color:var(--muted);font-size:14px;margin:0 0 16px}.lede{font-size:17px;margin:0 0 12px}
.status{font-size:14px;color:var(--muted);padding:10px 14px;background:var(--soft);border-radius:6px;margin:0}
section{padding-top:28px;scroll-margin-top:16px}h2{font-size:22px;color:var(--ink);margin:0 0 6px;font-weight:600;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:17px;color:var(--fg);margin:20px 0 6px;font-weight:600}.sl{color:var(--muted);font-size:14.5px;margin:6px 0 10px}.muted{color:var(--muted)}
.nw{white-space:nowrap}a{color:var(--blue)}.wt{color:var(--warn)}.sv{color:var(--fg)}
.tw{overflow-x:auto;margin:8px 0}table{border-collapse:collapse;width:100%;font-size:14.5px}
th{text-align:left;font-weight:600;color:var(--muted);font-size:13px;padding:7px 10px;border-bottom:1px solid var(--line);background:var(--soft)}
td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
table.two td:first-child{width:32%}table.objt td:first-child,table.auto td:first-child{width:26%}table.open td:first-child{width:56px}table.open td:nth-child(2){width:130px;color:var(--muted)}
code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--fg);background:rgba(135,131,120,.13);padding:1px 4px;border-radius:3px}
.rules{padding-left:22px}.rules li{margin:8px 0}
.fig{margin:10px 0 4px;border:1px solid var(--line);border-radius:6px;padding:14px;overflow-x:auto}
figcaption{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:13px;color:var(--muted);margin-top:10px}
.key i.kb{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;vertical-align:-1px;border:1.5px solid}
.dia{width:100%;height:auto;display:block}.dia text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:var(--fg)}
.dl{font-size:10.5px;font-weight:600;letter-spacing:.06em;fill:var(--muted)!important}
.erd .box{fill:var(--bg);stroke:var(--line);stroke-width:1.2}.erd .hd{fill:var(--soft)}.erd .bn .box{stroke:var(--blue);stroke-width:1.5}
.erd .bc .box{stroke:var(--warn);stroke-width:1.5}.erd .bt{font-size:14px;font-weight:600}.erd .bs{font:11px ui-monospace,Menlo,monospace;fill:var(--muted)!important}
.erd .tg{font-size:9.5px;font-weight:600;letter-spacing:.06em;fill:var(--muted)!important}
.erd .fn{font:12px ui-monospace,Menlo,monospace}.erd .fw{fill:var(--muted)!important;font-style:italic}.erd .ft,.erd .fe{font-size:11.5px;fill:var(--muted)!important}.erd .fe{font-style:italic}
.erd .fm{font-size:13px;font-weight:700;fill:var(--muted)!important}
.rel{fill:none;stroke:var(--muted);stroke-width:1.2}.rel.md{stroke:var(--fg);stroke-width:1.8}
.erd .bl .box{stroke-dasharray:5 4}.key .kb.bl{border-style:dashed;border-color:var(--muted)}.key .kb.bn{border-color:var(--blue)}.key .kb.bc{border-color:var(--warn)}.key .kb.be{border-color:var(--line)}
.flow rect{stroke-width:1.2;fill:var(--bg);stroke:var(--line)}.flow .fs rect{fill:var(--soft)}
.flow .nb{fill:var(--muted)}.flow .nt{font-size:11px;font-weight:700;fill:var(--bg)!important}
.flow .ac{font-size:10.5px;font-weight:600;letter-spacing:.05em;fill:var(--muted)!important}.flow .st2{font-size:13.5px}.flow .fl{stroke:var(--muted);stroke-width:1.3}.flow .ah{fill:var(--muted)}
.key .kb.fp{border-color:var(--line)}.key .kb.fs{border-color:var(--line);background:var(--soft)}
.filt{display:flex;gap:8px;margin:6px 0 8px}.filt select,.filt input{font:inherit;font-size:14px;padding:5px 8px;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--fg)}.filt input{flex:1}
#inv{table-layout:fixed}#inv td{overflow-wrap:anywhere}tr.gh td{padding:16px 10px 6px;border-bottom:1px solid var(--line);font-weight:600}tr.gh code{font-size:14px}
table.mx td,table.mx th{white-space:nowrap}
@media (max-width:900px){.wrap{grid-template-columns:1fr}nav{display:none}main{padding:28px 20px 80px}}
@media print{nav,.filt{display:none}.wrap{grid-template-columns:1fr}}
</style></head><body>
<div class="wrap"><nav aria-label="Sections">%%NAV%%</nav><main>%%HEAD%%%%BODY%%</main></div>
<script>
(function(){var g=document.getElementById('fg'),s=document.getElementById('fs'),q=document.getElementById('q');
if(g){function f(){var t=(q.value||'').toLowerCase(),shown={};document.querySelectorAll('#inv tbody tr:not(.gh)').forEach(function(r){
var ok=(!g.value||r.dataset.g===g.value)&&(!s.value||r.dataset.s===s.value)&&(!t||r.textContent.toLowerCase().indexOf(t)>-1);r.style.display=ok?'':'none';if(ok)shown[r.dataset.o]=1});
document.querySelectorAll('#inv tr.gh').forEach(function(h){h.style.display=shown[h.dataset.o]?'':'none'})}
[g,s].forEach(function(e){e.addEventListener('change',f)});q.addEventListener('input',f)}
var links=[].slice.call(document.querySelectorAll('nav a'));if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('cur',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-10% 0px -80% 0px'});
document.querySelectorAll('main section').forEach(function(sec){io.observe(sec)})}})();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--content', required=True)
    ap.add_argument('--base')
    ap.add_argument('--head', action='append', default=[])
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    c = json.load(open(a.content, encoding='utf-8'))
    rows = inventory(a.base, a.head) if a.base and a.head else {}
    if a.base and a.head:
        c['_flows'] = {'%s|%s' % k: v for k, v in all_flows(a.head[0]).items()}
    open(a.out, 'w', encoding='utf-8').write(page(c, rows))
    print('wrote %s · %d components from the repo, %d planned in content' % (a.out, len(rows), len(c.get('planned') or [])))


if __name__ == '__main__':
    main()
