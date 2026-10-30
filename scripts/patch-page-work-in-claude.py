"""Add the "Work in Claude" line to each stage's step 1 on a saved copy of the Start Motion page, and the plugin
line to the kit inventory. Takes nothing away: the copy boxes, prompts and builders stay as the page door.

Applied Oct 30, 2026 (kept so the page can be rebuilt). Run it before scripts/patch-page-start-here.py. Usage:
  python3 -I scripts/patch-page-work-in-claude.py --page "start-motion.html" --out "start-motion.patched.html"

Run scripts/refresh-page-skills.py on the output afterwards (or before; the two are independent) and publish the
result over the same artifact URL. Stops if an anchor is missing or already patched.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, 'plugins', 'start-motion')
MARKET = 'avirabinovitch-1/kicksaw-start-motion'

STEPS = [  # step 1 heading on the page -> the command(s)
    ('Save the handoff builder in Claude', ['/start-motion:handoff']),
    ('Save the kickoff deck skill in Claude', ['/start-motion:kickoff']),
    ('Save the two discovery skills in Claude', ['/start-motion:discovery-plan', '/start-motion:discovery-call']),
    ('Save the readout builder in Claude', ['/start-motion:readout']),
    ('Save the design builder in Claude', ['/start-motion:design']),
    ('Save the story writer in Claude', ['/start-motion:user-stories']),
]

CSS = """
<style id="work-in-claude-css">
.wic { margin: 12px 0 14px; padding: 12px 14px; border: 1px solid var(--line, #D9DEE3); border-left: 3px solid var(--accent, #0071B9); border-radius: 8px; font-size: 14px; }
.wic b { display: block; margin-bottom: 4px; }
.wic code { font: 500 13px ui-monospace, Menlo, monospace; background: var(--sunk, #EFF2F5); padding: 1px 6px; border-radius: 4px; }
</style>
"""

ap = argparse.ArgumentParser()
ap.add_argument('--page', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()

page = open(a.page, encoding='utf-8').read()
if 'work-in-claude-css' in page:
    sys.exit('this page already carries the Work in Claude patch')
version = json.load(open(os.path.join(PLUGIN, '.claude-plugin', 'plugin.json'), encoding='utf-8'))['version']

for heading, cmds in STEPS:
    m = re.search(r'<h3>%s</h3>\s*<p>.*?</p>' % re.escape(heading), page, re.S)
    if not m:
        sys.exit('step 1 not found: ' + heading)
    cmd_html = ' or '.join('<code>/%s</code>' % c.split(':', 1)[1] for c in cmds)
    full_html = ' or '.join('<code>%s</code>' % c for c in cmds)
    box = ('\n<div class="wic"><b>Or work directly in Claude.</b> Install the Kicksaw Project Start Motion plugin once '
           '(the steps are on <button class="go" type="button" data-go="start">Start here</button>; marketplace <code>%s</code>, Sync automatically on), then type %s '
           '(in Cowork and Claude Code, %s). '
           'It is the same skill as the copy below, with nothing to paste: it tells you where the client stands, asks for its picks in one message, '
           'and names the next command when it is done. Updates reach you with each weekly release.</div>' % (MARKET, cmd_html, full_html))
    page = page[:m.end()] + box + page[m.end():]
    print('patched:', heading)

anchor = '<li><b>7 Kicksaw skills</b><span>Saved once in each person\'s Claude; each one reads what the stage before it made.</span></li>'
if anchor not in page:
    sys.exit('kit inventory line not found')
page = page.replace(anchor, '<li><b>7 Kicksaw skills</b><span>Saved once in each person\'s Claude from the copy boxes, or installed once as the Kicksaw Project Start Motion plugin (<i data-plugin-version="%s" style="font-style:normal">v%s</i>, updates itself weekly); each one reads what the stage before it made.</span></li>' % (version, version))
print('patched: kit inventory')

if '</head>' in page:
    page = page.replace('</head>', CSS + '</head>', 1)
else:  # the live page source starts at <title> (the host adds the head); put the style right after it
    page = re.sub(r'(<title>.*?</title>)', lambda m: m.group(1) + CSS, page, count=1, flags=re.S)
open(a.out, 'w', encoding='utf-8').write(page)
print('wrote', a.out, len(page), 'bytes')
