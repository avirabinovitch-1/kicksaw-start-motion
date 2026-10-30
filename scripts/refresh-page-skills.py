"""Write the plugin's seven skill texts into a saved copy of the Start Motion page, so the page's copy boxes
hand out the same skill the plugin installs.

Usage:
  python3 -I scripts/refresh-page-skills.py --page "start-motion.html" --out "start-motion.patched.html" [--version 0.1.0]

--page is the live page's index.html as read from the artifact (host wrapper or not; the script only touches the
<pre id="...SkillText"> blocks and the kit's version line). Publish the output over the same artifact URL.
Prints each block it replaced with the old and new sizes, and stops if a block or a skill file is missing.
"""
import argparse, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, 'plugins', 'start-motion')
BLOCKS = {  # pre id on the page -> skill folder
    'handoffSkillText': 'handoff',
    'skillText': 'kickoff',
    'planSkillText': 'discovery-plan',
    'discSkillText': 'discovery-call',
    'roSkillText': 'readout',
    'desSkillText': 'design',
    'storySkillText': 'user-stories',
}

ap = argparse.ArgumentParser()
ap.add_argument('--page', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--version', default=None, help='plugin version to show on the page; default: plugin.json')
a = ap.parse_args()

page = open(a.page, encoding='utf-8').read()
version = a.version or json.load(open(os.path.join(PLUGIN, '.claude-plugin', 'plugin.json'), encoding='utf-8'))['version']

for pid, skill in BLOCKS.items():
    path = os.path.join(PLUGIN, 'skills', skill, 'SKILL.md')
    if not os.path.exists(path):
        sys.exit('missing skill file: ' + path)
    text = open(path, encoding='utf-8').read().rstrip('\n')
    # stamp the plugin version into the skill's run-log row, so the seven files never need editing by hand on release
    stamped = re.sub(r'(start-motion:%s \()v[0-9][^)]*(\))' % re.escape(skill), r'\g<1>v%s\g<2>' % version, text)
    if stamped != text:
        open(path, 'w', encoding='utf-8').write(stamped + '\n')
        text = stamped
    m = re.search(r'(<pre[^>]*\bid="%s"[^>]*>)(.*?)(</pre>)' % re.escape(pid), page, re.S)
    if not m:
        sys.exit('page has no <pre id="%s">' % pid)
    old = m.group(2)
    # the page wraps the text in <code>...</code>; keep that wrapper if it was there
    inner = html.escape(text, quote=False)
    if old.lstrip().startswith('<code>'):
        inner = '<code>' + inner + '</code>'
    page = page[:m.start(2)] + inner + page[m.end(2):]
    print('%-16s %-15s %6d -> %6d chars' % (pid, skill, len(old), len(inner)))

# version line, if the page carries one
page, n = re.subn(r'(data-plugin-version=")[^"]*(")', r'\g<1>%s\g<2>' % version, page)
print('plugin version marker updated' if n else 'no plugin version marker on this page yet (add data-plugin-version to the kit inventory)')
open(a.out, 'w', encoding='utf-8').write(page)
print('wrote', a.out, len(page), 'bytes')
