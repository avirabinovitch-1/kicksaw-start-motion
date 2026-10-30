"""Assemble the seven plugin skills from the Start Motion page's skill texts (src/<cmd>.md) plus the
Claude-first additions: a Start section, a one-message intake, plugin-local template paths, a Next line,
the run log. Anchors must match exactly once; the script stops otherwise."""
import re, sys, os

SRC = sys.argv[1] if len(sys.argv) > 1 else 'src'  # folder holding the seven page skill texts as <cmd>.md
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'plugins', 'start-motion', 'skills')
VERSION = 'v0.1.0'
PAGE = 'https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S'

def rep(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit('anchor found %d times, expected %d:\n%s' % (n, count, old[:120]))
    return text.replace(old, new)

def runlog(cmd, stage):
    return f"""## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:{cmd} ({VERSION}) · {stage} · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

"""

METHOD_LINE = "Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page."

THIRD = {'Build or update': 'Builds or updates', 'Build the discovery plan': 'Builds the discovery plan', 'Build the sales-to-delivery': 'Builds the sales-to-delivery',
         'Build, update and present': 'Builds, updates and presents', 'Process a Kicksaw': 'Processes a Kicksaw', 'Draft, update and finalize': 'Drafts, updates and finalizes',
         'Finish, refine, split and push': 'Finishes, refines, splits and pushes'}
def frontmatter(text, name, desc_prefix):
    m = re.match(r'---\nname: [^\n]+\ndescription: ([^\n]+)\n---\n', text)
    if not m:
        sys.exit('frontmatter not matched for ' + name)
    d = m.group(1)
    for a, b in THIRD.items():
        if d.startswith(a):
            d = b + d[len(a):]; break
    else:
        sys.exit('description not in the third-person table: ' + d[:40])
    desc = desc_prefix + ' ' + d
    return '---\nname: %s\ndescription: %s\n---\n' % (name, desc) + text[m.end():]

# ---------------------------------------------------------------- discovery-call
def discovery_call(t):
    t = frontmatter(t, 'discovery-call', 'Start Motion stage 2 (/start-motion:discovery-call).')
    start = f"""## Start: where the client stands

{METHOD_LINE}

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere.

1. Read the Discovery documents note in the client's Claude Project (section 0 below). If it is there, read the plan's session list (the `dp-data` block) and the requirements list's Sessions and sources tab, and report in three lines before doing anything else: the last session processed (plan ID, name, date, S-ID); the next session on the plan; what is open (blocking questions, overdue inputs). For example: "Tog. Last processed: D3 Workflow deep dive, Oct 28 (S-05). Next on the plan: D4 Systems and data, Nov 3. Open: two blocking questions, one input overdue."
2. If the note is not there and nothing turns up in the person's artifacts or Drive, say so and offer setup right there: "No discovery documents for [Client] yet. Want me to set them up from the SOW?" Setup is what this skill does when the documents do not exist; it is not a separate request anyone has to know about.
3. If the plan shows the call in the request already processed, say so. Never process a call twice.

## What to ask: one message

This stage has almost no picks. Ask once, in one message, and only for what the Start did not find:
- Processing a call: which call. Today's call is the default; a date or a pasted transcript overrides it. If tl;dv has more than one call for that client that day, list them and ask which.
- Setup: the client's Drive folder (only if no folder named for the client turns up), and whether to build the discovery plan now or later.

The standing instructions people used to paste from the page (propose every change before writing anything; flag anything past the SOW or at a SOW limit such as rule counts, integration endpoints, source files or licenses, with the quote and timestamp, so the SC can raise it with the PM that week) are rules of this skill below; nobody types them.

Then read back what you heard in one line and run: "Processing Tog, Oct 30, D4 Systems and data, S-06. Proposals first; nothing is written until you accept."

"""
    t = rep(t, "## Setting up a new client (once, before the first discovery session)\n", start + "## Setting up a new client (once, before the first discovery session)\n")
    t = rep(t, 'One request ("process today\'s [Client] call") updates the documents that grow during discovery. Ask only if more than one call for that client happened that day and it is unclear which one is meant.',
            'One request ("process today\'s [Client] call") updates the documents that grow during discovery. What to ask, and when, is in "What to ask" below.')
    t = rep(t, "Ask the SC only for what none of these say.", "Ask the SC only for what none of these say, in the one message \"What to ask\" describes.")
    t = rep(t, "written to the standard in the Kicksaw user stories skill (Stage 6 on the Start Motion page), so the stories are close to ready for Jira by sign-off. That skill is the full standard; the rules below are the ones that matter at this stage. If that skill is not saved, the rules below are enough to draft from.",
            "written to the standard in `/start-motion:user-stories` (its SKILL.md is the full standard; it ships in the same plugin), so the stories are close to ready for Jira by sign-off. The rules below are the ones that matter at this stage.")
    old_tpl = t[t.index("The templates are files in one shared Google Drive folder"):t.index("- `primary-full-color.svg` and `primary-inverse.svg` (the Kicksaw logo files all three pages load as `brand/...`)\n") + len("- `primary-full-color.svg` and `primary-inverse.svg` (the Kicksaw logo files all three pages load as `brand/...`)\n")]
    new_tpl = """The page templates ship with this skill, in this skill's folder:
- `templates/Kicksaw Workflow Document.template.html` (the page source, with its `wf-data` block)
- `templates/Kicksaw What We Heard.template.html` (the page source, with its `wwh-data` block)
- `brand/primary-full-color.svg` and `brand/primary-inverse.svg` (the Kicksaw logo files all three pages load as `brand/...`)
- `references/discovery-documents-note.md` (the shape of the Discovery documents note written in step 5)

The discovery plan template is in the discovery-plan skill's folder (it is the plan skill that fills it). Use these copies; never take a template from anyone's artifact. The requirements list is the exception: it is a Google Sheet, `Kicksaw Requirements List: Template`, in the shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh), and is always copied in Drive. That folder also holds viewing copies of the page templates for anyone who wants to look at them; the plugin's copies are what Claude builds from.
"""
    t = rep(t, old_tpl, new_tpl)
    t = rep(t, "Download `Kicksaw Workflow Document.template.html` and the two logo files from the folder into the workspace.", "Copy `templates/Kicksaw Workflow Document.template.html` and the two logo files in `brand/` from this skill's folder into the workspace.")
    t = rep(t, "The same with `Kicksaw What We Heard.template.html`", "The same with `templates/Kicksaw What We Heard.template.html`")
    t = rep(t, "Run the discovery plan skill (\"plan discovery for [Client]\")", "Run `/start-motion:discovery-plan` (\"plan discovery for [Client]\")")
    t = rep(t, "in this shape: a table of each document", "in the shape of `references/discovery-documents-note.md`: a table of each document")
    t = rep(t, "6. Report the links and remind the SC to share the workflow and What we heard pages",
            """   Then save the same note as a Google Doc, "Discovery documents: [Client]", in the client's Drive folder, in the same Discovery subfolder as the requirements list, so anyone on the client can find where everything is. The project copy is the one the skills work from; the Drive copy is updated whenever the project copy changes (a new link, a changed setting, a new person).
6. Report the links and remind the SC to share the workflow and What we heard pages""")
    t = rep(t, "If the note is missing, search the SC's artifacts and Drive for", "If the note is missing from the project, look for the Google Doc \"Discovery documents: [Client]\" in the client's Drive folder (the Discovery subfolder) and use it; it holds the same links. If neither exists, search the SC's artifacts and Drive for")
    t = rep(t, "End the note with an internal \"Build notes\" section for things that are not requirements: data sources and export paths, environment facts, limits, approvals, risks. These never go in the client-facing documents.",
            "End the note with an internal \"Build notes\" section for things that are not requirements: data sources and export paths, environment facts, limits, approvals, risks. These never go in the client-facing documents.\n\nSave the session note in the project, and also as a Google Doc with the same name in the client's Drive folder, in the Discovery subfolder next to the requirements list, so the PM and the SA can read it without the SC's project. The two copies say the same thing; the project copy is the one later runs read.")
    t = rep(t, "If the folder or one of its files cannot be opened, say which one and stop; do not rebuild a template from memory. If the folder is not visible to the person running this, they need view access to it from whoever owns the folder (Avi Rabinovitch today).",
            "If a template file cannot be opened, say which one and stop; do not rebuild a template from memory. If the requirements list template in Drive is not visible to the person running this, they need view access to the folder from whoever owns it (Avi Rabinovitch today).")
    t = rep(t, "the SC runs \"prep me for [Client] [session]\" from the discovery plan skill", "the SC runs `/start-motion:discovery-plan` (\"prep me for [Client] [session]\")")
    t = rep(t, "Then the items not applied and why, and any coverage gaps still open. No recap of steps.",
            "Then the items not applied and why, and any coverage gaps still open. No recap of steps.\n\nEnd with one line naming what comes next: the day before the next session, `/start-motion:discovery-plan` preps it (\"prep me for [Client] [session]\"); when the bar in `references/method.md` is met and the discovery playback is held, `/start-motion:readout`.")
    t = rep(t, "## Rules\n", runlog('discovery-call', 'discovery') + "## Rules\n")
    return t

# ---------------------------------------------------------------- discovery-plan
def discovery_plan(t):
    t = frontmatter(t, 'discovery-plan', 'Start Motion stage 2 (/start-motion:discovery-plan).')
    start = f"""## Start: where the client stands

{METHOD_LINE}

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else.

- "Plan discovery for [Client]": the signed SOW (found, and which edition); the sales and pre-kickoff calls (how many, which have transcripts, which do not); the handoff doc or IKT (found or none); client documents in the folder; whether the discovery documents exist yet (the Discovery documents note and the requirements list); and whether a plan already exists for this client (then this is an update, say so and change only what is asked). For example: "Tog. SOW found (Oct 3 edition). Calls: four in Sales Notes, three with transcripts, one MP4 with no transcript. Handoff doc: none. Discovery documents: set up Oct 20. No plan yet."
- "Prep me for [Client] [session]": the session on the plan (ID, name, date, attendees); the last call processed and whether anything since is unprocessed; inputs the session depends on and which have arrived; what the client has been told about it.
- No discovery documents yet: say so and offer to set them up first (`/start-motion:discovery-call` does it from the SOW), because the plan seeds the requirements list's Open items and Sessions and sources tabs and cannot finish without the sheet.

## What to ask: one message

Ask once, in one message, and only for what the Start did not find:
- Building the plan: the discovery window (weeks or dates), the session days, remote or on site or mixed, and anything the SC already knows about the people, the politics and the constraints. The page prompt carried these as blanks; here they are the questions.
- Prepping a session: nothing beyond the session, unless the request did not name one.

Then read back what you heard in one line and run: "Planning Tog discovery: four weeks from Nov 10, Tuesdays and Thursdays, remote. Reading the SOW and three calls."

"""
    t = rep(t, "## Where things live\n", start + "## Where things live\n")
    t = rep(t, "| The template | `Kicksaw Discovery Plan.template.html` in the shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh), next to the workflow and What we heard templates and the two logo files. Preview: https://claude.ai/artifact/DG9bga86fMsBuVRY5NYu1t |",
            "| The template | `templates/Kicksaw Discovery Plan.template.html` in this skill's folder, with the two logo files in `brand/`. A viewing copy sits in the shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh); the plugin's copy is what Claude builds from. Preview: https://claude.ai/artifact/DG9bga86fMsBuVRY5NYu1t |")
    t = rep(t, "- Take `Kicksaw Discovery Plan.template.html` and the two logo files from `Kicksaw Delivery Kit.zip` in the Drive folder (one download that saves as a file; unzip it), or download them separately if the zip is missing. Never take them from anyone's artifact.",
            "- Take `templates/Kicksaw Discovery Plan.template.html` and the two logo files in `brand/` from this skill's folder. Never take them from anyone's artifact.")
    t = rep(t, "If the requirements list does not exist yet, run the discovery call skill's setup first.", "If the requirements list does not exist yet, run `/start-motion:discovery-call` setup first.")
    t = rep(t, "Keep the plan's internal notes out of anything client-facing.\n",
            "Keep the plan's internal notes out of anything client-facing.\n\nEnd with one line naming what comes next: `/start-motion:kickoff` builds the kickoff deck, and its Discovery sessions slide takes the session list above; if the discovery documents are not set up yet, `/start-motion:discovery-call` sets them up from the SOW.\n")
    t = rep(t, "- Reply with the link, and remind the SC to use the Share menu before sending the deck to the client.\n",
            "- Reply with the link, and remind the SC to use the Share menu before sending the deck to the client.\n\nWhether or not a deck was built, end the prep with one line naming what comes next: after the session, `/start-motion:discovery-call` processes the call the same day.\n")
    t = rep(t, "## Rules\n", runlog('discovery-plan', 'discovery') + "## Rules\n")
    t = rep(t, "the Look section of the kickoff deck skill", "the kickoff skill's design rules (`/start-motion:kickoff`, its `references/kickoff-templates.md`)")
    return t

# ---------------------------------------------------------------- readout
def readout(t):
    t = frontmatter(t, 'readout', 'Start Motion stage 3 (/start-motion:readout).')
    start = f"""## Start: where the readout stands

{METHOD_LINE}

This skill covers five moves that are five separate prompts on the page: the section plan and build, the dry run, cutting the deck, the readout call, and sign-off. Work out which one is next from where the readout stands, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Read the Discovery documents note, the three discovery documents, the client settings in the note, and the readout files in the client's project if they exist (readout/manifest.md, readout/content.json, readout/sign-off.md). Then report against the stage's readiness list, in a few lines, before doing anything else:

- the discovery documents: current to which call, and none still a template
- requirements: how many confirmed, how many heard (those show as provisional), whether every row has a priority
- workflows: how many, by W-ID
- calls: how many on Sessions and sources, and whether every one has a tl;dv link
- the SOW, and the handoff packet if there is one
- client settings: what we heard played back or future state only; dates solid or not; who presents, to whom
- the dry run, the presentation and the two working sessions: on the calendar or not
- the readout itself: none yet, or its version, section count, whether the deck is cut, whether the dry run and the readout call have been processed, whether sign-off is recorded
- and the move that is next

For example: "Tog. Discovery documents current to S-09 (Nov 20); none still a template. Requirements: 41 confirmed, 6 heard, every row with a priority. Workflows: five (W-01 to W-05). Calls: nine, all with a tl;dv link. SOW found. Client settings: play back what we heard; dates not decided; the SC presents to the sponsor and the product owner. Dry run not on the calendar yet. No readout yet. Next: the section plan." Or later: "Tog. Readout v1.0 built Nov 24, 13 sections, deck not cut. Dry run was Nov 26 in tl;dv and has not been processed. Next: process the dry run?"

If a document is missing or still a template, say which and stop (section 0). Nothing is built from memory or transcripts.

## What to ask: the section list in one message

Only the first move, the section plan, has picks. The other four take the recording or the feedback and need nothing picked. When no section list was given, show the page's section picker as one message and let the SC answer once:

```
Two settings, from the Discovery documents note; change them here if they are wrong:
What we heard: [play back what we heard | future state only | not decided]. Playing it back means 02 and 03 come straight from the What we heard page.
Dates: [solid | a dependency sets the pace | not decided]. Solid means the next steps get dates and a timeline; a dependency means no dates and the dependency is named.

Sections, in readout order. Always-in sections stay in; optional ones are out unless you add them. Numbers are fixed; a section left out keeps its number.

Overview
01 Executive summary
What we heard (in as a group; out as a group for future state only)
02 What we heard
03 Pain points and the response
04 Current state, optional
What we will build
05 Recommended build
06 How it comes together
07 Target operating model, optional (when roles or teams change)
08 Future state workflows
Example journeys inside 08, optional (when one journey carries the solution)
Scope
09 Scope at a glance
10 Future phase: roadmap items, optional (when scope was split or something past the SOW came up)
The road ahead
11 Aligning with the SOW
12 Success measures
13 Design decisions to close
14 Inputs needed from the client
15 Next steps
Reference
A Workflows today, optional (with 04, when today's process needs to be on record)
B Link to the requirements list

Workflows to draw in 08: [list every W-ID and name from the workflow document]. Name the ones to draw and any that go to the appendix; otherwise I propose them in the plan.

Anything else I should know (who signs, what the sponsor cares about, anything the client asked to see)?
```

The two settings are the one place a default appears, because the SC answered them when the documents were set up and the note holds the answer; say where they came from. When the note does not have them, they read "not decided" and are asked plainly. Read the answer back in one line ("Tog readout. What we heard played back, dates solid. 15 sections plus example journeys; W-01, W-02 and W-04 drawn, W-03 and W-05 in the appendix. Section plan next."), then propose the cut (section 2) and wait.

The standing instructions people used to paste from the page (propose the section plan first and wait for confirmation; the three approvals and the sign-off date in the plan; the judgment items drafted for the SC to edit) are already in this skill; nobody types them.

"""
    t = rep(t, "## Where the template lives\n", start + "## Where the template lives\n")
    old = t[t.index("The shared Google Drive folder **Kicksaw Discovery Templates**"):t.index("## 0. Load the three discovery documents")]
    new = """This skill's folder carries everything the build needs:
- `templates/Kicksaw Solution Readout.template.html`: the page shell (styles, renderer, an empty `ro-data` block)
- `scripts/build-readout.py`: merges the content file, the workflow data and the What we heard data into the page, runs the checks, and writes the client's page
- `references/content-example.json`: a filled example of the content file
- `brand/primary-full-color.svg` and `brand/primary-inverse.svg`: the logo files every page loads as `brand/...`

Use these copies, never anyone's artifact. The shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh) holds viewing copies of the same files. If a file cannot be opened, say which and stop; do not rebuild the template from memory.

"""
    t = rep(t, old, new)
    t = rep(t, "the prompt from the section picker on the Kicksaw Delivery Start Motion page", "the prompt from the section picker on the Start Motion page")
    t = rep(t, "## 5. Cut the deck\n", """## 4b. Process the dry run

When asked ("process today's [Client] readout dry run"): pull the dry run recording from tl;dv (if more than one call for the client happened that day, ask which). Propose the cuts and corrections it decided, to the section plan (what the deck keeps, what moves to the appendix, the sign-off date) and to the content file, and wait for the SC's OK. Then apply them to readout/manifest.md and readout/content.json, bump the version (v1.1), list the changes in `project.updated`, rebuild the page, and report what changed. The deck is cut only after this, so it carries exactly what the dry run kept.

## 5. Cut the deck
""")
    t = rep(t, "- Draft the answers the SC and SA agree on, then fold them into the three documents and into content.json.", "- Draft the answers the SC and SA agree on; the two working sessions with the client lead are where they are settled. Fold them into the three documents and into content.json.")
    t = rep(t, "Copy `Kicksaw Solution Readout.content-example.json` as the starting shape the first time", "Copy `references/content-example.json` from this skill's folder as the starting shape the first time")
    t = rep(t, "Download `Kicksaw Solution Readout.template.html` and `build-readout.py` from the Drive folder into the workspace, next to the saved page sources", "Copy `templates/Kicksaw Solution Readout.template.html` and `scripts/build-readout.py` from this skill's folder into the workspace, next to the saved page sources")
    t = rep(t, "First build: a new artifact, with the two logo files from the Drive folder passed in `files`", "First build: a new artifact, with the two logo files from this skill's `brand/` folder passed in `files`")
    t = rep(t, "file the approval (or a link to it) in the client's Claude Project as readout/sign-off.md, and say so in the report. Only then does the user stories skill read the list.",
            "file the approval (or a link to it) in the client's Claude Project as readout/sign-off.md and as a Google Doc \"Readout sign-off: [Client]\" in the client's Drive folder (the Discovery subfolder, next to the requirements list), so the PM has it without the SC's project, and say so in the report. Only then does `/start-motion:user-stories` read the list.")
    t = rep(t, "Then every CHECK the build printed that is not fixed, and every placeholder still to fill. No recap of steps.",
            """Then every CHECK the build printed that is not fixed, and every placeholder still to fill. No recap of steps.

End with one line naming what comes next, by move:
- after the build: the SA reviews the build, then the dry run (15 to 20 minutes, recorded); after it, `/start-motion:readout` again to process the recording
- after the dry run is processed: `/start-motion:readout` to cut the deck
- after the deck: present; the same day, `/start-motion:readout` to process the readout call
- after the readout call: the two working sessions, then `/start-motion:readout` to finalize for sign-off
- after the sign-off is recorded: `/start-motion:design` finalizes the design against the signed scope, and `/start-motion:user-stories` reads the list only after this""")
    t = rep(t, "## Rules\n", runlog('readout', 'readout') + "## Rules\n")
    return t

# ---------------------------------------------------------------- kickoff
def kickoff(t):
    t = frontmatter(t, 'kickoff', 'Start Motion stage 1 (/start-motion:kickoff).')
    t = rep(t, "Where the templates live: the delivery kit plugin carries `templates/kickoff/`, `icons/`, `brand/` and `kickoff-templates.md`. The Kicksaw Slides design system (https://claude.ai/artifact/Dz63JoG9fN8CMu86q1sB7a) holds the master copy; when the plugin copy is not there, read the same files from the design system. If neither can be opened, say so and stop before building: a deck drawn without the templates is not the standard.",
            "Where the templates live: this skill's folder carries `templates/kickoff/` (every slide as a finished file), `templates/kickoff-manifest.json`, `icons/` (the white glyphs), `brand/` (the logo files and the icon mark), `references/kickoff-templates.md` (how a deck is built from the templates, when to use each one, its limits, the swap rule and the icon list), and `tokens.json` and `design-system.json` (the Kicksaw Slides design system's tokens). The Kicksaw Slides design system (https://claude.ai/artifact/Dz63JoG9fN8CMu86q1sB7a) holds the master copy; the plugin's files are what you build from. The topographic pattern files (`brand/topo-white.png`, `brand/topo-navy.png`) are in the design system only; when they cannot be read, build without the pattern and say so in the report. If the templates cannot be opened at all, say so and stop before building: a deck drawn without the templates is not the standard.")
    start = f"""## 0. Start: where the client stands

{METHOD_LINE}

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the signed SOW (found, and its date); the handoff packet (found or none); the Kicksaw team (who is named, and where); the client team (sponsor, champion, SMEs named or not); the discovery plan (built, with how many sessions, or not yet); the phase plan (go-live and break weeks firm or not); images (client logo in the folder or not; headshots from the deck library); the kickoff date (set or not); and whether a kickoff deck already exists for this client (then the request is a change to it, section 1). For example: "Tog. Signed SOW: found (Oct 3). Handoff packet: none. Kicksaw team: four people named in the SOW. Client team: sponsor and champion named; no SMEs yet. Discovery plan: built, nine sessions. Phase plan: go-live in the SOW, break weeks not set. Images: client logo in the Drive folder. Kickoff date: not set. No kickoff deck yet."

If no discovery plan exists, say that the Discovery sessions slide (the one slide that is never dropped) will carry placeholders, and offer to run `/start-motion:discovery-plan` first.

## What to ask: the slide list in one message

When no slide list was given, show the page's slide picker as one message and let the person answer once. Core slides are in unless they take them out; optional ones are out unless they add them; A is the standard layout and a letter changes it; the owner in brackets presents it.

```
Kickoff date: a Monday.

Slides, in deck order. Core slides are in unless you take them out; optional ones are out unless you add them. Where a slide has two layouts, A is the standard; name the letter to change it.

1. Title: A navy with blades, B white with the mark [PM]
2. Agenda: A navy list, B white path [PM]
3. Why we're here: A numbers and problems, B icon rings [SC]
4. Goals and success [SC]
   optional: A client quote [SC]
   optional: Win themes [SC]
5. Meet the Kicksaw team: A cards, B table [PM]
6. Meet the client team: A navy cards, B who works with whom [PM]
7. What we're building [SC]
   optional: What it can look like (screenshots) [SC]
   optional: Timeline: A Gantt, B phase band [PM]
   optional: Week by week calendar [PM]
8. How we work: A flow and story, B cycle [SC]
   optional: Salesforce terms in plain language [SC]
   optional: Client time commitments by role [PM]
   optional: Pre-discovery playback [SC]
9. Discovery sessions, always in [SC]
   optional: Discovery playback preview [SC]
10. Communication and tools [PM]
11. Risks and how the client can help: A rows, B cards [PM]
12. Next steps: A by date, B path [PM]
13. Questions and thank you: A navy, B white [All]

To see every layout: the Kicksaw Kickoff Deck Library, https://claude.ai/artifact/EooMRC9rhebaLnRQzEBvce

Anything else I should know (who opens the call, how long, anything about the sponsor)?
```

Read the answer back in one line ("Tog kickoff, Monday Nov 10. 14 slides: the core 13 without Risks, plus A client quote and Timeline (B), Title in B. Plan next."), then show the plan (section 2) and build on a yes. Two stops, picks then plan, the same as the page.

"""
    t = rep(t, "## 1. Start from whatever was given\n", start + "## 1. Start from whatever was given\n")
    t = rep(t, "- **Only a client name.** Look up the signed SOW first,", "- **Only a client name.** Ask for the picks as in \"What to ask\" above, then look up the signed SOW first,")
    t = rep(t, "Ask at most three short multiple-choice questions, and only ones whose answer changes the deck.", "The picks are already given, so the plan is the last stop: ask a question in it only when a pick does not fit this client or a source leaves a gap that changes the deck, and at most three.")
    t = rep(t, "the prompt from the slide picker on the Kicksaw Delivery Start Motion page", "the prompt from the slide picker on the Start Motion page")
    t = rep(t, "- Presenter names go in the speaker notes, never on the slide.\n",
            "- Presenter names go in the speaker notes, never on the slide. The agenda slide shows topics only.\n- The EM/DM opens the call and sales introduces the team; say so in the Title and Agenda speaker notes. On Communication and tools, show the executive checkpoint and the weekly playback with the client lead.\n")
    t = rep(t, "Create the deck and install the Kicksaw Slides design system's tokens. Read `kickoff-templates.md` before writing anything.",
            "Create the deck and apply the tokens in this skill's `tokens.json` (the Kicksaw Slides design system's tokens) the way the Slides type's instructions say; if the design system artifact itself can be opened, applying it is the same thing. Read `references/kickoff-templates.md` before writing anything.")
    t = rep(t, "Icons: choose from the list in `kickoff-templates.md`", "Icons: choose from the list in `references/kickoff-templates.md`")
    t = rep(t, "the limits are in `kickoff-templates.md`", "the limits are in `references/kickoff-templates.md`")
    t = rep(t, "Remind the person to use the Share menu before sending the deck to the client, and that any layout can be swapped by asking (\"switch the timeline to B\").",
            "Remind the person to use the Share menu before sending the deck to the client, and that any layout can be swapped by asking (\"switch the timeline to B\").\n- End with one line naming what comes next: the day before the reverse demo, `/start-motion:discovery-plan` preps it (\"prep me for [Client] D1\"); if the discovery documents are not set up yet, `/start-motion:discovery-call` sets them up from the SOW.")
    t = t.rstrip('\n') + '\n\n' + runlog('kickoff', 'kickoff').rstrip('\n') + '\n'
    return t

# ---------------------------------------------------------------- handoff
def handoff(t):
    t = frontmatter(t, 'handoff', 'Start Motion stage 0 (/start-motion:handoff).')
    start = f"""## Start: where the packet stands

{METHOD_LINE}

This skill covers three moves that are three separate prompts on the page: building the handoff document (sales), drafting delivery's questions (the SC, PM, SA and EM/DM), and updating the document from the recorded handoff call. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the sales call transcripts (how many, in which folder, named by date and call or not, and any recording with no transcript); the signed SOW (found, and whether it is the countersigned final); the contractual documents (MSA, order form, BAA when PHI is in scope, NDAs, amendments: which are there); the handoff doc (exists on DJ's standard, exists in another shape, or none); named client contacts; the handoff call (booked, and whether it is at least 24 hours after the packet). For example: "Tog. Transcripts: three Chorus exports in 02 Sales calls, one MP4 with no transcript. SOW: countersigned Oct 3. Contracts: MSA and order form present; BAA not in the folder and PHI is in scope. Handoff doc: none. Contacts: sponsor named in the SOW. Handoff call: not booked. Next: build the handoff document."

## What to ask: one message

Ask once, in one message, and only for what the Start did not find: the client's handoff folder when none turns up under the client's name, and the transcript of any recording that has none. Nothing else; the document is built from what is there, and the gaps are flagged in it.

Then read back what you heard in one line and run: "Building the Tog handoff document from the SOW, the order form and three transcripts. The BAA and one transcript are flagged as missing."

"""
    t = rep(t, "## 0. Gather the packet\n", start + "## 0. Gather the packet\n")
    t = rep(t, "## 5. Deliver\n", """## 4b. Delivery's questions, when delivery asks

When the SC, PM, SA or EM/DM asks ("read the [Client] handoff packet and draft the questions delivery should ask sales"): read the packet, including the handoff doc if sales already built it, and draft the questions only this packet raises, nothing a transcript already answers, grouped by why they bought, people, what was promised, how it was sized, the environment and watch-outs, with what prompted each one. Keep it to the 10 to 15 questions only sales can answer, most important first, and move anything only the client can answer to the open decisions for kickoff. If the handoff doc exists, write them into its Delivery questions section; otherwise hand them back in chat for the team to send to sales ahead of the call.

## 5. Deliver
""")
    t = rep(t, "Ask once, in one message, and only for what the Start did not find: the client's handoff folder when none turns up under the client's name, and the transcript of any recording that has none. Nothing else; the document is built from what is there, and the gaps are flagged in it.",
            "Ask once, in one message, and only for what the Start did not find: the client's handoff folder when none turns up under the client's name, the transcript of any recording that has none, and a readable copy of any packet file that cannot be opened (section 0 stops on those). Nothing else; the document is built from what is there, and the gaps are flagged in it.")
    t = rep(t, "Remind sales to share the packet at least 24 hours before the handoff call.",
            "Remind sales to share the packet at least 24 hours before the handoff call. End with one line naming what comes next: delivery reads the packet and runs `/start-motion:handoff` to draft its questions for sales; after the recorded call, `/start-motion:handoff` folds the answers in.")
    t = rep(t, "if it does not, tell the PM it needs creating.",
            "if it does not, tell the PM it needs creating. End with one line naming what comes next: once the SC and PM accept the packet, `/start-motion:kickoff` builds the kickoff deck, and `/start-motion:discovery-plan` plans discovery from the same folder.")
    t = rep(t, "## Rules\n", runlog('handoff', 'handoff') + "## Rules\n")
    return t

# ---------------------------------------------------------------- design
def design(t):
    t = frontmatter(t, 'design', 'Start Motion stage 5 (/start-motion:design).')
    start = f"""## Start: where the design stands

{METHOD_LINE}

This skill covers three moves that are three separate prompts on the page: starting the draft, keeping it current from calls and decisions, and getting it ready to share once scope is signed. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the signed SOW; the discovery documents (current to which call; the Integrations and Open items tabs; the data list if there is one); the readout (none, draft at which version, or signed on which date); the current org (access or not, when the client already runs Salesforce); third-party contacts and any access worksheet or data dictionary; and whether a design already exists (then its status, Draft or Final, and the TBDs still open). For example: "Tog. SOW found. Discovery documents current to S-09. Readout v1.1, not yet signed. Org: client runs Salesforce, access not granted. Design: draft started Nov 18, 14 TBDs open, 3 answered on calls since. Next: fold in the calls since Nov 18."

## What to ask: one message

Ask once, in one message, and only for what the Start did not find. Starting the draft needs nothing beyond the client; organized by capability or by integration is proposed in the section plan (section 1), not asked. Updating needs nothing; the calls since the last update are read. Getting it ready to share needs the readout version that was signed, if readout/sign-off.md does not say.

Then read back what you heard in one line and run.

"""
    t = rep(t, "## 0. Load what you need\n", start + "## 0. Load what you need\n")
    t = rep(t, "what is still TBD and who answers each one, and what the SA should check. No recap of steps.",
            "what is still TBD and who answers each one, and what the SA should check. No recap of steps.\n\nEnd with one line naming what comes next: after the first draft, keep it current with `/start-motion:design` after each systems session, third-party call or decision; after scope sign-off, `/start-motion:design` gets it ready to share and the SC, PM and build lead review it; once it is shared, `/start-motion:user-stories` writes the stories with the design in hand.")
    t = rep(t, "## Rules\n", runlog('design', 'design') + "## Rules\n")
    return t

# ---------------------------------------------------------------- user-stories
def user_stories(t):
    t = frontmatter(t, 'user-stories', 'Start Motion stage 6 (/start-motion:user-stories).')
    start = f"""## Start: where the backlog stands

{METHOD_LINE}

This skill covers five moves that are five separate prompts on the page: proposing the epics, finishing the stories epic by epic, pushing approved stories to Jira, prepping refinement, and folding a refinement session in. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: written sign-off on a named readout version (recorded, or not); the requirements list (how many approved, how many still heard or confirmed, whether the User stories tab exists and how many drafts it holds); every discovery call on Sessions and sources with its tl;dv link (any missing); the client's Jira project and its key (and what is already in it); the product owner (named in the note or not); the solution design (shared, draft, or none); refinement sessions on the calendar or not; and the epic plan (stories/epic-plan.md exists or not, and which epics are finished, pushed or refined). For example: "Tog. Sign-off recorded Dec 4 on readout v1.2. Requirements: 38 approved, 5 confirmed (stay on the sheet). User stories tab: 41 drafts. Calls: all nine linked. Jira: TOG, empty. Product owner: Dana Ruiz. Design: shared Dec 3. Epic plan: none yet. Next: propose the epics."

If the readout is not signed, or there are no approved requirements, say so and stop (section 0).

## What to ask: one message

Ask once, in one message, and only for what the Start did not find: the epic to finish next when more than one is open and the request did not name it; the product owner when the note does not name them; the Jira project key when none is found. Everything else comes from the documents.

Then read back what you heard in one line and run: "Finishing the Tog stories for the Lead intake epic, six drafts, one at a time for your review."

"""
    t = rep(t, "## 0. Load the signed scope, the drafts and the calls\n", start + "## 0. Load the signed scope, the drafts and the calls\n")
    t = rep(t, "(readout/content.json and readout/sign-off.md in the client's Claude Project)", "(readout/content.json and readout/sign-off.md in the client's Claude Project; when the sign-off file is not in the project, the Google Doc \"Readout sign-off: [Client]\" in the client's Drive folder holds the same record)")
    t = rep(t, "the Jira project key when none is found. Everything else comes from the documents.", "the Jira project key when none is found; and, when folding in a refinement session, which call, if more than one for the client happened that day. Everything else comes from the documents.")
    t = rep(t, "Before showing the SC anything for an epic, have a separate reviewer agent read that epic's stories cold against the transcripts and the readout and report defects only; reconcile first.",
            "Before showing the SC anything for an epic, have that epic's stories read cold against the transcripts and the readout for defects only (a separate reviewer agent where one is available, otherwise a second pass of your own from the transcripts, not from memory); reconcile first.")
    t = rep(t, "and any quote that could not be found in the transcript. No recap of steps.",
            "and any quote that could not be found in the transcript. No recap of steps.\n\nEnd with one line naming what comes next, by move: after the epic plan, `/start-motion:user-stories` finishes the stories epic by epic; after the SC approves a story, `/start-motion:user-stories` creates it in Jira; before each refinement session, `/start-motion:user-stories` preps it; the same day after it, `/start-motion:user-stories` folds the answers in; once sprint 1 is refined, the SA adds build details and sizes the stories with the SC, and the PM loads the sprint.")
    t = rep(t, "## Reference\n", runlog('user-stories', 'stories') + "## Reference\n")
    return t

BUILD = {
    'handoff': handoff, 'kickoff': kickoff, 'discovery-plan': discovery_plan, 'discovery-call': discovery_call,
    'readout': readout, 'design': design, 'user-stories': user_stories,
}
# cross references to the old standalone skill names
OLD = {
    'kicksaw-sales-handoff skill': '`/start-motion:handoff`', 'kicksaw-kickoff-deck skill': '`/start-motion:kickoff`',
    'kicksaw-discovery-plan skill': '`/start-motion:discovery-plan`', 'kicksaw-discovery-call skill': '`/start-motion:discovery-call`',
    'kicksaw-solution-readout skill': '`/start-motion:readout`', 'kicksaw-solution-design skill': '`/start-motion:design`',
    'kicksaw-user-stories skill': '`/start-motion:user-stories`',
}
for cmd, fn in BUILD.items():
    t = open(os.path.join(SRC, cmd + '.md'), encoding='utf-8').read().rstrip('\n') + '\n'
    t = fn(t)
    for a, b in OLD.items():
        t = t.replace(a, b)
    if '\u2014' in t:
        sys.exit('em dash in ' + cmd)
    out = os.path.join(OUT, cmd, 'SKILL.md')
    open(out, 'w', encoding='utf-8').write(t)
    print(cmd, len(t), 'bytes', t.count('/start-motion:'), 'command refs')
