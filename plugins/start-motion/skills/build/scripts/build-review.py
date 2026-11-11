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
            out.append('<path d="%s" class="rel%s" marker-end="url(#one)"%s/>' % (d, ' md' if f['md'] else '', ' stroke-dasharray="4 3"' if f['change'] == 'Removed' else ''))
    for o, (x, y) in pos.items():
        e, h = ents[o], hgt(o)
        cls = {'New': 'bn', 'Changed': 'bc'}.get(e['state'], 'be')
        tag = {'New': 'NEW', 'Changed': 'CHANGED'}.get(e['state'], 'STANDARD' if not o.endswith('__c') else 'EXISTING')
        out.append('<g class="%s"><rect x="%d" y="%d" width="%d" height="%d" rx="6" class="box"/><rect x="%d" y="%d" width="%d" height="%d" rx="6" class="hd"/><rect x="%d" y="%d" width="%d" height="8" class="hd"/>' % (cls, x, y, BW, h, x, y, BW, HH - 6, x, y + HH - 14, BW))
        out.append('<text x="%d" y="%d" class="bt">%s</text><text x="%d" y="%d" class="bs">%s</text><text x="%d" y="%d" class="tg" text-anchor="end">%s</text>' % (
            x + 10, y + 18, E(e['label'][:24]), x + 10, y + 32, E(o[:34]), x + BW - 10, y + 18, tag))
        fl = e['fields']
        if not fl:
            out.append('<text x="%d" y="%d" class="fe">no new fields</text>' % (x + 10, y + HH + 14))
        for i, f in enumerate(fl[:MAXF]):
            fy = y + HH + i * RH + 14
            mark = {'New': '+', 'Changed': '~', 'Removed': '−'}.get(f['change'], '')
            out.append('<text x="%d" y="%d" class="fm %s">%s</text><text x="%d" y="%d" class="fn%s">%s</text><text x="%d" y="%d" class="ft" text-anchor="end">%s</text>' % (
                x + 10, fy, {'New': 'pn', 'Changed': 'pc', 'Removed': 'pr'}.get(f['change'], ''), mark, x + 22, fy,
                ' fw' if f['status'] in ('Planned', 'Waits') else '', E(f['name'] if len(f['name']) <= 27 else f['name'][:25] + '…'), x + BW - 10, fy, E(f['type'][:16])))
        if len(fl) > MAXF:
            out.append('<text x="%d" y="%d" class="fe">and %d more, in Every component</text>' % (x + 22, y + HH + MAXF * RH + 14, len(fl) - MAXF))
        out.append('</g>')
    out.append('</svg>')
    return ('<figure class="fig">%s<figcaption><span class="key"><i class="kb bn"></i>New object</span><span class="key"><i class="kb bc"></i>Changed</span>'
            '<span class="key"><i class="kb be"></i>Existing or standard</span><span class="key">+ new field · ~ changed field · grey: not built yet</span>'
            '<span class="key">→ lookup · ⇒ master-detail; each line runs from the relationship field to its parent</span></figcaption></figure>') % ''.join(out)


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
    return '<figure class="fig">%s<figcaption><span class="key"><i class="kb fp"></i>Done by a person</span><span class="key"><i class="kb fs"></i>Done by the system</span></figcaption></figure>' % ''.join(out)


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
    for p in (os.path.join(here, '..', '..', 'kickoff', 'brand', 'logo-inverse.svg'), os.path.join(here, '..', 'skills', 'kickoff', 'brand', 'logo-inverse.svg')):
        if os.path.exists(p):
            svg = open(p, encoding='utf-8').read()
            return svg.replace('<svg ', '<svg class="logo" role="img" aria-label="Kicksaw" ', 1)
    return '<span class="wordmark">kicksaw</span>'


NEED_ORDER = {'SA call': 0, 'Decide': 0, 'Found in the build': 1, 'Removes': 2, 'Changes what exists': 3, 'Confirm': 4, 'Review': 5}
NEED_CLS = {'SA call': 'nd', 'Decide': 'nd', 'Found in the build': 'nf', 'Removes': 'nf', 'Changes what exists': 'nx', 'Confirm': 'nc', 'Review': 'nc'}


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
        found.insert(0, '%d new field%s that no permission set in this build grants, so only administrators will see %s: %s.' % (
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
    need = list(c.get('needs_you') or []) + [{'kind': 'Found in the build', 'text': f} for f in found[:25]]
    need.sort(key=lambda n: NEED_ORDER.get(n.get('kind'), 9))

    groups, body = [], []
    cur = []

    def group(title):
        groups.append((title, []))

    def sec(anchor, title, inner, badge=None, lede=None):
        if not inner:
            return
        groups[-1][1].append('<a href="#%s">%s%s</a>' % (anchor, E(title), '<span class="nbg">%s</span>' % badge if badge else ''))
        body.append('<section id="%s"><h2>%s</h2>%s%s</section>' % (anchor, E(title), '<p class="sl">%s</p>' % lede if lede else '', inner))

    group('Review')
    sec('needs-you', 'Needs you', ''.join(
        '<div class="need %s"><div class="nk">%s</div><div class="nt2">%s%s</div></div>' % (
            NEED_CLS.get(n.get('kind'), 'nc'), E(n.get('kind')), md(n.get('text')),
            ' <a href="%s">Open</a>' % E(n['link']) if n.get('link') else '') for n in need) if need else
        '<p class="muted">Nothing is waiting on the SA.</p>', len(need) or None, 'Decisions to make first, then anything the page found on its own, then what to confirm and review.')
    sec('rules', 'Decisions that shape the design', '<ol class="rules">%s</ol>' % ''.join(
        '<li><div class="rl">%s</div><div class="rw">%s</div><div class="rb">%s · %s%s</div></li>' % (md(r.get('rule')), md(r.get('why')), dl(r.get('id')),
            E(r.get('by')), ', ' + E(r.get('date')) if r.get('date') else '') for r in c.get('rules') or []) if c.get('rules') else '',
        None, 'Every decided row from the Decisions tab that this build stands on.')
    sec('stories', 'Stories this serves', table(['Story', 'What the design gives it'],
        [[jl(s.get('key')) + ' ' + md(s.get('title')), md(s.get('gives'))] for s in c.get('stories') or []], 'two'))
    sec('differences', 'Where the design differs from the stories', table(['#', 'Story says', 'The design does', 'Recommendation'],
        [[E(d.get('n')), md(d.get('says')), md(d.get('does')), md(d.get('rec'))] for d in c.get('differences') or []]),
        len(c.get('differences') or []) or None)

    group('Design')
    sec('today', 'Today and after', table(['Area', 'Today', 'After this build'],
        [[md(x.get('area')), md(x.get('today')), md(x.get('after'))] for x in c.get('today') or []]))
    objs = [r for r in allrows if r['type'] == 'CustomObject']
    children = {}
    for r in allrows:
        if r['type'] == 'CustomField' and (r.get('details') or '').startswith('Master-detail'):
            m = re.match(r'Master-detail to (\w+)', r['details'])
            if m:
                children.setdefault(m.group(1), []).append(r['member'].split('.')[0])
    sec('data-model', 'Data model', erd(rows, c) + table(['Object', 'Change', 'Relationships', 'Settings and notes'],
        [['<b>%s</b><br>%s' % (E(r.get('label') or r['member']), api(r['member'])), chip(r['change']),
          '<br>'.join(['%s %s' % (api(x['member'].split('.', 1)[1]), E((x.get('details') or '').split(';')[0].replace('Lookup to', '→').replace('Master-detail to', '⇒'))) for x in allrows if x['type'] == 'CustomField' and x['member'].startswith(r['member'] + '.') and
                       re.match(r'(Lookup|Master-detail) to', x.get('details') or '')] + ['Parent of %s ⇒' % api(ch) for ch in children.get(r['member'], [])]) or '<span class="muted">None</span>',
          md(r.get('why') or '') + ('<div class="muted">%s</div>' % E(r.get('details')) if r.get('details') else '')] for r in objs], 'objt'))
    flows = c.get('flows') or []
    sec('flows', 'How it works', ''.join(
        '<h3>%s</h3>%s%s' % (md(f.get('name')), flow_svg(f, i),
            table(['When', 'What happens'], [[md(o.get('when')), md(o.get('then'))] for o in f.get('outcomes') or []], 'two'))
        for i, f in enumerate(flows)))
    autos = c.get('automation') or []
    sec('automation', 'Automation', table(['Automation', 'Runs when', 'What it does', 'Beside it on the same object and moment', 'Status'],
        [['<b>%s</b><br>%s<div class="muted">%s</div>' % (E((a.get('name') or '').replace('_', ' ')), api(a.get('name') or ''), E(a.get('type'))),
          md(a.get('runs_when')), md(a.get('does')), md(a.get('beside') or 'Nothing'),
          chip(rows.get('Flow/' + (a.get('name') or ''), {}).get('status') or a.get('status') or ('Existing' if 'xisting' in (a.get('type') or '') else 'Planned'))]
         for a in autos] or
        [['%s' % api(a['member']), E(a.get('trigger')), md(a.get('details')), '', chip(a['status'])] for a in allrows if group_of(a['type']) == 'Automation'], 'auto'))
    sec('pages', 'Pages, layouts and actions', table(['Page or action', 'Object', 'What the user sees'],
        [[md(p.get('name')), api(p.get('object') or ''), md(p.get('shows'))] for p in c.get('pages') or []]))
    ps = [r for r in allrows if r['type'] == 'PermissionSet' and r.get('objects')]
    acc = '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(a) for a in c.get('access') or []) if c.get('access') else ''
    if ps:
        pobjs = sorted({o for r in ps for o, _ in r['objects']})
        cell = lambda v: '<span class="cr2">%s</span>' % ' '.join('<i class="%s">%s</i>' % ('on' if l in v else 'off', l) for l in 'CRED')
        acc += '<h3>Objects</h3>' + table(['Object'] + [r.get('label') or r['member'] for r in ps], [[api(o)] + [cell(dict(r['objects']).get(o, '')) for r in ps] for o in pobjs], 'mx')
        newf = [r['member'] for r in allrows if r['type'] == 'CustomField' and r['change'] == 'New' and r['status'] in ('Built', 'Merged')]
        if newf:
            acc += '<h3>New fields</h3>' + table(['Field'] + [r.get('label') or r['member'] for r in ps],
                [[api(f)] + [(lambda v: '<span class="fa %s">%s</span>' % ('on' if v else 'off', v or 'No access'))(dict(r.get('fields') or []).get(f, '')) for r in ps] for f in newf], 'mx')
        acc += '<p class="muted">Read from the permission set files in the repo. C create, R read, E edit, D delete.</p>'
    sec('access', 'Who can do what', acc)
    sec('reporting', 'Reporting', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(x) for x in c.get('reporting') or []) if c.get('reporting') else '')

    group('Build')
    # every component, grouped by the object it belongs to
    byobj = {}
    for r in allrows:
        o = obj_of(r) or ('Access' if group_of(r['type']) == 'Access' else 'Reporting' if group_of(r['type']) == 'Reporting' else 'Other')
        byobj.setdefault(o, []).append(r)
    order = sorted(byobj, key=lambda o: (o in ('Access', 'Reporting', 'Other'), not any(x['type'] == 'CustomObject' and x['change'] == 'New' for x in byobj[o]), o))
    inv = []
    for o in order:
        items = sorted(byobj[o], key=lambda r: (ORDER_IN_OBJ.index(r['type']) if r['type'] in ORDER_IN_OBJ else 99, r['member'].lower()))
        n_new = sum(1 for r in items if r['change'] == 'New')
        inv.append('<tr class="gh" data-o="%s"><td colspan="5"><span class="gho">%s</span> <span class="muted">%d component%s · %d new</span></td></tr>' % (
            E(o), api(o) if o not in ('Access', 'Reporting', 'Other') else E(o), len(items), '' if len(items) == 1 else 's', n_new))
        for r in items:
            label = r.get('label')
            nm = r['member'].split('.', 1)[1] if '.' in r['member'] and r['type'] != 'Report' else r['member']
            name = ('<b>%s</b><br>' % E(label) if label and label != r['member'] else '') + api(nm)
            trace = ' · '.join(x for x in [jl(r['story']) if r.get('story') else '', E(r.get('task') or ''), dl(r['decision']) if r.get('decision') else ''] if x)
            det = md(r.get('why') or '') + ('<div class="muted">%s</div>' % md(r['details']) if r.get('details') and r.get('why') else md(r.get('details') or '') if not r.get('why') else '')
            inv.append('<tr data-g="%s" data-c="%s" data-s="%s" data-o="%s"><td>%s<div class="ty">%s</div></td><td>%s</td><td>%s</td><td class="trc">%s</td><td>%s%s</td></tr>' % (
                E(group_of(r['type'])), E(r['change']), E(r['status']), E(o), name, E(FRIENDLY.get(r['type'], r['type'])), chip(r['change']),
                det, trace or '<span class="muted">Not in the plan</span>', chip(r['status']), '<div class="muted">waits on %s</div>' % E(r['waits']) if r.get('waits') else ''))
    filt = '<div class="filt">%s%s%s<input id="q" type="search" placeholder="Search names, types and details"></div>' % (
        '<select id="fg" aria-label="Kind"><option value="">Every kind</option>%s</select>' % ''.join('<option>%s</option>' % E(g) for g, _ in GROUPS),
        '<select id="fc" aria-label="Change"><option value="">New, changed and removed</option><option>New</option><option>Changed</option><option>Removed</option></select>',
        '<select id="fs" aria-label="Status"><option value="">Any status</option><option>Planned</option><option>Waits</option><option>Built</option><option>Merged</option></select>')
    st_ = {k: count(lambda r, k=k: r['status'] == k) for k in ('Merged', 'Built', 'Planned', 'Waits')}
    sec('inventory', 'Every component', filt + '<div class="tw"><table id="inv"><colgroup><col style="width:27%%"><col style="width:9%%"><col><col style="width:16%%"><col style="width:10%%"></colgroup><thead><tr><th>Component</th><th>Change</th><th>Details</th><th>Story · task · decision</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(inv) if allrows else '',
        len(allrows), 'Grouped by object. Built and merged components are described from their metadata files; the rest from the build plan.')
    changed = [r for r in allrows if r['change'] in ('Changed', 'Removed')]
    sec('changes', 'Changes to what is already in the org', table(['Component', 'Change', 'What changes, and what depends on it', 'Done by'],
        [[api('%s/%s' % (r['type'], r['member'])), chip(r['change']), md(r.get('why') or r.get('details') or ''),
          'A person, by hand' if r['change'] == 'Removed' else 'The build'] for r in changed]), len(changed) or None)
    sec('build', 'Build tasks', table(['Task', 'Story', 'Holds', 'Waits on', 'Status'],
        [['<b>%s</b>' % E(x.get('id')), jl(x.get('story')), md(x.get('holds')), md(x.get('waits') or 'Nothing'),
          chip(x.get('status', 'Planned')) + (' <a href="%s">Pull request</a>' % E(x['pr']) if x.get('pr') else '')] for x in c.get('tasks') or []]))
    sec('checks', 'Checks a person makes in the sandbox', '<ol class="checks">%s</ol>' % ''.join('<li>%s</li>' % md(v) for v in c.get('checks') or []) if c.get('checks') else '')

    group('Reference')
    sec('open-questions', 'Open questions', table(['#', 'Question', 'Owner', 'Blocks'],
        [[E(q.get('n')), md(q.get('q')), E(q.get('owner')), md(q.get('blocks'))] for q in c.get('open_questions') or []]))
    sec('not-built', 'Not built', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(v) for v in c.get('not_built') or []) if c.get('not_built') else '')
    sec('sources', 'Sources', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(v) for v in c.get('sources') or []) if c.get('sources') else '')
    sec('change-log', 'Change log', table(['Date', 'Change'], [[E(x.get('date')), md(x.get('change'))] for x in c.get('changelog') or []], 'two'))

    nav = ''.join('<div class="ng"><div class="ngt">%s</div>%s</div>' % (E(t), ''.join(links)) for t, links in groups if links)
    total = max(1, len(allrows))
    bar = ''.join('<i class="%s" style="width:%.2f%%" title="%s: %d"></i>' % (k.lower(), 100.0 * v / total, k, v) for k, v in st_.items() if v)
    legend = ''.join('<span><i class="%s"></i>%s %d</span>' % (k.lower(), k, v) for k, v in st_.items() if v)
    stats = [('New objects', count(lambda r: r['type'] == 'CustomObject' and r['change'] == 'New')),
             ('New fields', count(lambda r: r['type'] == 'CustomField' and r['change'] == 'New')),
             ('Automation', count(lambda r: group_of(r['type']) == 'Automation')),
             ('Pages and actions', count(lambda r: group_of(r['type']) == 'Pages and actions')),
             ('Changes to what exists', count(lambda r: r['change'] == 'Changed')),
             ('Removals', count(lambda r: r['change'] == 'Removed'))]
    statbox = ''.join('<div class="st"><div class="sn">%d</div><div class="sl">%s</div></div>' % (b, E(a)) for a, b in stats)
    band = ('<header class="band"><div class="bi">%s<div class="eyebrow">Design and build review · %s</div><h1>%s</h1><div class="rule"></div>'
            '<p class="meta">%s</p></div></header>') % (
        logo(), E(c.get('client')), E(c.get('title') or 'Design and build review'),
        ' · '.join(md(x) for x in [c.get('status'), 'SA: ' + c['sa'] if c.get('sa') else '', 'as of ' + (c.get('as_of') or str(date.today())), c.get('links')] if x))
    head = ('<div class="intro"><p class="lede">%s</p><div class="stats">%s</div>'
            '<div class="prog"><div class="bar">%s</div><div class="lg">%s</div></div></div>') % (md(c.get('summary')), statbox, bar, legend)
    return TEMPLATE.replace('%%TITLE%%', E('%s · %s' % (c.get('client'), c.get('title') or 'Design and build review'))).replace(
        '%%NAV%%', nav).replace('%%HEAD_BAND%%', band).replace('%%HEAD%%', head).replace('%%BODY%%', ''.join(body))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--navy:#03355e;--cyan:#44c8f5;--blue:#0071b9;--orange:#dd6443;--charcoal:#414042;--muted:#676668;--card:#f4f4f4;--line:#d7d7d7;--soft:#e9f2f9;
--bg:#fff;--fg:#414042;--ink:#03355e;--panel:#fafafa;--grn:#2e7d32;--grnbg:#e6f2e6;--amb:#9a5b00;--ambbg:#fdf0dc;--red:#b23b22;--redbg:#fbe9e4;--cyanbg:#e3f6fd}
@media (prefers-color-scheme:dark){:root{--bg:#0d1b2a;--fg:#d9e2ec;--ink:#ffffff;--muted:#9fb3c8;--card:#13283d;--line:#22405e;--panel:#10233a;--soft:#13324f;
--grn:#8fd694;--grnbg:#173322;--amb:#f2c072;--ambbg:#3a2a10;--red:#f4a08a;--redbg:#3d1c14;--cyanbg:#0f3550}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 "Source Sans 3","Source Sans Pro",Arial,sans-serif}
h1,h2,h3,.eyebrow,.ngt,.sn,.nk,th{font-family:Inter,Arial,sans-serif}
.band{background:var(--navy);color:#fff;padding:28px 0 26px}.bi{max-width:1320px;margin:0 auto;padding:0 40px 0 320px}
.logo{height:26px;width:auto;display:block;margin-bottom:22px}.wordmark{font:700 22px Inter;color:#fff;display:block;margin-bottom:18px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--cyan)}
h1{font-size:30px;line-height:1.15;margin:6px 0 0;font-weight:700;color:#fff;letter-spacing:-.3px}
.rule{width:72px;height:5px;background:var(--orange);margin:14px 0 12px}
.band .meta{color:#b9d6ea;font-size:14px;margin:0}.band .meta a{color:#fff}
.wrap{display:grid;grid-template-columns:260px minmax(0,1fr);max-width:1320px;margin:0 auto}
nav{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:28px 18px 40px 40px;font-size:14px}
.ng{margin-bottom:18px}.ngt{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--blue);margin:0 0 6px 8px}
nav a{display:flex;justify-content:space-between;align-items:center;color:var(--fg);text-decoration:none;padding:4px 8px;border-radius:6px;line-height:1.35}
nav a:hover{background:var(--card)}nav a.cur{background:var(--soft);color:var(--ink);font-weight:600}
.nbg{font:600 11px Inter;background:var(--card);color:var(--muted);border-radius:10px;padding:1px 7px;margin-left:8px}
nav a[href="#needs-you"] .nbg{background:var(--orange);color:#fff}
main{padding:0 40px 100px 20px;min-width:0}
.intro{padding:24px 0 8px}.lede{font-size:18px;line-height:1.55;max-width:900px;margin:0 0 18px;color:var(--fg)}
.stats{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}
.st{background:var(--card);border-radius:8px;padding:10px 14px}.sn{font-size:26px;font-weight:700;color:var(--ink);line-height:1.1}.sl{font-size:13px;color:var(--muted)}
.prog{margin-top:14px}.bar{display:flex;height:8px;border-radius:4px;overflow:hidden;background:var(--card)}.bar i{display:block}
.lg{display:flex;gap:16px;font-size:13px;color:var(--muted);margin-top:6px}.lg i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
i.merged{background:#2e7d32}i.built{background:var(--cyan)}i.planned{background:#b8c4ce}i.waits{background:var(--orange)}
section{padding-top:30px;scroll-margin-top:12px}
h2{font-size:22px;font-weight:700;color:var(--ink);margin:0 0 4px;letter-spacing:-.2px}
h2::after{content:"";display:block;width:40px;height:3px;background:var(--orange);margin-top:8px}
h3{font-size:16px;font-weight:600;color:var(--ink);margin:22px 0 8px}
.sl{color:var(--muted);font-size:14px;margin:8px 0 12px}.muted{color:var(--muted)}
a{color:var(--blue)}@media (prefers-color-scheme:dark){a{color:var(--cyan)}}
.tw{overflow-x:auto;margin:10px 0}table{border-collapse:collapse;width:100%;font-size:14.5px}
th{text-align:left;font-size:12px;font-weight:600;color:var(--ink);background:var(--card);padding:9px 12px;border-bottom:1px solid var(--line)}
td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
table.two td:first-child{width:30%}
code{font:13px "JetBrains Mono",ui-monospace,Menlo,monospace;color:var(--ink);background:none;padding:0}
.chip{display:inline-block;font:600 11.5px Inter;padding:2px 9px;border-radius:10px;white-space:nowrap;background:var(--card);color:var(--muted)}
.cn{background:var(--soft);color:var(--blue)}.cc{background:var(--ambbg);color:var(--amb)}.cr{background:var(--redbg);color:var(--red)}
.cb{background:var(--cyanbg);color:var(--blue)}.cm{background:var(--grnbg);color:var(--grn)}.cw{background:var(--ambbg);color:var(--orange)}
.need{display:grid;grid-template-columns:150px minmax(0,1fr);gap:14px;padding:12px 16px;border:1px solid var(--line);border-left:4px solid var(--line);border-radius:0 8px 8px 0;margin:8px 0;background:var(--bg)}
.nk{font-size:12px;font-weight:600;padding-top:2px}.need.nd{border-left-color:var(--orange)}.need.nd .nk{color:var(--orange)}
.need.nf{border-left-color:var(--red);background:var(--redbg)}.need.nf .nk{color:var(--red)}
.need.nx{border-left-color:var(--amb)}.need.nx .nk{color:var(--amb)}.need.nc{border-left-color:var(--blue)}.need.nc .nk{color:var(--blue)}
.rules{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;counter-reset:r}
.rules li{background:var(--card);border-radius:8px;padding:14px 16px}.rl{font-weight:600;color:var(--ink)}.rw{margin-top:4px}.rb{margin-top:8px;font-size:13px;color:var(--muted)}
.fig{margin:14px 0 6px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px;overflow-x:auto}
figcaption{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:var(--muted);margin-top:12px}
.key i.kb{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px;border:1.5px solid}
.dia{width:100%;height:auto;display:block;color:var(--fg)}.dia text{font-family:Inter,Arial,sans-serif;fill:var(--fg)}
.dl{font-size:10.5px;font-weight:600;letter-spacing:.08em;fill:var(--muted)!important}
.erd .box{fill:var(--bg);stroke:var(--line);stroke-width:1.2}.erd .hd{fill:var(--card)}
.erd .bn .box{stroke:var(--blue);stroke-width:1.6}.erd .bn .hd{fill:var(--soft)}.erd .bc .box{stroke:var(--orange);stroke-width:1.6}.erd .bc .hd{fill:var(--ambbg)}
.erd .bt{font-size:14px;font-weight:600;fill:var(--ink)!important}.erd .bs{font:11px "JetBrains Mono",monospace;fill:var(--muted)!important}
.erd .tg{font-size:9.5px;font-weight:600;letter-spacing:.06em;fill:var(--muted)!important}.erd .bn .tg{fill:var(--blue)!important}.erd .bc .tg{fill:var(--orange)!important}
.erd .fn{font:12px "JetBrains Mono",monospace}.erd .fw{fill:var(--muted)!important;font-style:italic}.erd .ft{font-size:11.5px;fill:var(--muted)!important}.erd .fe{font-size:11.5px;fill:var(--muted)!important;font-style:italic}
.erd .fm{font-size:13px;font-weight:700}.erd .pn{fill:var(--blue)!important}.erd .pc{fill:var(--orange)!important}.erd .pr{fill:var(--red)!important}
.rel{fill:none;stroke:var(--muted);stroke-width:1.3}.rel.md{stroke:var(--ink);stroke-width:2}
.key .kb.bn{border-color:var(--blue);background:var(--soft)}.key .kb.bc{border-color:var(--orange);background:var(--ambbg)}.key .kb.be{border-color:var(--line);background:var(--card)}
.flow rect{stroke-width:1.3}.flow .fp rect{fill:var(--bg);stroke:var(--line)}.flow .fs rect{fill:var(--soft);stroke:var(--blue)}
.flow .nb{fill:var(--navy)}.flow .fs .nb{fill:var(--blue)}.flow .nt{font-size:11px;font-weight:700;fill:#fff!important}
.flow .ac{font-size:10.5px;font-weight:600;letter-spacing:.06em;fill:var(--muted)!important}.flow .fs .ac{fill:var(--blue)!important}
.flow .st2{font-size:13.5px}.flow .fl{stroke:var(--muted);stroke-width:1.5}.flow .ah{fill:var(--muted)}
.key .kb.fp{border-color:var(--line);background:var(--bg)}.key .kb.fs{border-color:var(--blue);background:var(--soft)}
table.objt td:first-child,table.auto td:first-child{width:26%}
.cr2 i{font:600 11px Inter;font-style:normal;display:inline-block;width:20px;text-align:center;border-radius:4px;padding:1px 0;margin-right:2px}
.cr2 i.on{background:var(--soft);color:var(--blue)}.cr2 i.off{color:var(--line)}
.fa{font:600 12px Inter}.fa.on{color:var(--grn)}.fa.off{color:var(--red)}
table.mx th:not(:first-child),table.mx td:not(:first-child){text-align:center}
.filt{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 10px;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:2}
.filt select,.filt input{font:inherit;font-size:14px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}
.filt input{flex:1;min-width:200px}
#inv{table-layout:fixed}#inv td{overflow-wrap:anywhere}
tr.gh td{background:var(--card);padding:9px 12px;border-top:12px solid var(--bg)}.gho code{font-weight:600;font-size:14px}
.ty{font-size:12.5px;color:var(--muted);margin-top:2px}.trc{font-size:13.5px}
.checks li{margin:6px 0}
@media (max-width:1000px){.wrap{grid-template-columns:1fr}nav{display:none}.bi{padding:0 22px}main{padding:0 22px 60px}.stats{grid-template-columns:repeat(3,1fr)}.need{grid-template-columns:1fr;gap:2px}}
@media print{nav,.filt{display:none}.wrap{grid-template-columns:1fr}.band{-webkit-print-color-adjust:exact;print-color-adjust:exact}.bi{padding:0 24px}section{break-inside:avoid-page}}
</style></head><body>%%HEAD_BAND%%
<div class="wrap"><nav aria-label="Sections">%%NAV%%</nav><main>%%HEAD%%%%BODY%%</main></div>
<script>
(function(){var g=document.getElementById('fg'),c=document.getElementById('fc'),s=document.getElementById('fs'),q=document.getElementById('q');
if(g){function f(){var t=(q.value||'').toLowerCase(),shown={};document.querySelectorAll('#inv tbody tr:not(.gh)').forEach(function(r){
var ok=(!g.value||r.dataset.g===g.value)&&(!c.value||r.dataset.c===c.value)&&(!s.value||r.dataset.s===s.value)&&(!t||r.textContent.toLowerCase().indexOf(t)>-1);r.style.display=ok?'':'none';if(ok)shown[r.dataset.o]=1});
document.querySelectorAll('#inv tr.gh').forEach(function(h){h.style.display=shown[h.dataset.o]?'':'none'})}
[g,c,s].forEach(function(e){e.addEventListener('change',f)});q.addEventListener('input',f)}
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
