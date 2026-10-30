"""Add the "Start here" page to a saved copy of the Start Motion page, and the new-client setup command to the kit
inventory. Takes nothing away.

What it adds:
  - A "Start here" slide right after Overview: what the kit is, the two ways to work, the one-time install steps,
    how a client is started (the new-client command, or the same steps by hand), where things live, the stages in
    order, and where feedback goes. It carries the new-client skill's copy box, filled from the plugin.
  - A "Start here" box in the Overview band.
  - Kit inventory: the new-client setup row, 8 skills instead of 7, the skill names shown as their commands, and the
    templates note updated (the plugin carries the copies Claude builds from).

Run scripts/patch-page-work-in-claude.py first (this script expects its "8 Kicksaw skills" anchor to be the one that
script leaves), then this one, then scripts/refresh-page-skills.py, and publish over the same artifact URL.

Usage:
  python3 -I scripts/patch-page-start-here.py --page "start-motion.html" --out "start-motion.patched.html"
Stops if an anchor is missing or the page is already patched.
"""
import argparse, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, 'plugins', 'start-motion')
MARKET = 'avirabinovitch-1/kicksaw-start-motion'
FEEDBACK = 'https://claude.ai/artifact/EpRXHNkkifdH2xrd33qP7K'

ap = argparse.ArgumentParser()
ap.add_argument('--page', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()

page = open(a.page, encoding='utf-8').read()
if 'id="start"' in page:
    sys.exit('this page already carries the Start here patch')
version = json.load(open(os.path.join(PLUGIN, '.claude-plugin', 'plugin.json'), encoding='utf-8'))['version']
skill = open(os.path.join(PLUGIN, 'skills', 'new-client', 'SKILL.md'), encoding='utf-8').read().rstrip('\n')

def need(anchor, what):
    if page.count(anchor) != 1:
        sys.exit('%s: anchor found %d times' % (what, page.count(anchor)))

CSS = """
<style id="start-here-css">
.sh-ways code, .sh-list code, .sh-live code, .path-body code { font: 500 13px var(--mono); background: var(--surface); border: 1px solid var(--rule); padding: 1px 6px; border-radius: 4px; white-space: nowrap; }
.sh-h { margin: 34px 0 14px; }
.sh-h h3 { font-size: 22px; margin: 0 0 4px; }
.sh-h p { margin: 0; color: var(--muted); font-size: 14.5px; }
.sh-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; max-width: 1100px; }
.sh-list li { display: grid; grid-template-columns: 34px minmax(0, 1fr) auto; gap: 14px; align-items: center; padding: 10px 14px; background: var(--surface); border: 1px solid var(--rule); border-radius: 8px; min-width: 0; }
.sh-list .n { display: grid; place-items: center; width: 30px; height: 30px; border-radius: 50%; background: var(--drive); color: var(--drive-ink); font: 500 15px var(--display); }
.sh-list .n.m { background: var(--chip); color: var(--ink-2); }
.sh-list b { display: block; color: var(--ink); font-size: 15.5px; }
.sh-list span { display: block; color: var(--ink-2); font-size: 14px; }
.sh-list .cmd { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
.sh-list .cmd .go { font-size: 14px; }
.sh-live { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px 32px; max-width: 1100px; }
.sh-live > div { border-top: 4px solid var(--teal); padding-top: 12px; min-width: 0; }
.sh-live b { display: block; color: var(--heading); font-size: 15.5px; margin-bottom: 4px; }
.sh-live p { font-size: 14.5px; margin: 0; }
.band .req + .req { margin-top: 0; }
@media (max-width: 760px) {
  .sh-live { grid-template-columns: minmax(0, 1fr); }
  .sh-list li { grid-template-columns: 34px minmax(0, 1fr); }
  .sh-list .cmd { grid-column: 2; align-items: flex-start; }
}
</style>
"""

SLIDE = """
<!-- START HERE -->
<section class="slide" id="start" data-label="Start here" data-n="&#9654;">
  <p class="eyebrow">Start here</p>
  <h2>Your first project with the kit</h2>
  <p class="lead">The kit is seven stages. Each one has its method on this page and a skill that does the work in Claude. You can work from this page or straight from Claude; both run the same skill. This page gets you set up once, then started on a client in a few minutes.</p>

  <div class="strip3 sh-ways">
    <div><b>Page first</b><p>Open the stage, read how it runs and what good looks like, then use its builder or copy its prompt and paste it into Claude.</p></div>
    <div><b>Claude first</b><p>Open Claude and type the stage's command, such as <code>/kickoff</code>. The skill says where the client stands, asks for its picks in one message, runs, and names the next command.</p></div>
    <div><b>Either way, the same skill</b><p>The plugin installs the same skill text the copy boxes on each stage hand out. This page stays the place to read the method, the examples and the bar.</p></div>
  </div>

  <div class="sh-h"><h3>Set up once</h3><p>About ten minutes, on your own Claude account. After this, every stage command works.</p></div>
  <ol class="path">
    <li>
      <div class="path-n">1</div>
      <div class="path-body">
        <p class="path-when">Once</p>
        <h3>Get access to the kit's repo</h3>
        <p>The kit lives in a private GitHub repo. If you do not have a GitHub account, make a free one at github.com. Send Avi your GitHub username; he adds you to the repo. Accept the invitation from the email GitHub sends you.</p>
      </div>
    </li>
    <li>
      <div class="path-n">2</div>
      <div class="path-body">
        <p class="path-when">Once</p>
        <h3>Install the plugin in Claude</h3>
        <p>In Claude, open Customize, then Plugins, then Add marketplace. Enter <code>__MARKET__</code> and add it. Install <b>Kicksaw Project Start Motion</b> from that marketplace, and turn on <b>Sync automatically</b> so each weekly release reaches you without doing anything. One install covers chat, Cowork and Claude Code on the same account.</p>
      </div>
    </li>
    <li>
      <div class="path-n">3</div>
      <div class="path-body">
        <p class="path-when">Once</p>
        <h3>Connect the tools the stages read</h3>
        <p>In Claude's settings, under Connectors, connect Google Drive (the client folder, the templates and the requirements list), Gmail and Slack (what the client and the team said between calls), tl;dv (call transcripts) and Jira (user stories). Notion is useful for the Closed Won task. A stage that finds one missing says so and carries on with what it has.</p>
      </div>
    </li>
    <li>
      <div class="path-n">4</div>
      <div class="path-body">
        <p class="path-when">Check</p>
        <h3>Type / in a new chat</h3>
        <p>The commands appear: <code>/new-client</code>, <code>/handoff</code>, <code>/kickoff</code>, <code>/discovery-plan</code>, <code>/discovery-call</code>, <code>/readout</code>, <code>/design</code>, <code>/user-stories</code>. In Cowork and Claude Code the same commands carry the prefix, as in <code>/start-motion:kickoff</code>. If nothing appears, the marketplace did not add; check step 2 or ask Avi.</p>
      </div>
    </li>
  </ol>

  <div class="sh-h"><h3>Start a client</h3><p>Once per client. The signed SOW is the only thing you need in hand; everything else sales shared helps, and nothing waits for it.</p></div>
  <ol class="path">
    <li>
      <div class="path-n">1</div>
      <div class="path-body">
        <p class="path-when">Per client</p>
        <h3>Make a Claude Project for the client</h3>
        <p>In Claude, make a new Project named for the client and add the signed SOW and anything sales shared that is a document. Run every stage command inside that Project: the working files the stages keep live there and are read back on every run. Strongly recommended, not required; the kit also runs outside a Project, and in Codex, with the Drive copies as the shared record.</p>
      </div>
    </li>
    <li>
      <div class="path-n">2</div>
      <div class="path-body">
        <p class="path-when">Per client</p>
        <h3>Type <code>/new-client</code></h3>
        <p>It finds the signed SOW and whatever sales shared, finds or makes the client's Drive folder and its Discovery subfolder, checks the Project and the connectors, offers to set up the discovery documents from the SOW, and names the first stage to run: <code>/handoff</code> when sales shared a packet, otherwise <code>/discovery-plan</code>. The same thing by hand: a Drive folder named for the client with a Discovery subfolder, the SOW inside it, then the first stage command; every stage offers to set up what it finds missing.</p>
        <div class="path-actions">
          <button type="button" class="btn primary" id="copyNewClientSkill">Copy the instructions</button>
        </div>
        <details class="peek"><summary>See the instructions</summary>
        <pre class="code skill" id="newClientSkillText"><code>__SKILL__</code></pre>
        </details>
      </div>
    </li>
    <li>
      <div class="path-n">3</div>
      <div class="path-body">
        <p class="path-when">Per client</p>
        <h3>Run the stages in order</h3>
        <p>Each command opens by saying where the client stands against the stage's checklist, asks for its picks in one message, shows its plan, and waits for your go. When it is done it names the next command. The order is below; the stage pages on this site hold the full method and what good looks like.</p>
      </div>
    </li>
  </ol>

  <div class="sh-h"><h3>Where things live</h3><p>So anyone on the client can find the outputs without your Claude Project.</p></div>
  <div class="sh-live">
    <div><b>Your Claude Project</b><p>The working files the stages read back: the Discovery documents note, the session notes, the readout content. One Project per client.</p></div>
    <div><b>The client's Drive folder</b><p>The outputs the team needs, in the Discovery subfolder next to the requirements list: the Discovery documents note, every session note and the readout sign-off record, saved there as they are written. The SOW and whatever sales shared sit in the client folder too.</p></div>
    <div><b>Shared artifacts, linked in Slack</b><p>The kickoff deck, the discovery pages, the readout and its deck, and the solution design are Claude pages and decks, shared with the team and linked in the client's Slack channel.</p></div>
  </div>

  <div class="sh-h"><h3>The stages, in order</h3><p>Select a stage to open it. Stage 4 is a meeting; the readout command carries its record.</p></div>
  <ol class="sh-list">
    <li><span class="n">0</span><div><b>SOW and handoff</b><span>The handoff document on DJ's standard and delivery's questions for sales. Here for visibility; a project never waits for it.</span></div><div class="cmd"><code>/handoff</code><button class="go" type="button" data-go="handoff">Open the stage</button></div></li>
    <li><span class="n">1</span><div><b>Kickoff</b><span>The client-facing kickoff deck from the finished slide templates; you pick the slides, it shows the plan first.</span></div><div class="cmd"><code>/kickoff</code><button class="go" type="button" data-go="kickoff">Open the stage</button></div></li>
    <li><span class="n">2</span><div><b>Discovery</b><span>The discovery plan from the SOW before kickoff and prep before each session; then every call processed the same day into the requirements list, the workflow document and What we heard, with a draft story for every requirement.</span></div><div class="cmd"><code>/discovery-plan</code><code>/discovery-call</code><button class="go" type="button" data-go="discovery">Open the stage</button></div></li>
    <li><span class="n">3</span><div><b>Readout</b><span>The solution readout from the discovery documents: section plan, build, dry run, deck, the readout call and the sign-off request.</span></div><div class="cmd"><code>/readout</code><button class="go" type="button" data-go="readout">Open the stage</button></div></li>
    <li><span class="n m">4</span><div><b>Scope sign-off</b><span>Written sign-off from the named sponsor on a named readout version, before any story goes to Jira.</span></div><div class="cmd"><button class="go" type="button" data-go="signoff">Open the stage</button></div></li>
    <li><span class="n">5</span><div><b>Design</b><span>The solution design on the standard sections, written for the SA and finalized once the scope is signed.</span></div><div class="cmd"><code>/design</code><button class="go" type="button" data-go="design">Open the stage</button></div></li>
    <li><span class="n">6</span><div><b>User stories</b><span>Epics, the stories finished against the signed scope with the client's words, pushed to Jira, refined one sprint ahead.</span></div><div class="cmd"><code>/user-stories</code><button class="go" type="button" data-go="stories">Open the stage</button></div></li>
  </ol>

  <p class="note">Something off, or a step that did not work? Post it in #discovery-skill-feedback in Slack as it happens, in any form, or use the <a href="__FEEDBACK__" target="_blank" rel="noopener">Delivery Kit Feedback page</a>. New feedback is sorted every weekday morning and the page shows what changed. Everything the kit runs on is listed on <button class="go" type="button" data-go="kit">Kit inventory</button>. Plugin <span data-plugin-version="__VERSION__">v__VERSION__</span>.</p>
</section>
"""

SCRIPT = """
<script id="start-here-js">
(function () {
  var cs = document.getElementById('copyNewClientSkill'), src = document.getElementById('newClientSkillText');
  if (!cs || !src) return;
  var label = cs.textContent;
  cs.addEventListener('click', function () {
    var txt = src.textContent;
    function selectIt() { var r = document.createRange(); r.selectNodeContents(src); var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); if (src.closest('details')) src.closest('details').open = true; cs.textContent = 'Selected: press Copy'; }
    try { navigator.clipboard.writeText(txt).then(function () { cs.textContent = 'Copied'; setTimeout(function () { cs.textContent = label; }, 2200); }, selectIt); } catch (e) { selectIt(); }
  });
})();
</script>
"""

slide = (SLIDE.replace('__MARKET__', MARKET).replace('__FEEDBACK__', FEEDBACK)
         .replace('__VERSION__', version).replace('__SKILL__', html.escape(skill, quote=False)))

# 1. the slide, right after Overview
anchor = '<!-- ROLES & TOOLS -->'
need(anchor, 'roles section marker')
page = page.replace(anchor, slide.strip('\n') + '\n\n' + anchor)
print('added: Start here slide')

# 2. the Overview band: a Start here box beside Required
anchor = '<button class="go" type="button" data-go="required" style="color:var(--band-ink);text-decoration-color:var(--teal)">one page</button>.</span></div>'
need(anchor, 'overview band Required box')
page = page.replace(anchor, anchor + '\n    <div class="req"><b>New here</b><span>Set up once and start a client in a few minutes: <button class="go" type="button" data-go="start" style="color:var(--band-ink);text-decoration-color:var(--teal)">Start here</button>.</span></div>')
print('added: Overview band box')

# 3. kit inventory
anchor = "<li><b>7 Kicksaw skills</b><span>Saved once in each person's Claude from the copy boxes, or installed once as the Kicksaw Project Start Motion plugin"
need(anchor, 'kit inventory skills line (run patch-page-work-in-claude.py first)')
page = page.replace(anchor, anchor.replace('7 Kicksaw skills', '8 Kicksaw skills'))

grid_row = '<tr><th scope="row"><a href="#kv-handoff" class="kv-rl" data-kv="handoff">Handoff builder</a></th>'
need(grid_row, 'kit grid handoff row')
page = page.replace(grid_row, '<tr><th scope="row"><a href="#kv-newclient" class="kv-rl" data-kv="newclient">New client setup</a></th><td class="kv-c"><span class="kv-dot m" aria-label="made or run here"></span></td><td class="kv-c"></td><td class="kv-c"></td><td class="kv-c"></td><td class="kv-c"></td><td class="kv-c"></td><td class="kv-c"></td></tr>\n' + grid_row)

list_row = '<tr id="kv-handoff"><td><b>Handoff builder</b>'
need(list_row, 'kit list handoff row')
page = page.replace(list_row, ('<tr id="kv-newclient"><td><b>New client setup</b><span class="st pilot">Pilot</span><code>/start-motion:new-client</code></td>'
    '<td>The client ready for the stage commands: the SOW and whatever sales shared found, the Drive folder and its Discovery subfolder, the Claude Project and connectors checked, the first stage named</td>'
    '<td>Signed SOW</td><td><span class="kv-sns"><button type="button" class="kv-sn m" data-go="start" title="Open Start here">&#9654;</button></span></td>'
    '<td class="kv-acts"><button type="button" class="kv-btn primary" data-copy="newClientSkillText">Copy instructions</button><button type="button" class="kv-btn" data-go="start">Open Start here</button></td></tr>\n') + list_row)

NAMES = [('kicksaw-sales-handoff', '/start-motion:handoff'), ('kicksaw-kickoff-deck', '/start-motion:kickoff'),
         ('kicksaw-discovery-plan', '/start-motion:discovery-plan'), ('kicksaw-discovery-call', '/start-motion:discovery-call'),
         ('kicksaw-solution-readout', '/start-motion:readout'), ('kicksaw-solution-design', '/start-motion:design'),
         ('kicksaw-user-stories', '/start-motion:user-stories')]
for old, new in NAMES:
    code = '<code>%s</code></td>' % old
    need(code, 'kit list code name ' + old)
    page = page.replace(code, '<code>%s</code></td>' % new)

anchor = '<div class="kv-h"><h3>Skills</h3><p>Copy here or on the stage page; it is the same text.</p></div>'
need(anchor, 'kit skills header')
page = page.replace(anchor, '<div class="kv-h"><h3>Skills</h3><p>Installed together as the Kicksaw Project Start Motion plugin (see <button class="go" type="button" data-go="start">Start here</button>), or copied here or on the stage page; it is the same text.</p></div>')

anchor = '<code>Kicksaw Delivery Kit.zip</code> there holds all of them in one download.</p></div>'
need(anchor, 'kit templates note')
page = page.replace(anchor, 'The plugin carries its own copy of each one, and that is what Claude builds from; the Drive folder holds the viewing copies, refreshed with each release.</p></div>')
print('patched: kit inventory')

# 4. the old saved-skill names, everywhere else they are still used (the page prompts say "Use the X skill";
#    the plugin's skills are named by their commands, so the prompts name those). Run before refresh-page-skills.py,
#    which writes the plugin's texts into the copy boxes; those carry the command names already.
for old, new in NAMES:
    n = page.count(old)
    page = page.replace(old, new)
    print('renamed %s -> %s (%d)' % (old, new, n))

# 5. css and script
if '</head>' in page:
    page = page.replace('</head>', CSS + '</head>', 1)
else:
    page = re.sub(r'(<title>.*?</title>)', lambda m: m.group(1) + CSS, page, count=1, flags=re.S)
anchor = '<nav class="pager" aria-label="Slide navigation">'
need(anchor, 'pager')
page = page.replace(anchor, SCRIPT.strip('\n') + '\n\n' + anchor)
open(a.out, 'w', encoding='utf-8').write(page)
print('wrote', a.out, len(page), 'bytes')
