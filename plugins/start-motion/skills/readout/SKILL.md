---
name: readout
description: Start Motion stage 3 (/start-motion:readout). Builds, updates and presents a Kicksaw solution readout from the three discovery documents (the requirements list, the workflow document and the What we heard page). Proposes the cut, fills the readout template's content file, builds the page with the readout build script, cuts the readout deck from it, folds client review feedback back in, and finalizes and records written sign-off. Use whenever someone says "build the readout for [client]", "update the readout", "cut the deck", "fold in the readout feedback", "get the readout ready for sign-off" or pastes a section list from the Start Motion page.
---

# Kicksaw solution readout

One request ("build the solution readout for [Client]") produces the readout from the three discovery documents. The readout is never written from raw transcripts: the discovery call skill has already turned every call into the requirements list, the workflows and the What we heard page. This skill assembles, decides and renders. Ask only for what step 0 cannot find.

The readout is a page built from a template, the same way the workflow document and What we heard are. You write one content file (readout/content.json in the client's Claude Project); the build script merges it with the client's What we heard data and workflow data and produces the page. Nobody edits the page by hand. A wrong line is fixed in its source (the requirements list, the workflow document, What we heard, or content.json), and the page is rebuilt.

Reference examples: the Fred Hutch CIS Solution Readout (https://claude.ai/artifact/1zGR6YS43gd5uF9fuaaQHH) and its deck (https://claude.ai/artifact/HBeWJkdv6Q2UFQPE7agzvL); the Crossroads readout deck (https://claude.ai/artifact/3EBpjRHritAxrDaDD75qqo) for a future-state-only readout with a dated timeline. Match their depth and tone, not their content. The template preview shows the finished shape: https://claude.ai/artifact/Dyb1mx8s7mQh9M6hcghCzo.

## Start: where the readout stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

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

## Where the template lives

This skill's folder carries everything the build needs:
- `templates/Kicksaw Solution Readout.template.html`: the page shell (styles, renderer, an empty `ro-data` block)
- `scripts/build-readout.py`: merges the content file, the workflow data and the What we heard data into the page, runs the checks, and writes the client's page
- `references/content-example.json`: a filled example of the content file
- `brand/primary-full-color.svg` and `brand/primary-inverse.svg`: the logo files every page loads as `brand/...`

Use these copies, never anyone's artifact. The shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh) holds viewing copies of the same files. If a file cannot be opened, say which and stop; do not rebuild the template from memory.

## 0. Load the three discovery documents

Find them through the "Discovery documents" note in the client's Claude Project, which links them with the SOW and the handoff packet if there is one:

- The requirements list (a Google Sheet, through the Sheets connector; read the Requirements, Open items, Sessions and sources and Integrations tabs to the end of their data, one tab per call). Only requirements with status Confirmed or Approved go into the readout as the build. Heard items are shown as provisional, and said so.
- The workflow document (a Claude page, through the Artifact tool by URL). Save its page source to the workspace; the build script reads its `wf-data` block.
- The What we heard page (a Claude page, the same way). Save its page source; the build script reads its `wwh-data` block.
- The SOW, and the handoff packet if there is one, because section 11 lines the readout up with the SOW.
- The note's client settings: whether the client wants what we heard played back or future state only, who presents, who the client audience is, whether a dated timeline is possible.
- readout/content.json and readout/manifest.md, if a readout already exists. Then this is an update: change only what was asked and what the documents changed.

If any of the three documents is missing, or a page's data block still says `"template": true`, say which and stop. Do not build a readout from memory or from transcripts.

Where each readout section comes from:

| Readout section | Built from | Who writes it |
|---|---|---|
| 01 Executive summary | The numbers and systems from What we heard, the SOW | Drafted by Claude, edited by the SC |
| 02 What we heard, 03 Pain points, 04 Current state | The What we heard page, as it is | The build script copies it |
| 05 Recommended build | Confirmed requirements grouped by epic | Drafted by Claude; group headers are the SC's |
| 06 How it comes together | Epic order and the Integrations tab | Drafted by Claude, edited by the SC |
| 07 Target operating model | The systems from What we heard and the Integrations tab | Drafted by Claude |
| 08 Future state workflows | The workflow document | The build script copies the workflows; Claude writes the today and changes lines |
| 09 Scope at a glance, 10 Future phase | Requirements by Scope and Priority, rows marked Past SOW | Drafted by Claude |
| 11 Aligning with the SOW | The SOW against the rows marked Past SOW | Drafted by Claude; the scope principle is the SC's |
| 12 Success measures | The pain points | Drafted by Claude, edited by the SC |
| 13 Design decisions, 14 Inputs needed | The Open items tab | Drafted by Claude |
| 15 Next steps | The sessions coverage and the SOW timeline | Drafted by Claude |
| B The requirements list | The list's link | The build script |

## 1. Start from whatever was given

- **Only a client name.** Propose the cut (step 2) from the documents and the client settings.
- **A picked section list,** usually the prompt from the section picker on the Start Motion page: sections by their fixed numbers, whether What we heard is in or left out on purpose, how the dates read (not decided, solid, or a dependency sets the pace), the workflows to draw, and notes. Treat it as the SC's cut. Build exactly those sections; if a pick looks wrong for this client (a dated timeline with no dates in the SOW, What we heard left out for a client who asked for a playback), say so in the manifest and let the SC decide.
- **An existing readout to change.** Read readout/content.json and change only what was asked. Never rebuild the content from scratch.

## 2. Propose the cut, then wait

Before writing the content file, reply with a one-page manifest and wait for the SC to confirm:
- Every spine section with in or out and the reason. The only spine sections that are ever left out are 02 to 04 (What we heard, Pain points, Current state), and only when the client settings say future state only.
- Every optional section with in or out: 04 current state, 07 target operating model (roles or teams change), example journeys inside 08 (one journey carries the solution), 10 future phase (scope was split), a dated timeline in 15 (only when the SC says the dates are solid), A workflows today.
- The workflows to draw, by W-ID, in order, and any in the workflow document that are left out, with why.
- The judgment items only the SC writes, drafted for them to edit: the three pillars, the build table's group headers, the sequencing layers, the scope principle, the success measures.
- The three things the client is being asked to approve.
- The sign-off definition (who signs, in writing, naming this version) and the date it is asked for.
- What is still a placeholder, and who can fill it.

Save the confirmed manifest as readout/manifest.md in the client's Claude Project.

## 3. The spine

Six groups, numbered sections. Section numbers, W-IDs and step numbers are fixed: a section left out keeps its number and the others do not move, and nothing is renumbered after sign-off, because the user stories cite them.

Overview
1. Executive summary. Two or three short paragraphs: who the client is, what is breaking today and why, what this project builds. Three pillars, one line each. "What we are asking you to approve": the three approvals, the sign-off definition and the date. Figure 1, the system at a glance (what comes in, the core system, what goes out).

What we heard (in by default; out as a group only for future-state-only clients)
2. What we heard. Lede with one client quote. Theme, What we heard (with the quote and speaker), Solution implication.
3. Pain points and the response. Pain point, Today, At go-live. A callout for any hard constraint.
4. Current state (optional). The real numbers, what gets replaced, what stays.

What we will build
5. Recommended build. Capability, Launch build, What it solves, grouped under headers. Every row answers a theme or pain point.
6. How it comes together. Four layers at most, in build order. Sequencing, not a timeline.
7. Target operating model (optional). Role or team, Today, At go-live.
8. Future state workflows. The overview map, then each workflow: W-ID and name, lede, swimlane, How it runs today and What changes, the requirements behind it with their step numbers, decisions to close. Example journeys (optional) after the workflows.

Scope
9. Scope at a glance. In this project, set aside.
10. Future phase roadmap items (optional). Item, What it would add, Size, with a line that none of them touch the committed go-live without the client's approval.

The road ahead
11. Aligning with the SOW. One paragraph, one bold-led line per deviation, the scope principle.
12. Success measures. About the client's day-to-day work, not system metrics.
13. Key design decisions to close. Open ones first, each with who decides it.
14. Inputs needed from the client. Each with a named owner.
15. Next steps. A strip (readout, review, sign-off, build, go-live) and three numbered steps. Dated only when the manifest says the dates are solid; otherwise name the dependency that sets the pace.

Reference
A. Appendix: workflows today (optional).
B. Link to the requirements list. The list is an input and a reference, not part of the readout.

## 4. Write the content file and build the page

1. Copy `references/content-example.json` from this skill's folder as the starting shape the first time; afterwards edit readout/content.json in place. Fill it from the confirmed manifest and the documents. Field by field:
   - `project`: `template` false, `client`, `clientDetail`, `engagement`, `platforms`, `title` (the project's name), `description`, `preparedBy`, `presentedBy`, `date`, `version` (v1.0 for the first draft), `status` ("draft" until step 7 says "final"), `signed` (null until the sign-off is recorded), `requirementsList` and `workflowDocument` (label and link), `updated` (the version and the list of what changed after the readout; empty on the first draft).
   - `include`: which optional sections are in, by number (`"02"`, `"04"`, `"07"`, `"10"`, `"A"`) and `"journeys"`. Always-in sections need no entry.
   - `s01`: `paragraphs`, `pillars` (t, d), `approve` (items: exactly three; `definition`; `by`), `figure` (caption, `core` t and s, `left` and `right` boxes with t, s and the arrow label e).
   - `s02`: a `lede` only if the SC wants a different one from the What we heard page. Sections 02 to 04 are otherwise filled by the build script.
   - `s05` groups and rows (cap, build, solves); `s06` layers (t, d); `s07` rows (role, today, future); `s08` (`lede`, `draw`: the W-IDs in order, `notes` per W-ID with `today` and `changes`, `journeys` with steps of role and t, and an outcome); `s09` (inScope, setAside); `s10` groups and rows (item, adds, size) and `note`; `s11` (intro, deviations t and d, principle); `s12` rows (measure, how); `s13` rows (area, status "open" or "closed", decision, why, who); `s14` items (text, owner); `s15` strip (when, t, d, `golive` on the last) and steps (t, d); `sB` note.
   - `internal`: notes for the team by section (`"s05"`) or by W-ID (`"W-01"`). They sit behind the Internal notes switch, off by default. Nothing confidential about the client relationship goes anywhere in the file, including here.
   - Any row that changed after the readout gets `"upd": "v1.1"` so the page marks it.
2. Copy `templates/Kicksaw Solution Readout.template.html` and `scripts/build-readout.py` from this skill's folder into the workspace, next to the saved page sources of the workflow document and What we heard.
3. Run: `python3 -I build-readout.py --template "Kicksaw Solution Readout.template.html" --content content.json --workflows "<Client> Workflows.html" --heard "<Client> What We Heard.html" --out "<Client> Solution Readout.html"`. It copies sections 02 to 04 from What we heard as they are, copies the workflows to draw from the workflow document's data (so every diagram is identical in both), and prints a CHECK line for each problem (a W-ID that does not exist, approvals that are not three, an open decision with no one to decide it, an input with no owner, em dashes, a final version the sign-off line does not name) and a NOTE listing every placeholder still to fill. Fix every CHECK in its source and run it again.
4. Publish the page. First build: a new artifact, with the two logo files from this skill's `brand/` folder passed in `files` as `brand/primary-full-color.svg` and `brand/primary-inverse.svg`. Every rebuild after that: publish to the same URL, and add its link to the Discovery documents note. Never publish over anyone else's artifact.
5. Save content.json back to readout/content.json in the client's Claude Project.

Writing rules for everything in the content file: plain client language, sentence case, tables over paragraphs, the client's own names for their records and teams, real numbers only from What we heard or the client's own exports, and no em dashes.

## 4b. Process the dry run

When asked ("process today's [Client] readout dry run"): pull the dry run recording from tl;dv (if more than one call for the client happened that day, ask which). Propose the cuts and corrections it decided, to the section plan (what the deck keeps, what moves to the appendix, the sign-off date) and to the content file, and wait for the SC's OK. Then apply them to readout/manifest.md and readout/content.json, bump the version (v1.1), list the changes in `project.updated`, rebuild the page, and report what changed. The deck is cut only after this, so it carries exactly what the dry run kept.

## 5. Cut the deck

The deck is cut from the readout, never built separately. It orients the client so they can digest the readout afterwards; nobody reads a document aloud.
- Slides, in order: cover; executive summary with the three pillars and the volumes; what we heard (if included) as Theme, Today, At go-live; success measures, moved to the front; the system at a glance (Figure 1); the workflow overview; what we will build; scope boundaries; what we are asking you to approve; design choices closed; open decisions; build sequence; path to go-live or the timeline; next steps and what we need from the client; appendix link to the readout and the requirements list.
- Every slide carries a header saying what it is. Detailed workflows go to the appendix when they were played back in discovery already.
- Speaker notes on every slide: which readout section it mirrors and the one or two things to say that are not on the slide.
- Build it as a Slides artifact on the Kicksaw brand, from the same content file, so the figures and wording match the readout. The deck is not what the client signs.

## 6. Run the review window

After the presentation:
- Capture every client question and comment from the readout call transcript into the Open items tab with an owner (the SA takes the technical ones).
- Draft the answers the SC and SA agree on; the two working sessions with the client lead are where they are settled. Fold them into the three documents and into content.json. Bump the version (v1.1), mark each changed row with `upd`, list the changes in `project.updated`, and rebuild.
- Anything the client asked for that is past the SOW goes in the requirements list marked Past SOW, as a future phase or a change order; it never widens scope silently.

## 7. Finalize for sign-off and record it

When the SC says the review answers are in:
- Fold them in, bump the version, set `status` to "final", make the sign-off definition name that version and the signer, rebuild, and stop changing it. This version is the one the sign-off request names.
- Draft the sign-off request email for the PM to send to the named sponsor (the EM/DM copied): the readout link, the version, the three approvals, and the ask for a written reply.

When the written approval arrives:
- Set `project.signed` to the date, the signer and the version, and rebuild, so the cover shows it.
- Move the approved requirements to Approved in the requirements list, file the approval (or a link to it) in the client's Claude Project as readout/sign-off.md and as a Google Doc "Readout sign-off: [Client]" in the client's Drive folder (the Discovery subfolder, next to the requirements list), so the PM has it without the SC's project, and say so in the report. Only then does `/start-motion:user-stories` read the list.
- A verbal yes, a chat message, or silence past the date is not a sign-off. Say so if asked to record one.

## 8. Report back

Three short paragraphs: what the cut includes and why, what the SC should check before the dry run (figures, numbers, the three approvals, the sign-off date), and what is still open. Then every CHECK the build printed that is not fixed, and every placeholder still to fill. No recap of steps.

End with one line naming what comes next, by move:
- after the build: the SA reviews the build, then the dry run (15 to 20 minutes, recorded); after it, `/start-motion:readout` again to process the recording
- after the dry run is processed: `/start-motion:readout` to cut the deck
- after the deck: present; the same day, `/start-motion:readout` to process the readout call
- after the readout call: the two working sessions, then `/start-motion:readout` to finalize for sign-off
- after the sign-off is recorded: `/start-motion:design` finalizes the design against the signed scope, and `/start-motion:user-stories` reads the list only after this

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:readout (v0.1.3) · readout · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- Never invent a figure, name, date or quote. Where something is missing, use a bracketed placeholder and add it to the Open items tab.
- The SC reviews the manifest before the build and the readout before the dry run.
- Edit the source, never the page. Keep each document's tone, structure and look when updating; add to it, never restyle it.
- Section numbers, W-IDs and step numbers never change once given.
