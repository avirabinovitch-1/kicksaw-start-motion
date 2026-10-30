"""Build a client's solution readout page from its three discovery documents and the readout content file.

Usage:
  python3 -I build-readout.py --template "Kicksaw Solution Readout.template.html" \
      --content readout-content.json --workflows "<Client> Workflows.html" --heard "<Client> What We Heard.html" \
      --out "<Client> Solution Readout.html" [--allow-template]

--workflows and --heard take the page source of the client's workflow document and What we heard page (as read from
their artifacts) or a .json file holding just their data block. The readout's sections 02 to 04 come from What we
heard as it is, and its workflows are copied from the workflow document's data, so both draw identically.
Refuses to build a client readout from template data unless --allow-template is passed (used only to build the
template itself). Prints every check that failed and every placeholder left to fill.
"""
import argparse, json, re, sys

ap = argparse.ArgumentParser()
ap.add_argument('--template', required=True)
ap.add_argument('--content', required=True)
ap.add_argument('--workflows', required=True)
ap.add_argument('--heard', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--allow-template', action='store_true')
a = ap.parse_args()

def block(path, tag):
    txt = open(path, encoding='utf-8').read()
    if path.endswith('.json'):
        return json.loads(txt)
    m = re.search(r'<script id="%s" type="application/json">\s*(\{.*?)\s*</script>' % tag, txt, re.S)
    if not m:
        sys.exit('%s: no %s block found' % (path, tag))
    return json.loads(m.group(1))

C = json.load(open(a.content, encoding='utf-8'))
WF = block(a.workflows, 'wf-data')
WH = block(a.heard, 'wwh-data')
html = open(a.template, encoding='utf-8').read()

problems, notes = [], []
client_build = not C['project'].get('template')
for name, d in (('workflow document', WF), ('What we heard page', WH)):
    if d['project'].get('template') and client_build and not a.allow_template:
        sys.exit('The %s is still the template (template: true). Point at the client\'s copy.' % name)
    if d['project'].get('client') != C['project'].get('client'):
        problems.append('Client name differs: readout "%s", %s "%s"' % (C['project'].get('client'), name, d['project'].get('client')))

D = dict(C)
inc = C.get('include', {})

# 02 to 04 from What we heard, as it is
s02 = dict(C.get('s02') or {})
s02['lede'] = s02.get('lede') or WH['project'].get('lede', '')
s02.setdefault('quoteSource', WH['project'].get('quoteSource', ''))
s02['themes'] = WH.get('themes', [])
D['s02'] = s02
s03 = dict(C.get('s03') or {}); s03['pains'] = WH.get('pains', []); s03['constraint'] = WH.get('constraint')
D['s03'] = s03
s04 = dict(C.get('s04') or {}); s04['numbers'] = WH.get('numbers', []); s04['replaced'] = WH.get('replaced', []); s04['stays'] = WH.get('stays', [])
D['s04'] = s04
if inc.get('02') is not False and not s02['themes']:
    problems.append('What we heard is in, but the What we heard page has no themes')

# workflows, copied from the workflow document's data
byid = {w['id']: w for w in WF.get('workflows', [])}
draw = (C.get('s08') or {}).get('draw') or list(byid)
missing = [w for w in draw if w not in byid]
if missing:
    problems.append('Section 08 draws workflows the workflow document does not have: ' + ', '.join(missing))
D['workflows'] = [byid[w] for w in draw if w in byid]
for wid in ((C.get('s08') or {}).get('notes') or {}):
    if wid not in draw:
        problems.append('Section 08 has today/changes notes for %s, which is not drawn' % wid)
not_drawn = [w for w in byid if w not in draw]
if not_drawn:
    notes.append('In the workflow document but not drawn in the readout: ' + ', '.join(not_drawn))

# checks on the judgment items
ap1 = (C.get('s01') or {}).get('approve') or {}
if len(ap1.get('items', [])) != 3:
    problems.append('Section 01 should ask for exactly three approvals; it has %d' % len(ap1.get('items', [])))
if not ap1.get('definition'):
    problems.append('Section 01 has no sign-off definition')
if C['project'].get('status') == 'final' and C['project'].get('version', '') not in ap1.get('definition', ''):
    problems.append('Final for sign-off, but the sign-off definition does not name version %s' % C['project'].get('version'))
for r in (C.get('s13') or {}).get('rows', []):
    if r.get('status') == 'open' and not r.get('who'):
        problems.append('Open decision "%s" has no one named to decide it' % r.get('area'))
for it in (C.get('s14') or {}).get('items', []):
    if not it.get('owner'):
        problems.append('Input "%s" has no owner' % it.get('text', '')[:50])

blob = json.dumps(D, ensure_ascii=False)
if '—' in blob:
    problems.append('Em dashes found in the readout content')
ph = sorted(set(re.findall(r'\[[A-Za-z][^\]\["{}\\]{0,120}\]', blob)))
if ph and client_build:
    notes.append('Placeholders still to fill: ' + ', '.join(ph))

m = re.search(r'(<script id="ro-data" type="application/json">\n)(.*?)(\n</script>)', html, re.S)
if not m:
    sys.exit('template: no ro-data block found')
out = html[:m.start(2)] + json.dumps(D, indent=1, ensure_ascii=False).replace('</', '<\\/') + html[m.end(2):]
title = 'Kicksaw Solution Readout' if C['project'].get('template') else '%s Solution Readout' % C['project']['client']
out = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, out, count=1)
open(a.out, 'w', encoding='utf-8').write(out)
print('wrote %s (%d bytes), title: %s, workflows: %s' % (a.out, len(out), title, ', '.join(draw)))
for p in problems:
    print('CHECK:', p)
for n in notes:
    print('NOTE:', n)
