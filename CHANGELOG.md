# Changelog

## Not released: /refinement (branch refinement-stage-3, 2026-11-12)

Refinement sessions get their own command, stage 3 (Avi, Nov 12; project doc `claude/refinement-section-2026-11-12.md`). Not tested on a client yet: the plan is a run on the HLS backlog before this merges.

- New `/start-motion:refinement`. Before a session the SC picks the stories by sprint, by epic or one by one, on a clickable story list in the chat (`references/story-picker.html`; a text list where no visual can be shown). Each row shows the story's open question count and whether it carries a design question.
- The skill reads and reviews every picked story itself and adds what is missing (Avi, Nov 12: do not rely on the Open Questions field alone): criteria resting on something unconfirmed, contradictions between stories or with a later comment, cases not covered, unsettled dependencies, choices the client has not seen. It reads the Jira comments: a client answer in a comment becomes a point to confirm, a new point becomes a question. The SC sees where each question came from and can drop any.
- Every open question is worked up with what we know and Kicksaw's proposal, and the SC sees the proposals before anything is built. Where the sources give no basis for a proposal, the slide says so; nothing is invented.
- The refinement deck is built from finished slides (`templates/refinement/`, shown with Tidewell Solar): cover, today's stories, each story with its questions, a detail slide where a question needs a picture (things grouped, a rule over time, who can do what), the acceptance criteria to confirm as they read in Jira, and where we landed. A short story fits on one slide; a long one takes two. `references/refinement-deck.md`.
- With the deck, the SC gets a briefing in the chat, written so someone who was not in discovery could run the call from it: what the session is for, what to do before it, how to open it, each story in turn (what its questions decide, what to listen for, which criteria to slow down on), what to do when an answer is not ready and why, and what happens after.
- Fold-in moved here from `/user-stories`, with three additions: it reads the session's deck, uses notes the SC took on the call as pointers into the recording, and records an agreement with a proposal in the Refined on block.
- `/user-stories` ends when the stories are in Jira. Its prep and fold-in sections are replaced by a pointer to `/refinement`, and its description no longer answers to "prep refinement" or "fold in today's refinement".
- The story reviewer is started by `/refinement` before each session (`scripts/sync-agents.py`).
- From the first run on Fred Hutch (Nov 12): what counts as not yet approved follows the project's own statuses and how the client records approval; the picker shows the date of the client's latest comment and fits long Jira keys; on a large backlog it lists the next three sprints.
- Not in this branch: the Start Motion page's Refinement section, the version number, and the page's copy of the user stories skill text.

## After 0.1.10 (2026-11-12, no version change)

Two small changes merged ahead of 0.1.11 (the whole-scope design, not yet pushed). The version stays 0.1.10 so 0.1.11 keeps its number.

- **The story reviewer is advice to the SC, never a blocker** (Avi, Nov 12). It reports gaps (places where the architect or tester would have to guess), each with the question to ask the client, and wording points in one line per story. Pass or fail and "stops the build" are gone. In `/discovery-call`, a gap the transcript does not settle becomes a question on the Open items tab. In `/user-stories`, a gap no longer keeps an edited story out of Jira; it goes in as an open question. The reviewer also reads the stories before each refinement session and its gaps join the agenda. A status is never refused or held back because of a gap. Not yet run on a client's stories.
- **Decisions: the build plan stage is named the build design stage**, to match the private Start Motion Build plugin. A build design is approved from its review page, never in the decision picker. No change to how `/design` works. The design skill and README still say "build plan" in four places; that rename goes in with 0.1.11.

## 0.1.10 (2026-11-11)

The design is written at the level of shape and decisions (Avi, Nov 11, from the HLS E1 run; project doc `claude/build-agent-test/design-level-handoff-2026-11-11.md`). Run on HLS, 0.1.8 produced a design at build depth: every field, value and validation rule, 25 logged decisions, about 30 reviewer findings. An architect could not write that at the point in a project where the design is written.

- `/design` says what level it is written at. In: objects and how they relate, record types where the process differs, who owns the automation, the access approach, integration patterns, the decisions and the open questions. Out: individual fields, picklist values, validation rules, page and layout names, which permission each set carries. Those are worked out a sprint or an epic at a time, when that slice is built.
- The data model table carries no field lists; a field is named only when it is structural. A new object's spec is its relationships, ownership, record types where they differ and its automation owner. Security gives the approach by layer. Reporting says which reports exist, for whom and on which objects.
- Stories that already exist are read to understand a capability. Their field tables, values and rule wording are not copied into the design.
- A design decision is structural. Component choices are made and logged when the capability is built.
- Design reviewer: reviews at the same level. Coverage is per capability and requirement; a missing field, value, rule, page or permission is never a finding; feasibility is raised only where it would break the shape.
- README: stage numbers match the methodology (1.1 to 2.2).
- Not in this release: the same change on the build plan side (it is where the detail for a slice is designed) lives in the private Start Motion Build plugin.

## 0.1.9 (2026-11-11)

Solution design: two ways to work, the data model first, and decisions made inside the design (Avi, Nov 11). Built from a mockup Avi reviewed the same day (project doc `claude/design-decisions-prototype-2026-11-11.md`). Tested in a browser on the Harborlight example; not yet run end to end on a client.

- Working mode. A new `/design` starts in the chat with one choice: Build together or Run with it, on a clickable picker (`shared/design-mode-picker.html`, the same look as the build stages' picker) with a collapsed explainer and "Use this every time I start a design". A saved default skips the picker. `shared/design-mode.md`.
- The data model comes first. The step that asked the SA to approve a list of sections is gone. In either mode the first thing produced is the data model, one automation owner per object, access in brief, and the few structural decisions most of the design is built on.
- Build together. Everything in the chat: the SA decides the structural decisions first, then each capability comes as a short brief with its decisions in the decision picker, and the SA confirms before the next.
- Run with it. Claude shows the data model it is designing to and keeps going, drafts every section on its own picks and marks each place where the choice was the SA's. The one stop: a structural decision with no defensible pick.
- Decisions inside the design. The design page has a bar that counts what is answered, one marker per decision and Next decision, which goes to each choice in the section it affects. Structural decisions come first and everything else is locked until they are applied. The SA can pick, write their own, ask for more first, confirm or change a recommendation, reopen a call Claude made, and comment on any section. Send to Claude gives one message to paste into the chat; Claude logs the answers, rewrites only the sections they touch and says what changed.
- The design is a content file. `/design` writes `design-content.json` and `scripts/build-design.py` builds the page from it with `templates/Kicksaw Solution Design.template.html`; nobody writes the page's HTML by hand, and an update changes only the sections it touches. The script prints a CHECK for each problem. `references/design-content.md` and a full example, `references/design-content-example.json`.
- Clickable cards in Cowork. The decision picker and the mode picker are shown wherever the session can show an interactive visual, Cowork included; plain text only where none can be shown. Both fall back to text to copy if the chat cannot take the answer directly.
- Drafts are lighter. The client-facing "What it means for [client]" tables are added when the design is made ready to share, not in drafts. A draft's PDF is made when the design goes Final or someone asks; the content file is saved with every version. The design reviewer runs when a draft is complete, not part way through.
- Fixed: the report step listed the design reviewer's findings twice.
- Not in this release: the Start Motion page still shows the 0.1.8 design skill text and kit inventory. The private Start Motion Build plugin keeps its own copies of `decisions.md` and `decision-picker.html`; refresh them with `scripts/sync-agents.py --refresh-from`.

## 0.1.8 (2026-11-11)

Decisions, the whole-solution design and Drive copies (Avi, Nov 10 and 11). The build stages that were developed alongside these (build plan, build and their agents) moved to a separate private plugin, Start Motion Build, so only the people Avi grants access get them (Avi, Nov 11).

- Decisions tab. Every design choice with a real alternative gets a row on a new Decisions tab of the requirements list: the question, the options and their trade-offs, Claude's pick or lean, what was chosen, why, who decided and when. Four kinds: Clear (Claude decides and logs it; the SA can reopen any), Recommended (the SA confirms before the design goes Final), SA call and Client call. A decision never stops a run: only the work that depends on it waits. `shared/decisions.md`.
- Decision picker. In Claude chat, open decisions are put to the SA in one clickable picker (`shared/decision-picker.html`): what is being decided and why it matters, the options side by side with Claude's lean, write-your-own, Confirm or Change on recommendations, Reopen on Claude's calls, and "I need more first".
- `/design` logs every choice as it drafts, writes a Key decisions section, marks Recommended and Open sections with their IDs, and will not go Final with an SA call open. `/discovery-call` and `/user-stories` refinement close a decision row when the client answers it.
- Solution map. `/design` covers every epic in the signed scope and carries a Solution map (every object with the epics that use it, one automation owner per object and moment, shared values, sharing, permission set structure, naming, and the structural questions several epics depend on), so the build can go a slice at a time without boxing in the next.
- Design reviewer, wider. It is handed the workflows, the decided rows and the later epics' requirements, and reports workflow steps the design gives no home, work against a decision, choices nobody logged, and choices that close a door on a later epic.
- Design, readout and review page live in Drive. The master copy of each is an HTML file in the client's Drive folder with a PDF beside it, one running document saved as a new file per version, so none lives only in one person's Claude account. `shared/drive-copies.md`.
- Reading the org. With Start Motion Build installed and a terminal, `/design` starts its org reader; otherwise it uses the org summary or build log in the client's folder and says so.

## 0.1.7 (2026-11-10)

Review agents (Avi, Nov 10). The first phase of the agents: three reviewers, each with one job, a cold read and a fixed answer shape. Tested on Nov 10 against seeded fixtures (project doc `claude/agents-test-report-2026-11-10.md`); all three pass after one wording fix each.

- Source checker and story reviewer. `/discovery-call` runs both on the rows and stories a call added or changed (new step 4b). `/user-stories` runs both on an epic's stories before the SC sees them, and the story reviewer again before a story the SC edited goes to Jira. What the transcript plainly settles is fixed (a quote that differs from the transcript, a wrong timestamp or speaker, a missing trigger the client stated, a quote sitting inside the criteria). A requirement found narrower or broader than what the client said is never reworded on its own; it goes to the SC with the source lines beside it. Fixes may touch rows and stories the SC has edited: only what the finding names changes, each change is listed, and a reviewed story goes back to Draft. Two passes at most.
- Design reviewer. `/design` has the design checked after a draft, after an update and before it is shared (new step 4b): requirements the design does not cover, collisions with what the org already has, anything beyond the confirmed scope, anything heavier than it needs to be, and detail presented as fact that nobody confirmed. The design starts from the most recent written record of the org when the client has one.
- Simple and sound. `/design` has a new section 3b: only what the scope needs, standard before custom, configuration before code, one copy of every fact (a lookup, formula or roll-up before a flat field repeating another record, with the cases where a flat field is right), one automation per object and event, access through permission sets, nothing removed quietly. The design reviewer checks the same list.
- Reports say whether each reviewer ran as a separate agent or as a second pass in the same conversation (Claude chat), and put the clear findings first.
- Every skill that starts a reviewer carries a copy of it at `references/agents/`, written by `scripts/sync-agents.py`.

## 0.1.6 (2026-11-06)

- Requirements list scope (Avi, Nov 6): the Scope column's values are In SOW and Beyond SOW (was Past SOW), in every skill, story footer ("Priority: Beyond SOW") and the discovery call's start card. A new Scope decision column sits right of Scope with Raised with PM, Change order, Future phase and Dropped; empty on a Beyond SOW row means not yet reviewed. The discovery call writes Beyond SOW rows with Scope decision empty and lists the undecided ones on its report for the PM. The SC or PM fills Scope decision; Claude never fills it unless told what was decided.
- Conflict is a new Status value. When a call contradicts an earlier row or a closed decision, the discovery call sets the row to Conflict, keeps the earlier statement, adds the new quote under it and opens the blocking open item as before. When the SC settles it, the row goes back to Heard or Confirmed with the statement updated. Reports list the rows in Conflict.
- Readout: nothing is finalized and no sign-off is recorded while a requirement row is in Conflict; the skill lists them and stops. Before sign-off it lists every Beyond SOW row with its Scope decision for the PM and flags any still empty.
- Columns are found by header name, not letter ("the User stories column", not column Q). The discovery call reads the Requirements header row first; on an older sheet (Tog's, for one) it inserts a missing Scope decision column with its dropdown, renames Past SOW values to Beyond SOW, adds Conflict to the Status dropdown, and says so in the report.

## 0.1.5 (2026-11-04)

- Aligned with Kicksaw's Delivery Methodology (Avi, Nov 4): stages renumbered to sit inside the methodology's Implementation stages, names unchanged. Stage 0 (00 Pre-Sales); 1.1 Kickoff, 1.2 Discovery, 1.3 Readout, 1.4 Scope sign-off (01 Clarify & Align); 2.1 Solution design, 2.2 User stories (02 Design Foundation). Every skill description carries the new number.
- Handoff: the recorded handoff call with sales is held on every project; the command that builds the handoff document stays optional.
- Start Motion page v67: methodology panel on the Overview, handoff call required, SA accountable and SC responsible for user stories, Client Partner at the readout dry run, success criteria and communication plan at kickoff, client readiness before the kickoff deck, architecture diagram and delivery readiness in the design, change and adoption impacts as an optional design section, and five contradictions fixed.

## 0.1.4 (2026-11-02)

- Discovery call (Avi, Nov 2): every run checks tl;dv for client calls since the last one processed. A missed call is shown before anything else (in Claude chat, on the start card with "Process all in order" or "Process today's only"); calls are processed oldest first, and none is skipped silently.
- Start Motion page: "After every client call: /discovery-call [Client]" leads the Stage 2 after-every-call step, and the command card says setup happens once, through /new-client, and that the command asks before setting anything up.

## 0.1.3 (2026-11-02)

- Discovery call (Avi, Nov 2): the call is written straight into the four discovery documents, and the SC reviews it in the documents themselves (editing the requirements list directly, commenting on the workflow document and the What we heard page). "Fold in my comments" applies the comments, replies on each and resolves it, and the next run folds in any left open. Three kinds of change are never written silently: a conflict adds the new quote beside the old one and opens a blocking question instead of replacing anything; Past SOW items are written but tagged and listed for the PM; session adds, moves, splits, merges, cancellations and attendee changes stay suggestions. The SC's own edits in the sheet always stand. In Claude chat the report is a card (`references/start-card.html`): what needs the SC's eyes, then each document with its link and what moved, with buttons to fold in comments, draft the client follow-up email or draft the next session's agenda.
- Start card: items can link (`url`); the found block, the "not here" line and the summary take their own headings (`okTitle`, `naTitle`, `badTitle`, `sum`).

## 0.1.2 (2026-11-02)

- Discovery plan (Avi, Nov 2): in Claude chat the stage opens with a start card (`references/start-card.html`): what was found, with only missing items shown in full, and the intake questions as a short form prefilled from the client settings (kickoff Monday, length in weeks with the end date shown, session days, remote or on site, weeks that run differently, what the SC knows). Once built, the plan is reported as a review card (`references/plan-review.html`): the known, confirm and unknown counts, the coverage check, the risks, every session by week with who is in the room and what it must leave with, Change on any session, answer boxes for the SC-only questions, and buttons to put the sessions on the kickoff deck or draft the inputs request. Session prep uses the start card for its headlines with a Build the session deck button. Elsewhere the stage asks and reports in text as before.

## 0.1.1 (2026-11-02)

- Kickoff (Avi, Nov 2): picking slides in Claude no longer means reading a block of text. The skill looks at the SOW and the client's folder first, then proposes the deck: every core slide plus the optional slides whose reason holds, each with its reason. In Claude chat it shows a visual slide picker (`references/slide-picker.html`): a picture of every slide, tick boxes, A/B layout buttons, full-size pictures on click, and a Build this deck button that sends the picks back. Elsewhere it sends a short text version. Layouts start on A and can change after the build; owners stay out of the question and go in the plan and speaker notes.
- Kickoff: 32 slide pictures added at `skills/kickoff/thumbs/`, served to the picker through jsDelivr.

## 0.1.0 (2026-10-30), first build, not yet released

Skills built from the skill texts embedded in the live Start Motion page (version 1793311819-6881, Oct 30, 2026), one skill per stage command, with these additions on every skill:

- A Start section: the skill reads `references/method.md`, looks before it asks, and reports where the client stands against the stage's readiness list (the "Before you build" checklists on the page become what the command checks on open). A command that finds the client's documents missing offers to set them up right there.
- A one-message intake that works like the page's builder: the slide list (kickoff) and the section list (readout) shown in full with the optional items marked; the person answers once; the skill reads it back in one line, then shows the plan and waits, as the page does. No preset standard set. The readout's two settings (what we heard played back or future state only; dates solid or not) come prefilled from the Discovery documents note and can be changed.
- `references/method.md` per skill: what the stage is for, the checks before you accept, the bar, the calls the skill cannot make, and the link to the stage on the Start Motion page.
- A Next line at the end of every report naming the command that follows.
- The standing lines people used to paste from the page prompts moved into the skill's rules.
- Templates, logos and scripts carried inside each skill: discovery page templates and logos (discovery-plan, discovery-call), the readout template, build script and content example (readout), the kickoff slide templates, manifest, icons, brand files and tokens (kickoff), the Discovery documents note shape (discovery-call).
- The run log row names the plugin version.

- Shared outputs (Avi, Oct 30): the skills keep working out of the SC's Claude Project, and also save three things into the client's Drive folder (the Discovery subfolder, next to the requirements list) as they are written: the Discovery documents note as a Google Doc, every session note, and the readout sign-off record. The discovery call and user stories skills read those Drive copies when the project copy is not there, so anyone on the client can find the outputs.

- New client setup (Avi, Oct 30): `/start-motion:new-client` sets a client up once before the first stage: finds the signed SOW and whatever sales shared, finds or makes the client's Drive folder and its Discovery subfolder, says whether the person is in a Claude Project for the client (strongly recommended, not required) and which connectors are missing, offers the discovery documents setup, and names the first stage. The stage commands point to it when nothing at all exists for a client. The Start here page on Start Motion is the page version of the same steps, with the one-time install.
- Sales handoff (Avi, Oct 30): the kit assumes delivery gets the SOW plus whatever sales shared; no named sales calls folder and no transcript expectation. The discovery plan skill and the Discovery documents note no longer name a Sales Notes folder.
- The reading rule across the kit (Avi, Oct 30): the handoff, kickoff, discovery plan and discovery call skills read the whole client folder, every subfolder included; "01. Sales Handoff" is gone with "Sales Notes"; the readiness reports say what is there beyond the SOW in one clause instead of listing a handoff packet or transcripts as missing (`scripts/edits_0_2_0.py` is the record).
- Handoff is optional (Avi, Oct 30): it runs when sales shares a packet beyond the SOW; a folder holding only the SOW is reported as "nothing to hand off yet" and the skill stops; nothing downstream waits for it. The skill, its method reference and its description say so, and the handoff doc is saved in the Discovery subfolder, never at the top level. new-client hands back the text for the client Project's instructions.
- The em dash check in `build-readout.py` is written as a Python escape so the file carries none.
- Project instructions cut to three lines (Avi, Nov 2): the block new-client hands back now carries only the client, the Drive folder and the plugin line. The Kicksaw team, the client contacts and the document links were never read from the instructions; every stage reads them from the client folder and the Discovery documents note.

Commands: `/start-motion:new-client`, `/start-motion:handoff`, `kickoff`, `discovery-plan`, `discovery-call`, `readout`, `design`, `user-stories`.

Known gaps in this build: the kickoff brand folder has no topographic pattern PNGs (they live in the Kicksaw Slides design system; the skill builds without the pattern when it cannot read them). The kickoff icons were regenerated from Font Awesome Free (the same source the design system used), white on transparent, 256 px.
