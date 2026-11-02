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
.sh-paths { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; max-width: 1100px; align-items: start; }
.sh-path { border: 1.5px solid var(--rule-strong); border-top: 6px solid var(--teal); border-radius: 10px; padding: 18px 22px 20px; background: var(--bg); min-width: 0; }
.sh-path.claude { border-top-color: var(--drive); }
.sh-tag { font: 700 12px var(--sans); letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin: 0 0 4px; }
.sh-path h3 { font-size: 22px; margin: 0 0 8px; }
.sh-pick { font-size: 14.5px; color: var(--ink-2); margin: 0 0 16px; padding-bottom: 14px; border-bottom: 1px solid var(--rule); }
.sh-pick b { color: var(--ink); }
.sh-path .steps { gap: 12px; }
.sh-path .steps li span { font-size: 14px; }
.sh-path .note { margin-top: 16px; }
.sh-path .peek { margin-top: 14px; }
.band .req + .req { margin-top: 0; }
@media (max-width: 900px) {
  .sh-live { grid-template-columns: minmax(0, 1fr); }
  .sh-list li { grid-template-columns: 34px minmax(0, 1fr); }
  .sh-paths { grid-template-columns: minmax(0, 1fr); }
  .sh-list .cmd { grid-column: 2; align-items: flex-start; }
}
</style>
"""

SLIDE = """
<!-- START HERE -->
<section class="slide" id="start" data-label="Start here" data-n="&#9654;">
  <p class="eyebrow">Start here</p>
  <h2>How to use the kit</h2>
  <p class="lead">The kit is seven stages that take a project from a signed SOW to a build-ready backlog. For each stage, this page holds the method and what good looks like, and a skill in Claude does the work. There are two ways to run a stage, and you can switch between them at any time: <strong>from this page</strong>, where you read the stage and build your request with its builder, or <strong>in Claude</strong>, where you type the stage's command. Both run the same skill and make the same outputs.</p>

  <div class="sh-h"><h3>Set up once</h3><p>Five minutes, on your own Claude account. Both ways need this. The kit installs straight from a public GitHub repo. No GitHub account needed.</p></div>
  <ol class="path">
    <li>
      <div class="path-n">1</div>
      <div class="path-body">
        <h3>Install the plugin from GitHub</h3>
        <p>In Claude, open <b>Customize</b> (top left, in the sidebar), then <b>Plugins</b>. Click <b>Add</b> &gt; <b>Add marketplace</b> &gt; <b>Add from a repository</b>, type <code>__MARKET__</code> and click <b>Sync</b>. <b>Start motion</b> appears on the Plugins page: click <b>Add</b>. Done. It works in chat, Cowork and Claude Code, and updates arrive on their own. Repo: <a href="https://github.com/__MARKET__" target="_blank" rel="noopener">github.com/__MARKET__ &#8599;</a></p>
        <p>On Codex or another tool? <code>npx skills add __MARKET__</code> installs the same skills from the repo.</p>
      </div>
    </li>
    <li>
      <div class="path-n">2</div>
      <div class="path-body">
        <h3>Connect the tools the stages read</h3>
        <p>In Settings, under <b>Connectors</b>, connect Google Drive (the client folder, the templates and the requirements list), Gmail and Slack (what the client and the team said between calls), tl;dv (call transcripts) and Jira (user stories). A stage that finds one missing says so and carries on with what it has.</p>
      </div>
    </li>
    <li>
      <div class="path-n">3</div>
      <div class="path-body">
        <h3>Check it worked: type / in a new chat</h3>
        <p>These commands appear: <code>/new-client</code>, <code>/handoff</code>, <code>/kickoff</code>, <code>/discovery-plan</code>, <code>/discovery-call</code>, <code>/readout</code>, <code>/design</code>, <code>/user-stories</code>. In Cowork and Claude Code the same commands carry a prefix, as in <code>/start-motion:kickoff</code>. If nothing appears, go back to step 1 or ask Avi.</p>
      </div>
    </li>
  </ol>

  <div class="sh-h"><h3>Then pick how you want to work</h3><p>Each column is the whole way, from a new client to the last stage. Neither needs the other, and you can switch at any stage.</p></div>
  <div class="sh-paths">
    <div class="sh-path page">
      <p class="sh-tag">Way 1</p>
      <h3>Work from this page</h3>
      <p class="sh-pick"><b>Pick this if</b> you are new to a stage, or you want to read how it runs and see what good looks like before you ask Claude for anything.</p>
      <ol class="steps">
        <li><div><b>Add your client once.</b><span>The bar at the top of this page ("Your client") takes the client's name and dates once; every prompt on every stage fills in from it.</span></div></li>
        <li><div><b>Set the client up.</b><span>A Google Drive folder named for the client with a Discovery subfolder and the signed SOW inside it, and a Claude Project named for the client with the SOW added to its files. Or type <code>/new-client</code> in Claude and it checks and makes these for you.</span></div></li>
        <li><div><b>Open the stage in the rail above.</b><span>Start at Stage 2, Discovery, to plan discovery from the SOW; Stage 0 is optional, for when sales shared a packet beyond the SOW. Read "How it runs" and "What good looks like".</span></div></li>
        <li><div><b>Build your request on the stage's "How to create it" tab.</b><span>Pick the slides or sections you want, fill the blanks, then press Copy. The prompt names the stage's skill, so Claude knows what to run.</span></div></li>
        <li><div><b>Paste it into Claude, inside the client's Project.</b><span>Claude runs the stage's skill, tells you where the client stands, shows its plan and waits for your go before it writes anything.</span></div></li>
        <li><div><b>Check the result against the stage's bar here.</b><span>Every stage page ends with "done when" lines. When they hold, come back to this page for the next stage.</span></div></li>
      </ol>
      <p class="note">Cannot install the plugin? Each stage's step 1 has "Copy the instructions": paste that into Claude and say "save this as a skill". The prompts then work the same way; Claude will ask for the templates from the <a href="https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh" target="_blank" rel="noopener">Kicksaw Discovery Templates</a> folder in Drive when it needs them.</p>
    </div>
    <div class="sh-path claude">
      <p class="sh-tag">Way 2</p>
      <h3>Work in Claude</h3>
      <p class="sh-pick"><b>Pick this if</b> you know the stages and want to get on with the work. Nothing to copy; the skill asks you for what it needs.</p>
      <ol class="steps">
        <li><div><b>Open Claude in a Project named for the client.</b><span>Make the Project if it does not exist yet and add the signed SOW to its files. Every command runs inside it.</span></div></li>
        <li><div><b>The first time for a client, type <code>/new-client</code>.</b><span>It finds the SOW and whatever sales shared, finds or makes the client's Drive folder and Discovery subfolder, checks your connectors, offers to set up the discovery documents, and tells you which command to run first.</span></div></li>
        <li><div><b>Type the stage's command.</b><span>Usually <code>/discovery-plan</code>; <code>/handoff</code> is optional, for when sales shared a packet beyond the SOW. The commands in order are below.</span></div></li>
        <li><div><b>Answer one message of picks.</b><span>The skill says where the client stands, then asks for everything it needs in one message (the slides, the sections, the few blanks). You answer once.</span></div></li>
        <li><div><b>Say go.</b><span>It reads your answer back in one line, shows its plan and waits. On your go it builds, saves the outputs where the team can find them, and reports what it made and what to check.</span></div></li>
        <li><div><b>Run the next command it names.</b><span>Every report ends with the command that follows. Come to this page whenever you want the why, an example, or the full bar for a stage.</span></div></li>
      </ol>
      <details class="peek"><summary>See the new-client instructions</summary>
      <div class="path-actions"><button type="button" class="btn primary" id="copyNewClientSkill">Copy the instructions</button></div>
      <pre class="code skill" id="newClientSkillText"><code>__SKILL__</code></pre>
      </details>
    </div>
  </div>

  <div class="sh-h"><h3>Where things end up</h3><p>The same places whichever way you work, so anyone on the client can find the outputs without your Claude Project.</p></div>
  <div class="sh-live">
    <div><b>Your Claude Project</b><p>The working files the stages read back: the Discovery documents note, the session notes, the readout content. One Project per client.</p></div>
    <div><b>The client's Drive folder</b><p>The outputs the team needs, in the Discovery subfolder next to the requirements list: the Discovery documents note, every session note and the readout sign-off record, saved there as they are written. The SOW and whatever sales shared sit in the client folder too.</p></div>
    <div><b>Shared pages and decks, linked in Slack</b><p>The kickoff deck, the discovery pages, the readout and its deck, and the solution design are Claude pages and decks, shared with the team and linked in the client's Slack channel.</p></div>
  </div>

  <div class="sh-h"><h3>The stages, in order</h3><p>Select a stage to open its page. Stage 4 is a meeting; the readout command carries its record.</p></div>
  <ol class="sh-list">
    <li><span class="n">0</span><div><b>SOW and handoff</b><span>Optional. When sales shared a packet beyond the SOW: the handoff document on DJ's standard and delivery's questions. Nothing downstream waits for it.</span></div><div class="cmd"><code>/handoff</code><button class="go" type="button" data-go="handoff">Open the stage</button></div></li>
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
