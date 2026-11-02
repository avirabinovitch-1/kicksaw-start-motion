# Changelog

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
