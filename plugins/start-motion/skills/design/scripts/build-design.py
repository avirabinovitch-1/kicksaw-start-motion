"""Build a client's solution design page from its content file.

Usage:
  python3 -I build-design.py --template "../templates/Kicksaw Solution Design.template.html" \
      --content design-content.json --out "<Client> Solution Design v0.1.html" [--logo ../brand/primary-full-color.svg]

The content file is the design (references/design-content.md says what goes in it). Claude writes and edits the
content file, one section at a time; this script turns it into the page. Nobody writes the page's HTML by hand.
Prints a CHECK line for every problem (the page is still written, so it can be looked at) and exits 1 if there
were any. Prints a NOTE line with the counts.
"""
import argparse, json, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument('--template', required=True)
ap.add_argument('--content', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--logo', default=None)
a = ap.parse_args()

here = os.path.dirname(os.path.abspath(__file__))
logo_path = a.logo or os.path.join(here, '..', 'brand', 'primary-full-color.svg')
tpl = open(a.template, encoding='utf-8').read()
raw = open(a.content, encoding='utf-8').read()
data = json.loads(raw)
checks = []
def check(msg): checks.append(msg)

for k in ('client', 'version', 'status', 'sections', 'decisions'):
    if k not in data:
        check('content file has no "%s"' % k)
if data.get('status') not in ('Draft', 'Final'):
    check('status must be Draft or Final, found %r' % data.get('status'))
if '—' in raw:
    check('em dash in the content file; rewrite the sentence')

secs = data.get('sections', [])
decs = data.get('decisions', [])
sec_ids = [s.get('id') for s in secs]
dec_ids = [d.get('id') for d in decs]
for i in set(x for x in sec_ids if sec_ids.count(x) > 1):
    check('two sections share the id %r' % i)
for i in set(x for x in dec_ids if dec_ids.count(x) > 1):
    check('two decisions share the id %r' % i)
AUTO = ('key-decisions', 'claude-calls', 'change-log')
for s in secs:
    if not re.match(r'^[a-z0-9-]+$', s.get('id') or ''):
        check('section id %r: use lower-case letters, digits and hyphens' % s.get('id'))
    if not s.get('title'):
        check('section %r has no title' % s.get('id'))
    if s.get('auto') and s['auto'] not in AUTO:
        check('section %r: auto must be one of %s' % (s.get('id'), ', '.join(AUTO)))
    if not s.get('auto') and not (s.get('html') or '').strip():
        check('section %r is empty' % s.get('id'))
    for ref in re.findall(r'\{\{(D-[\w-]+)\}\}', s.get('html') or ''):
        if ref not in dec_ids:
            check('section %r marks %s, which is not in decisions' % (s.get('id'), ref))
        else:
            d = decs[dec_ids.index(ref)]
            if d.get('section') and d['section'] != s.get('id') and d.get('kind') != 'clear':
                pass  # a decision can be marked in more than one section; its card sits in its own
    if re.search(r'<script', s.get('html') or '', re.I):
        check('section %r contains a script tag' % s.get('id'))

KINDS = ('sa', 'recommended', 'client', 'clear')
STATUS = ('open', 'decided', 'parked', 'dropped')
for d in decs:
    i = d.get('id')
    if not re.match(r'^D-\d+$', i or ''):
        check('decision id %r: use D-01, D-02 and on' % i)
    if d.get('kind') not in KINDS:
        check('%s: kind must be one of %s' % (i, ', '.join(KINDS)))
    if d.get('status') not in STATUS:
        check('%s: status must be one of %s' % (i, ', '.join(STATUS)))
    if not d.get('q'):
        check('%s has no question (q)' % i)
    if d.get('kind') != 'clear' and d.get('section') not in sec_ids:
        check('%s: section %r is not a section of this design' % (i, d.get('section')))
    if d.get('depends_on') and d['depends_on'] not in dec_ids:
        check('%s depends on %s, which is not in decisions' % (i, d['depends_on']))
    if d.get('kind') == 'sa':
        opts = d.get('opts') or []
        if len(opts) < 2 and d.get('status') == 'open':
            check('%s is an SA call with fewer than two options' % i)
        keys = [o.get('k') for o in opts]
        if d.get('lean') and d['lean'] not in keys:
            check('%s: lean %r is not one of its options' % (i, d['lean']))
        if not d.get('lean') and not d.get('lean_why') and d.get('status') == 'open':
            check('%s has no lean and does not say what it turns on (lean_why)' % i)
        for o in opts:
            for f in ('k', 'name'):
                if not o.get(f):
                    check('%s: an option has no %s' % (i, f))
    if d.get('kind') == 'recommended' and not d.get('pick'):
        check('%s is a recommendation with no pick' % i)
    if d.get('kind') == 'clear':
        if d.get('status') != 'decided':
            check('%s is a call Claude made, so its status is decided' % i)
    if d.get('status') == 'decided' and not d.get('chosen'):
        check('%s is decided but has no chosen value' % i)
    if d.get('structural') and d.get('kind') not in ('sa', 'recommended'):
        check('%s: only an SA call or a recommendation can be structural' % i)

open_asks = [d for d in decs if d.get('kind') in ('sa', 'recommended') and d.get('status') in ('open', 'parked')]
if data.get('status') == 'Final' and open_asks:
    check('status is Final with %d decision(s) still open: %s' % (len(open_asks), ', '.join(d['id'] for d in open_asks)))
for need in ('key-decisions', 'change-log'):
    if not any(s.get('auto') == need for s in secs):
        check('no section with auto "%s"' % need)

logo = ''
if os.path.exists(logo_path):
    logo = open(logo_path, encoding='utf-8').read()
    logo = re.sub(r'<\?xml.*?\?>', '', logo)
    logo = re.sub(r'<!--.*?-->', '', logo, flags=re.S)
    logo = re.sub(r'<!DOCTYPE.*?>', '', logo, flags=re.S).strip().replace('`', '').replace('${', '$ {')
else:
    check('logo not found at %s' % logo_path)

title = '%s Solution Design' % (data.get('client') or 'Client')
blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
for token in ('%%TITLE%%', '%%DATA%%', '%%LOGO%%'):
    if tpl.count(token) != 1:
        sys.exit('template: expected exactly one %s' % token)
page = tpl.replace('%%TITLE%%', title.replace('<', '').replace('>', '')).replace('%%LOGO%%', logo).replace('%%DATA%%', blob)
open(a.out, 'w', encoding='utf-8').write(page)

for c in checks:
    print('CHECK ' + c)
n = lambda k, st=None: sum(1 for d in decs if d.get('kind') == k and (st is None or d.get('status') in st))
print('NOTE %s %s, %s: %d sections; SA calls %d open of %d; recommendations %d to confirm of %d; with the client %d; calls Claude made %d; %d bytes'
      % (data.get('client'), data.get('version'), data.get('status'), len(secs), n('sa', ('open', 'parked')), n('sa'),
         n('recommended', ('open', 'parked')), n('recommended'), n('client', ('open', 'parked')), n('clear'), len(page)))
sys.exit(1 if checks else 0)
