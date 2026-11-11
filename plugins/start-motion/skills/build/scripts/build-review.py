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

def erd(rows, content):
    """Objects as boxes, parents left of children, each relationship drawn and labeled."""
    objs, edges = {}, []
    for r in rows.values():
        if r['type'] == 'CustomObject':
            objs.setdefault(r['member'], {'state': r['change'], 'label': r.get('label') or r['member'], 'n': 0})
    for r in rows.values():
        if r['type'] != 'CustomField':
            continue
        o, f = r['member'].split('.', 1)
        objs.setdefault(o, {'state': 'Existing', 'label': o, 'n': 0})
        if r['change'] == 'New':
            objs[o]['n'] += 1
        ref = r.get('ref')
        if not ref:
            m = re.match(r'(?i)(lookup|master-detail) to ([\w]+)', r.get('details') or '')
            ref = m.group(2) if m else None
        if ref:
            objs.setdefault(ref, {'state': 'Existing', 'label': ref, 'n': 0})
            md_ = (r.get('ftype') == 'MasterDetail') or (r.get('details') or '').lower().startswith('master-detail')
            edges.append((o, ref, ('master-detail' if md_ else 'lookup') + ' · ' + f.replace('__c', ''), r['change'] == 'Removed'))
    for o, info in (content.get('objects_extra') or {}).items():
        objs.setdefault(o, {'state': info.get('state', 'Existing'), 'label': info.get('label', o), 'n': 0})
    if not objs:
        return ''
    parents = {o: set() for o in objs}
    for c, p, _, _ in edges:
        if c != p:
            parents[c].add(p)
    level = {}

    def lv(o, seen=()):
        if o in level:
            return level[o]
        if o in seen:
            return 0
        level[o] = 0 if not parents[o] else 1 + max(lv(p, seen + (o,)) for p in parents[o])
        return level[o]
    for o in objs:
        lv(o)
    cols = {}
    for o in sorted(objs, key=lambda x: (objs[x]['state'] == 'Existing', x)):
        cols.setdefault(level[o], []).append(o)
    BW, BH, GX, GY, PAD = 190, 62, 200, 30, 16
    pos = {}
    for c, names in cols.items():
        for i, o in enumerate(names):
            pos[o] = (PAD + c * (BW + GX), PAD + 22 + i * (BH + GY))
    W = PAD * 2 + (max(cols) + 1) * BW + max(cols) * GX + 40
    H = PAD * 2 + 22 + max(len(v) for v in cols.values()) * (BH + GY)
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Data model: %d objects and how they relate" class="dia">' % (W, H, len(objs)),
           '<defs><marker id="crow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10" fill="none" stroke="currentColor"/></marker></defs>']
    for c in sorted(cols):
        out.append('<text x="%d" y="%d" class="dl">%s</text>' % (PAD + c * (BW + GX), PAD + 8, 'Parents' if c == 0 else 'Children, level %d' % c))
    # one line per child and parent pair, naming every field on it
    pairs = {}
    for c, p, lab, removed in edges:
        if c != p and c in pos and p in pos:
            k = pairs.setdefault((c, p), {'labs': [], 'removed': True})
            k['labs'].append(lab)
            k['removed'] = k['removed'] and removed
    by_child = {}
    for (c, p) in pairs:
        by_child.setdefault(c, []).append(p)
    by_parent = {}
    for (c, p) in pairs:
        by_parent.setdefault(p, []).append(c)
    for (c, p), k in pairs.items():
        (cx, cy), (px, py) = pos[c], pos[p]
        sibs = sorted(by_child[c], key=lambda q: pos[q][1])
        y1 = cy + 14 + (BH - 14) * (sibs.index(p) + 1) / (len(sibs) + 1)
        ins = sorted(by_parent[p], key=lambda q: pos[q][1])
        y2 = py + BH * (ins.index(c) + 1) / (len(ins) + 1)
        kind = k['labs'][0].split(' · ')[0]
        names = ', '.join(l.split(' · ', 1)[1] for l in k['labs'])
        dash = ' stroke-dasharray="4 3"' if k['removed'] else ''
        if cx > px:
            x1, x2 = cx, px + BW
            mx = x2 + 24 + 8 * ins.index(c)
            out.append('<path d="M%d,%d H%d V%d H%d" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#crow)"%s/>' % (x1, y1, mx, y2, x2, dash))
            out.append('<text x="%d" y="%d" class="el" text-anchor="end">%s: %s</text>' % (x1 - 6, y1 - 4, E(kind), E(names[:30])))
        else:  # same column or a loop back: route around the right side
            x1, x2 = cx + BW, px + BW
            mx = max(x1, x2) + 26
            out.append('<path d="M%d,%d H%d V%d H%d" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#crow)"%s/>' % (x1, y1, mx, y2, x2, dash))
            out.append('<text x="%d" y="%d" class="el">%s · %s</text>' % (mx + 4, (y1 + y2) / 2, E(kind), E(names[:30])))
    for o, (x, y) in pos.items():
        s = objs[o]['state']
        cls = {'New': 'bn', 'Changed': 'bc'}.get(s, 'be')
        sub = {'New': 'new object', 'Changed': 'changed'}.get(s, 'standard object' if not o.endswith('__c') else 'existing') + (' · %d new fields' % objs[o]['n'] if objs[o]['n'] else '')
        out.append('<g class="%s"><rect x="%d" y="%d" width="%d" height="%d" rx="6"/>'
                   '<text x="%d" y="%d" class="bt">%s</text><text x="%d" y="%d" class="bs">%s</text>'
                   '<text x="%d" y="%d" class="bs">%s</text></g>' % (
                       cls, x, y, BW, BH, x + 10, y + 19, E(objs[o]['label'][:26]), x + 10, y + 35, E(o[:30]), x + 10, y + 50, E(sub)))
    out.append('</svg>')
    return ('<figure>%s<figcaption>Each line runs from the child to the parent and names the relationship field. '
            'New objects are outlined in blue, changed ones in amber, existing ones in grey. A dashed line is a relationship being removed.</figcaption></figure>') % ''.join(out)


def flow_svg(flow, i):
    steps = flow.get('steps') or []
    if not steps:
        return ''
    per, BW, BH, GX, GY, PAD = 4, 150, 74, 26, 30, 8
    rows_ = (len(steps) + per - 1) // per
    W = PAD * 2 + per * BW + (per - 1) * GX
    H = PAD * 2 + rows_ * BH + (rows_ - 1) * GY
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s, in %d steps" class="dia">' % (W, H, E(flow.get('name')), len(steps)),
           '<defs><marker id="ar%d" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           '<path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>' % i]
    for n, s in enumerate(steps):
        r, c = divmod(n, per)
        if r % 2:
            c = per - 1 - c  # snake so each arrow is short
        x, y = PAD + c * (BW + GX), PAD + r * (BH + GY)
        auto = (s.get('actor') or '').lower() in ('system', 'flow', 'automation', 'salesforce')
        out.append('<g class="%s"><rect x="%d" y="%d" width="%d" height="%d" rx="6"/>' % ('fs' if auto else 'fp', x, y, BW, BH))
        out.append('<text x="%d" y="%d" class="bs">%d · %s</text>' % (x + 8, y + 16, n + 1, E((s.get('actor') or '')[:20])))
        words, line, lines = (s.get('text') or '').split(), '', []
        for w in words:
            if len(line) + len(w) + 1 > 22:
                lines.append(line); line = w
            else:
                line = (line + ' ' + w).strip()
        lines.append(line)
        for k, ln in enumerate(lines[:3]):
            out.append('<text x="%d" y="%d" class="bt2">%s</text>' % (x + 8, y + 34 + k * 14, E(ln + ('…' if k == 2 and len(lines) > 3 else ''))))
        out.append('</g>')
        if n + 1 < len(steps):
            r2, c2 = divmod(n + 1, per)
            if r2 % 2:
                c2 = per - 1 - c2
            x2, y2 = PAD + c2 * (BW + GX), PAD + r2 * (BH + GY)
            if r2 == r:
                a, b = (x + BW, x2) if c2 > c else (x, x2 + BW)
                out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" marker-end="url(#ar%d)"/>' % (a, y + BH / 2, b, y + BH / 2, i))
            else:
                out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" marker-end="url(#ar%d)"/>' % (x + BW / 2, y + BH, x2 + BW / 2, y2, i))
    out.append('</svg>')
    return '<figure>%s<figcaption>%s. Grey steps are done by a person, blue ones by the system.</figcaption></figure>' % (''.join(out), E(flow.get('name')))


# ---------- the page ----------

GROUPS = [
    ('Data model', ['CustomObject', 'CustomField', 'RecordType', 'BusinessProcess', 'GlobalValueSet', 'StandardValueSet', 'CustomMetadata']),
    ('Rules', ['ValidationRule', 'DuplicateRule', 'MatchingRules']),
    ('Automation', ['Flow', 'ApexClass', 'ApexTrigger', 'Workflow', 'ApprovalProcess', 'AssignmentRules']),
    ('Pages and actions', ['FlexiPage', 'Layout', 'CompactLayout', 'QuickAction', 'ListView', 'CustomTab', 'LightningComponentBundle', 'CustomApplication']),
    ('Access', ['PermissionSet', 'PermissionSetGroup', 'Profile', 'SharingRules', 'Queue', 'Group', 'Role']),
    ('Reporting', ['ReportType', 'Report', 'Dashboard', 'ReportFolder', 'DashboardFolder']),
]


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
         'Waits': 'cw', 'Decided': 'cm', 'Proposed': 'cw'}.get(s, 'cp')
    return '<span class="chip %s">%s</span>' % (k, E(s))


def page(c, rows):
    jira = (c.get('jira_base') or '').rstrip('/')
    jl = lambda key: '<a href="%s/browse/%s">%s</a>' % (E(jira), E(key), E(key)) if jira and key else E(key)
    dec_url = c.get('decisions_url')
    dl = lambda d: '<a href="%s">%s</a>' % (E(dec_url), E(d)) if dec_url else E(d)
    # planned components fill in what the repo does not have yet
    for p in c.get('planned') or []:
        name = '%s/%s' % (p['type'], p['member'])
        r = rows.get(name)
        meta = {k: p[k] for k in ('story', 'task', 'decision', 'why', 'waits') if p.get(k)}
        if r:
            r.update({k: v for k, v in meta.items() if not r.get(k)})
        else:
            rows[name] = dict(type=p['type'], member=p['member'], change=p.get('change', 'New'),
                              status='Waits' if p.get('waits') else 'Planned', details=p.get('details', ''),
                              label=p.get('label'), ref=p.get('ref'), ftype=p.get('ftype'), **meta)
    allrows = sorted(rows.values(), key=lambda r: ([g for g, _ in GROUPS].index(group_of(r['type'])) if group_of(r['type']) != 'Other' else 99, r['type'], r['member'].lower()))
    count = lambda f: sum(1 for r in allrows if f(r))
    stats = [
        ('New objects', count(lambda r: r['type'] == 'CustomObject' and r['change'] == 'New')),
        ('New fields', count(lambda r: r['type'] == 'CustomField' and r['change'] == 'New')),
        ('Automation', count(lambda r: group_of(r['type']) == 'Automation')),
        ('Pages and actions', count(lambda r: group_of(r['type']) == 'Pages and actions')),
        ('Changes to what exists', count(lambda r: r['change'] == 'Changed')),
        ('Removals', count(lambda r: r['change'] == 'Removed')),
    ]
    built = count(lambda r: r['status'] in ('Built', 'Merged'))
    nav, body = [], []

    def sec(anchor, title, inner):
        if not inner:
            return
        nav.append('<a href="#%s">%s</a>' % (anchor, E(title)))
        body.append('<section id="%s"><h2>%s</h2>%s</section>' % (anchor, E(title), inner))

    found, nofls = [], []
    granted = {f for r in allrows if r['type'] == 'PermissionSet' for f, _ in r.get('fields') or []}
    obj_granted = {o for r in allrows if r['type'] == 'PermissionSet' for o, a in r.get('objects') or [] if 'R' in a}
    for r in allrows:
        if r['type'] == 'CustomField' and r['change'] == 'New' and r['status'] != 'Planned' and r['status'] != 'Waits':
            d = (r.get('details') or '')
            if r['member'] not in granted and 'required' not in d and not d.startswith('Master-detail'):
                nofls.append(r['member'])
        if r['type'] == 'CustomObject' and r['change'] == 'New' and r['member'] not in obj_granted and r['status'] not in ('Planned', 'Waits'):
            found.append('`%s` is new and no permission set in this build grants read on it.' % r['member'])
    if c.get('planned'):
        orphan = [r['member'] for r in allrows if r['status'] in ('Built', 'Merged') and not r.get('story') and not r.get('task')
                  and r['type'] not in ('PermissionSet', 'Profile', 'Layout', 'FlexiPage', 'ListView', 'CompactLayout')]
        if orphan:
            found.append('%d component%s in the repo that the build plan does not name: %s. Each needs a story and task, or comes out.' % (
                len(orphan), 's are' if len(orphan) > 1 else ' is', ', '.join('`%s`' % o for o in orphan[:15]) + (' and more' if len(orphan) > 15 else '')))
    if nofls:
        found.insert(0, '%d new field%s that no permission set in this build grants, so only administrators will see %s: %s.' % (
            len(nofls), 's' if len(nofls) > 1 else '', 'them' if len(nofls) > 1 else 'it', ', '.join('`%s`' % f for f in nofls)))
    for k, names in (c.get('_flows') or {}).items():
        if len(names) > 1:
            o, trig = k.split('|')
            found.append('%d active flows run on `%s` at the same moment (%s): %s. Say how they work together, or fold them into one.' % (
                len(names), o, trig.strip(), ', '.join('`%s`' % n for n in names)))
    if found:
        c.setdefault('needs_you', [])
        c['needs_you'] = c['needs_you'] + [{'kind': 'Found in the build', 'text': f} for f in found[:25]]
    need = c.get('needs_you') or []
    sec('needs-you', 'Needs you', '<ul class="need">%s</ul>' % ''.join(
        '<li><span class="nk">%s</span> %s%s</li>' % (E(n.get('kind')), md(n.get('text')),
            ' <a href="%s">Open</a>' % E(n['link']) if n.get('link') else '') for n in need) if need else
        '<p class="muted">Nothing waiting on the SA right now.</p>')
    sec('stories', 'Stories this serves', table(['Story', 'What the design gives it'],
        [[jl(s.get('key')) + ' ' + md(s.get('title')), md(s.get('gives'))] for s in c.get('stories') or []]))
    sec('differences', 'Where the design differs from the stories', table(['#', 'Story says', 'The design does', 'Recommendation'],
        [[E(d.get('n')), md(d.get('says')), md(d.get('does')), md(d.get('rec'))] for d in c.get('differences') or []]))
    sec('rules', 'Rules that shape the design', '<ol class="rules">%s</ol>' % ''.join(
        '<li><b>%s</b> %s <span class="muted">(%s, %s%s)</span></li>' % (md(r.get('rule')), md(r.get('why')), dl(r.get('id')),
            E(r.get('by')), ', ' + E(r.get('date')) if r.get('date') else '') for r in c.get('rules') or []) if c.get('rules') else '')
    sec('today', 'Today and after', table(['Area', 'Today', 'After this build'],
        [[md(x.get('area')), md(x.get('today')), md(x.get('after'))] for x in c.get('today') or []]))
    sec('data-model', 'Data model', erd(rows, c) + table(['Object', 'API name', 'Change', 'Relationship', 'Notes'],
        [[E(r.get('label') or r['member']), '<code>%s</code>' % E(r['member']), chip(r['change']),
          md(next((x.get('details') for x in allrows if x['type'] == 'CustomField' and x['member'].startswith(r['member'] + '.')
                   and (x.get('ftype') in ('MasterDetail',) or 'aster-detail' in (x.get('details') or ''))), '') or ''),
          md(r.get('why') or r.get('details'))] for r in allrows if r['type'] == 'CustomObject']))
    flows = c.get('flows') or []
    sec('flows', 'How it works', ''.join(
        '<h3>%s</h3>%s%s%s' % (md(f.get('name')), flow_svg(f, i), '<ol>%s</ol>' % ''.join(
            '<li><b>%s.</b> %s</li>' % (E(s.get('actor')), md(s.get('text'))) for s in f.get('steps') or []),
            table(['When', 'What happens'], [[md(o.get('when')), md(o.get('then'))] for o in f.get('outcomes') or []]))
        for i, f in enumerate(flows)))
    autos = [r for r in allrows if group_of(r['type']) == 'Automation']
    sec('automation', 'Automation', table(['Automation', 'Type', 'Runs when', 'What it does', 'Beside it on the same object and event', 'Status'],
        [['<code>%s</code>' % E(a.get('name')), E(a.get('type')), md(a.get('runs_when')), md(a.get('does')), md(a.get('beside') or 'Nothing'),
          chip(rows.get('Flow/' + (a.get('name') or ''), {}).get('status', a.get('status', 'Planned')))]
         for a in c.get('automation') or []] or
        [['<code>%s</code>' % E(a['member']), E(a['type']), E(a.get('trigger')), md(a.get('details')), '', chip(a['status'])] for a in autos]))
    # the full inventory, filterable
    FRIENDLY = {'CustomObject': 'Object', 'CustomField': 'Field', 'RecordType': 'Record type', 'ValidationRule': 'Validation rule',
                'Flow': 'Flow', 'ApexClass': 'Apex class', 'ApexTrigger': 'Apex trigger', 'FlexiPage': 'Lightning page', 'Layout': 'Page layout',
                'CompactLayout': 'Compact layout', 'QuickAction': 'Action', 'ListView': 'List view', 'CustomTab': 'Tab',
                'PermissionSet': 'Permission set', 'PermissionSetGroup': 'Permission set group', 'LightningComponentBundle': 'LWC',
                'CustomMetadata': 'Custom metadata record', 'GlobalValueSet': 'Global value set', 'ReportType': 'Report type'}
    inv, last = [], None
    for r in allrows:
        g = group_of(r['type'])
        if g != last:
            inv.append('<tr class="gh" data-g="%s"><td colspan="5">%s</td></tr>' % (E(g), E(g)))
            last = g
        label = r.get('label')
        name = ('%s<br>' % E(label) if label and label != r['member'] else '') + '<code>%s</code>' % E(r['member'])
        st = chip(r['status']) + ('<div class="muted">waits on %s</div>' % E(r['waits']) if r.get('waits') else '')
        trace = '<br>'.join(x for x in [jl(r['story']) if r.get('story') else '', E(r.get('task') or ''),
                                        dl(r['decision']) if r.get('decision') else ''] if x)
        inv.append('<tr data-g="%s" data-c="%s" data-s="%s"><td>%s<div class="muted">%s</div></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            E(g), E(r['change']), E(r['status']), name, E(FRIENDLY.get(r['type'], r['type'])), chip(r['change']),
            md(r.get('why') or '') + ('<div class="muted">%s</div>' % md(r['details']) if r.get('details') and r.get('why') else md(r.get('details') or '') if not r.get('why') else ''),
            trace, st))
    inv = ''.join(inv)
    filt = '<div class="filt">%s%s%s<input id="q" type="search" placeholder="Search names and details"></div>' % (
        '<select id="fg"><option value="">Every kind</option>%s</select>' % ''.join('<option>%s</option>' % E(g) for g, _ in GROUPS),
        '<select id="fc"><option value="">New, changed and removed</option><option>New</option><option>Changed</option><option>Removed</option></select>',
        '<select id="fs"><option value="">Any status</option><option>Planned</option><option>Waits</option><option>Built</option><option>Merged</option></select>')
    sec('inventory', 'Every component', '<p class="muted">%d components. %d built or merged. Details for built components are read from the metadata files in the repo; planned ones come from the build plan.</p>%s<div class="tw"><table id="inv"><colgroup><col style="width:28%%"><col style="width:9%%"><col><col style="width:12%%"><col style="width:11%%"></colgroup><thead><tr><th>Component</th><th>Change</th><th>Details</th><th>Story, task, decision</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div>' % (len(allrows), built, filt, inv) if allrows else '')
    # pages
    pages = c.get('pages') or []
    sec('pages', 'Pages, layouts and actions', table(['Page or action', 'Object', 'What the user sees'],
        [[md(p.get('name')), E(p.get('object')), md(p.get('shows'))] for p in pages]))
    # access matrix from permission sets in the repo, plus content
    ps = [r for r in allrows if r['type'] == 'PermissionSet' and r.get('objects')]
    acc = ''
    if ps:
        objs = sorted({o for r in ps for o, _ in r['objects']})
        acc = table(['Object'] + [r['member'] for r in ps], [['<code>%s</code>' % E(o)] + [E(dict(r['objects']).get(o, '')) for r in ps] for o in objs], 'mx')
        acc += '<p class="muted">C create, R read, E edit, D delete, read from the permission set files.</p>'
        newf = [r['member'] for r in allrows if r['type'] == 'CustomField' and r['change'] == 'New' and r['status'] in ('Built', 'Merged')]
        if newf:
            acc += '<h3>New fields</h3>' + table(['Field'] + [r['member'] for r in ps],
                [['<code>%s</code>' % E(f)] + [E(dict(r.get('fields') or []).get(f, '')) or '<span class="muted">none</span>' for r in ps] for f in newf], 'mx')
    sec('access', 'Who can do what', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(a) for a in c.get('access') or []) + acc if (c.get('access') or acc) else '')
    sec('reporting', 'Reporting', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(x) for x in c.get('reporting') or []) if c.get('reporting') else '')
    changed = [r for r in allrows if r['change'] in ('Changed', 'Removed')]
    sec('changes', 'Changes to what is already in the org', table(['Component', 'Change', 'What changes, and what depends on it', 'Done by'],
        [['<code>%s/%s</code>' % (E(r['type']), E(r['member'])), chip(r['change']), md(r.get('why') or r.get('details') or ''),
          'A person, by hand' if r['change'] == 'Removed' else 'The build'] for r in changed]))
    sec('build', 'The build', table(['Task', 'Story', 'Holds', 'Waits on', 'Status'],
        [[E(x.get('id')), jl(x.get('story')), md(x.get('holds')), md(x.get('waits') or 'Nothing'),
          chip(x.get('status', 'Planned')) + (' <a href="%s">PR</a>' % E(x['pr']) if x.get('pr') else '')] for x in c.get('tasks') or []]))
    sec('open-questions', 'Open questions', table(['#', 'Question', 'Owner', 'Blocks'],
        [[E(q.get('n')), md(q.get('q')), E(q.get('owner')), md(q.get('blocks'))] for q in c.get('open_questions') or []]))
    sec('checks', 'Checks a person makes in the sandbox', '<ol>%s</ol>' % ''.join('<li>%s</li>' % md(v) for v in c.get('checks') or []) if c.get('checks') else '')
    sec('not-built', 'Not built', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(v) for v in c.get('not_built') or []) if c.get('not_built') else '')
    sec('sources', 'Sources', '<ul>%s</ul>' % ''.join('<li>%s</li>' % md(v) for v in c.get('sources') or []) if c.get('sources') else '')
    sec('change-log', 'Change log', table(['Date', 'Change'], [[E(x.get('date')), md(x.get('change'))] for x in c.get('changelog') or []]))

    statbox = ''.join('<div class="st"><div class="sl">%s</div><div class="sn">%d</div></div>' % (E(a), b) for a, b in stats)
    head = ('<header><div class="eyebrow">Design and build review · %s</div><h1>%s</h1><p class="lede">%s</p>'
            '<p class="meta">%s</p><div class="stats">%s</div></header>') % (
        E(c.get('client')), E(c.get('title') or 'Design and build review'), md(c.get('summary')),
        ' · '.join(md(x) for x in [c.get('status'), 'SA: ' + c['sa'] if c.get('sa') else '', 'as of ' + (c.get('as_of') or str(date.today())),
                                   c.get('links')] if x), statbox)
    return TEMPLATE.replace('%%TITLE%%', E('%s · %s' % (c.get('client'), c.get('title') or 'Design and build review'))).replace(
        '%%NAV%%', ''.join(nav)).replace('%%HEAD%%', head).replace('%%BODY%%', ''.join(body))


TEMPLATE = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<style>
:root{--bg:#fff;--fg:#1b1b1f;--mut:#5c5c66;--line:#e3e3e8;--soft:#f6f6f8;--acc:#1f5fbf;--accbg:#e8f0fc;--amb:#8a5a00;--ambbg:#fdf3dc;--red:#a32d2d;--redbg:#fcebeb;--grn:#2e6b16;--grnbg:#eaf3de;--nav:#0f2747}
@media (prefers-color-scheme:dark){:root{--bg:#141418;--fg:#ececf0;--mut:#a3a3ad;--line:#2c2c33;--soft:#1c1c22;--acc:#8ab4f8;--accbg:#18263d;--amb:#f0c060;--ambbg:#33280f;--red:#f09595;--redbg:#3a1818;--grn:#9fd47a;--grnbg:#1f2c15;--nav:#0b1626}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.wrap{display:grid;grid-template-columns:220px minmax(0,1fr);max-width:1320px;margin:0 auto}
nav{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;padding:24px 16px;border-right:1px solid var(--line);font-size:13px}
nav a{display:block;color:var(--mut);text-decoration:none;padding:4px 8px;border-radius:6px}nav a:hover{background:var(--soft);color:var(--fg)}
main{padding:28px 40px 80px;min-width:0}header{border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:8px}
.eyebrow{font-size:12px;letter-spacing:.04em;color:var(--mut);text-transform:uppercase}h1{font-size:26px;margin:6px 0 8px;font-weight:600}
h2{font-size:19px;margin:36px 0 10px;font-weight:600}h3{font-size:16px;margin:22px 0 8px;font-weight:600}
.lede{font-size:16px;max-width:860px}.meta{color:var(--mut);font-size:13px}.muted{color:var(--mut)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-top:14px}
.st{background:var(--soft);border-radius:8px;padding:10px 12px}.sl{font-size:12px;color:var(--mut)}.sn{font-size:22px;font-weight:600}
.tw{overflow-x:auto;margin:10px 0}table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{text-align:left;vertical-align:top;padding:7px 10px;border-bottom:1px solid var(--line)}
th{font-weight:600;color:var(--mut);font-size:12px;background:var(--soft)}code{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft);padding:1px 4px;border-radius:4px}
table.mx td{text-align:center}table.mx td:first-child{text-align:left}
.chip{display:inline-block;font-size:11.5px;padding:1px 8px;border-radius:10px;white-space:nowrap;background:var(--soft);color:var(--mut)}
.cn{background:var(--accbg);color:var(--acc)}.cc{background:var(--ambbg);color:var(--amb)}.cr{background:var(--redbg);color:var(--red)}
.cb{background:var(--accbg);color:var(--acc)}.cm{background:var(--grnbg);color:var(--grn)}.cw{background:var(--ambbg);color:var(--amb)}
.need{padding-left:0;list-style:none}.need li{border:1px solid var(--line);border-left:3px solid var(--amb);border-radius:0 8px 8px 0;padding:8px 12px;margin:6px 0}
.nk{font-size:12px;font-weight:600;color:var(--amb);margin-right:6px}.rules li{margin:6px 0}
figure{margin:12px 0 18px}figcaption{font-size:12.5px;color:var(--mut);margin-top:6px}.dia{width:100%;height:auto;max-width:100%;color:var(--fg)}
.dia text{fill:currentColor;font-family:inherit}.dia .dl{font-size:11px;fill:var(--mut)}.dia .el{font-size:10.5px;fill:var(--mut)}
.dia .bt{font-size:13px;font-weight:600}.dia .bt2{font-size:11.5px}.dia .bs{font-size:10.5px;fill:var(--mut)}
.dia rect{fill:var(--soft);stroke:var(--line);stroke-width:1.2}.dia .bn rect{fill:var(--accbg);stroke:var(--acc)}.dia .bc rect{fill:var(--ambbg);stroke:var(--amb)}
.dia .fs rect{fill:var(--accbg);stroke:var(--acc)}
tr.gh td{background:var(--soft);font-weight:600;font-size:12.5px;padding:6px 10px}#inv{table-layout:fixed}#inv td{word-break:break-word}
.filt{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.filt select,.filt input{font:inherit;font-size:13px;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.filt input{flex:1;min-width:180px}a{color:var(--acc)}
@media (max-width:860px){.wrap{grid-template-columns:1fr}nav{display:none}main{padding:20px}}
</style></head><body><div class="wrap"><nav>%%NAV%%</nav><main>%%HEAD%%%%BODY%%</main></div>
<script>
(function(){var g=document.getElementById('fg'),c=document.getElementById('fc'),s=document.getElementById('fs'),q=document.getElementById('q');
if(!g)return;function f(){var t=(q.value||'').toLowerCase();document.querySelectorAll('#inv tbody tr').forEach(function(r){if(r.classList.contains('gh')){r.style.display=(!g.value||r.dataset.g===g.value)?'':'none';return}
var ok=(!g.value||r.dataset.g===g.value)&&(!c.value||r.dataset.c===c.value)&&(!s.value||r.dataset.s===s.value)&&(!t||r.textContent.toLowerCase().indexOf(t)>-1);r.style.display=ok?'':'none'})}
[g,c,s].forEach(function(e){e.addEventListener('change',f)});q.addEventListener('input',f)})();
</script></body></html>'''


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
