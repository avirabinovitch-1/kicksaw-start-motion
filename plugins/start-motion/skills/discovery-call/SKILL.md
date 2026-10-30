---
name: discovery-call
description: Start Motion stage 2 (/start-motion:discovery-call). Processes a Kicksaw discovery call end to end. Pull the tl;dv transcript, write the session note, propose changes to the four discovery documents (the discovery plan, the requirements list, the workflow document and the What we heard page) in a fixed review shape, write what the SC accepts, draft or update the user story and acceptance criteria for every requirement heard, and update the plan for the next session. Use whenever someone says "process today's [client] call", "update discovery", "set up the discovery documents for [client]", or pastes a discovery transcript.
---

# Kicksaw discovery call

One request ("process today's [Client] call") updates the documents that grow during discovery. What to ask, and when, is in "What to ask" below.

The four documents, and where each one lives:

| Document | What it holds | Where |
|---|---|---|
| Discovery plan | Every SOW line and what we know about it, the people, the risks, the sessions with their agendas and must-leave-with lists, the questions, the inputs and the decisions. Built before kickoff by the discovery plan skill; updated here after every call | A Claude page made from the "Kicksaw Discovery Plan" template. Its content is the `dp-data` block at the bottom of the page |
| Requirements list | One row per requirement with its quote, speaker, source call, workflow and steps, status and priority. The user story and acceptance criteria for every requirement, with the open questions each story still has. Also the open items (decisions and questions), the sessions and sources, and the integrations | A Google Sheet made from the "Kicksaw Requirements List: Template" |
| Workflow document | One overview and one screen per workflow, W-01 onward, with numbered steps that the requirements point at | A Claude page made from the "Kicksaw Workflow Document" template. Its diagrams are drawn from the data block at the bottom of the page |
| What we heard | Themes with quotes, pain points and the response, the real numbers, the systems today and what replaces them | A Claude page made from the "Kicksaw What We Heard" template. Same idea: a data block the page draws from |

The solution readout is built from the last three later. Nothing in a readout is written from a transcript directly, so what goes into these documents is what the client will eventually sign. The user stories are drafted here too, from the call the requirement was heard on, so that by sign-off every requirement already has a story ready for Jira. The plan is internal and is never shown to the client; it is how the SC knows what is covered, what is left and what the next session has to do.

## Start: where the client stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere.

1. Read the Discovery documents note in the client's Claude Project (section 0 below). If it is there, read the plan's session list (the `dp-data` block) and the requirements list's Sessions and sources tab, and report in three lines before doing anything else: the last session processed (plan ID, name, date, S-ID); the next session on the plan; what is open (blocking questions, overdue inputs). For example: "Tog. Last processed: D3 Workflow deep dive, Oct 28 (S-05). Next on the plan: D4 Systems and data, Nov 3. Open: two blocking questions, one input overdue."
2. If the note is not there and nothing turns up in the person's artifacts or Drive, say so and offer setup right there: "No discovery documents for [Client] yet. Want me to set them up from the SOW?" Setup is what this skill does when the documents do not exist; it is not a separate request anyone has to know about. If nothing at all turns up for the client (no Drive folder, no SOW), offer `/start-motion:new-client` first: it sets the client up and names the stage to run next.
3. If the plan shows the call in the request already processed, say so. Never process a call twice.

## What to ask: one message

This stage has almost no picks. Ask once, in one message, and only for what the Start did not find:
- Processing a call: which call. Today's call is the default; a date or a pasted transcript overrides it. If tl;dv has more than one call for that client that day, list them and ask which.
- Setup: the client's Drive folder (only if no folder named for the client turns up), and whether to build the discovery plan now or later.

The standing instructions people used to paste from the page (propose every change before writing anything; flag anything past the SOW or at a SOW limit such as rule counts, integration endpoints, source files or licenses, with the quote and timestamp, so the SC can raise it with the PM that week) are rules of this skill below; nobody types them.

Then read back what you heard in one line and run: "Processing Tog, Oct 30, D4 Systems and data, S-06. Proposals first; nothing is written until you accept."

## Setting up a new client (once, before the first discovery session)

When someone says "set up the discovery documents for [Client]" (usually with the SOW, and whatever else is in the client's folder), make the client's copies of the templates. This is the same routine `/start-motion:new-client` runs as the first command on a new client; when this skill finds the documents missing, offer setup here. The SOW is the one input setup needs. Nobody edits a template by hand, and nothing is ever written to a template.

The page templates ship with this skill, in this skill's folder:
- `templates/Kicksaw Workflow Document.template.html` (the page source, with its `wf-data` block)
- `templates/Kicksaw What We Heard.template.html` (the page source, with its `wwh-data` block)
- `brand/primary-full-color.svg` and `brand/primary-inverse.svg` (the Kicksaw logo files all three pages load as `brand/...`)
- `references/discovery-documents-note.md` (the shape of the Discovery documents note written in step 5)

The discovery plan template is in the discovery-plan skill's folder (it is the plan skill that fills it). Use these copies; never take a template from anyone's artifact. The requirements list is the exception: it is a Google Sheet, `Kicksaw Requirements List: Template`, in the shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh), and is always copied in Drive. That folder also holds viewing copies of the page templates for anyone who wants to look at them; the plugin's copies are what Claude builds from.

Steps:
1. **Requirements list.** Copy the sheet with the Google Drive connector (copy the file; never edit the original) into the client's Drive folder, in its Discovery subfolder (or the Engagement docs subfolder when that is the one the client folder has; if there is neither, make a Discovery subfolder and say so in the report), named "[Client] Requirements List". Never at the top level of the client folder. Then, through the Google Sheets connector on the copy only: replace [Client] on every tab's title row; change the Read me tab's line that says this is the template so it says this is [Client]'s list; delete the example rows (the E1 epic and E1.1 and E1.2 on Requirements, the E1.1 and E1.2 stories on User stories, open items 1 to 4, S-01 to S-03, INT-1); add one grey epic row per SOW epic, taken from the SOW, numbered E1 onward from the core of the system outward, each with its two or three lines (if the SOW has scope sections rather than numbered epics, make one epic per scope section, split one only where it holds two separate capabilities, and list them in the report for the SC to confirm); add any sales calls, the handoff call and any pre-kickoff calls (from the client's Drive folder and tl;dv) as the first S-IDs, in date order, with their links; if there are none, the S-IDs start at the first discovery session. Check the Overview tab still counts.
2. **Workflow document.** Copy `templates/Kicksaw Workflow Document.template.html` and the two logo files in `brand/` from this skill's folder into the workspace. In the HTML, find the `<script id="wf-data" type="application/json">` block (the live one: the template also holds a commented-out copy above it, so use the last match in the file, outside any `<!-- -->` comment) and check that its `project.template` is `true` (if it is not, this is not the template; stop). Rewrite the block for the client: `"template": false`, the client's name and engagement, `"updated": "before the first session"`, a session note that says the workflows will appear as sessions are processed, empty `sameOnEvery` and `alsoRaised`, and an empty `workflows` array. Change the `<title>` to "[Client] Workflows". Publish it as a new artifact with the two logo files passed in `files` as `brand/primary-full-color.svg` and `brand/primary-inverse.svg`. Never publish over anyone else's artifact; this is always a new one.
3. **What we heard.** The same with `templates/Kicksaw What We Heard.template.html` and its `wwh-data` block: `"template": false`, the client's name and engagement, `"version": "v0.1, before the first session"`, empty `platforms`, `date`, `lede` and `quoteSource`, `updated` with no items, and empty `themes`, `pains`, `numbers`, `replaced` and `stays` with `constraint` set to null. Title "[Client] What We Heard". Publish it as a new artifact with the same two logo files.
4. **Discovery plan.** Run `/start-motion:discovery-plan` ("plan discovery for [Client]") with the SOW and whatever else is in the folder. It builds the plan page from the template, seeds the Open items and Sessions and sources tabs, and reports the session list for the kickoff deck. If the SC only wants the documents for now, skip this step and say the plan is still to be built.
5. Write the "Discovery documents" note into the client's Claude Project, titled "Discovery documents: [Client]", in the shape of `references/discovery-documents-note.md`: a table of each document with its link and what it was made from (the discovery plan, the requirements list, the workflow document, What we heard, the SOW and anything else shared, the sales and pre-kickoff calls, and the session notes kept in the project as discovery-<n>-<topic>-<date>.md); a Where to look list (the internal Slack channel, the Jira project and the client's email domain, so prep and call processing know where to read); a Client settings list (discovery window and session days, remote or on site, what we heard played back or future state only, who presents the readout and to whom, whether it can carry a dated timeline); and a Client team table (name, role, decides on). It holds the four links, the SOW link and the handoff packet link if there is one, the Slack channel, Jira project and email domain, the client settings and the client team with roles, from the SOW, the Closed Won record, any calls and any client documents. Ask the SC only for what none of these say, in the one message "What to ask" describes. No handoff packet or sales calls is never a reason to stop; build from the SOW and say in the report what came from where.
   Then save the same note as a Google Doc, "Discovery documents: [Client]", in the client's Drive folder, in the same Discovery subfolder as the requirements list, so anyone on the client can find where everything is. The project copy is the one the skills work from; the Drive copy is updated whenever the project copy changes (a new link, a changed setting, a new person).
6. Report the links and remind the SC to share the workflow and What we heard pages with the client lead from the Share menu before the first playback. The plan is not shared with the client.

If a template file cannot be opened, say which one and stop; do not rebuild a template from memory. If the requirements list template in Drive is not visible to the person running this, they need view access to the folder from whoever owns it (Avi Rabinovitch today).

## 0. Find the documents

The client's Claude Project has a short note called "Discovery documents" with the links to the four documents, the SOW and the handoff packet if there is one, where to look (the internal Slack channel, the Jira project and the client's email domain), and the client team with roles. Read it, then open the documents:

- The requirements list through the Google Sheets connector. Read the Requirements, User stories, Open items and Sessions and sources tabs to the end of their data (open ranges, never a fixed row count), one tab per call: asking for several tabs at once hits the Sheets rate limit.
- The discovery plan, the workflow document and the What we heard page through the Artifact tool, by URL. The content is the JSON in the `dp-data`, `wf-data` and `wwh-data` script blocks; read those, not the rendered HTML.
- If a page's data block says `"template": true`, stop: that is the template, not the client's copy. Say so and run the setup above.
- The solution design doc or the client's org, if either is available: the objects, fields and picklist values that already exist, so the acceptance criteria name them correctly.

If the note is missing from the project, look for the Google Doc "Discovery documents: [Client]" in the client's Drive folder (the Discovery subfolder) and use it; it holds the same links. If neither exists, search the SC's artifacts and Drive for "[Client] Discovery Plan", "[Client] Requirements List", "[Client] Workflows" and "[Client] What We Heard" first. If you find documents, ask the SC to confirm them and write the note. Run the setup above only when nothing turns up. If there is no plan, say so and carry on with the other three; the Session plan block below then only reports coverage against the Sessions and sources tab. Never build a readout from memory or from transcripts in place of the documents.

A client sheet made before the User stories tab existed has no such tab. Add it, copying the header row and the two description rows from the template's User stories tab, and point column Q on Requirements at it.

## 1. Get the transcript

- tl;dv: search meetings on that date, pick the one for this client, get the transcript. If a transcript was pasted, use that.
- Read all of it. Note each speaker, their role and whether they are client or Kicksaw. A new client name goes on the team list marked "to confirm", and on the plan's people list.
- Then read email, Slack and Jira since the last call, from the places the note lists, as the Rules below say. If one is not listed or not connected, say so in the report and carry on.
- Match the call to a planned session on the plan (by date and topic). The plan's session ID (D4) and the sheet's S-ID both go on the Sessions and sources row. Every change below cites the S-ID.

## 2. Write the session note

discovery-<n>-<topic>-<YYYY-MM-DD>.md in the client's Claude Project, where <n> counts client discovery sessions only. Who was on, what the session set out to cover (the plan's must-leave-with list and agenda), the process as it runs today in the speaker's order (with their numbers and short quotes), what changed in our understanding, what the client owes us, what is still to schedule. Facts only; mark anything inferred as inferred.

End the note with an internal "Build notes" section for things that are not requirements: data sources and export paths, environment facts, limits, approvals, risks. These never go in the client-facing documents.

Save the session note in the project, and also as a Google Doc with the same name in the client's Drive folder, in the Discovery subfolder next to the requirements list, so the PM and the SA can read it without the SC's project. The two copies say the same thing; the project copy is the one later runs read.

## 3. Propose the changes, then wait

Read the transcript against the documents and reply with one list in this shape, every time. The SC reads it in a few minutes and answers accept, reject or change on each item. Write nothing until they do.

**Requirements**
- New: the next ID in its epic, the statement in plain language, the quote, the speaker, the source, the workflow and steps it belongs to (or, when it is not part of a process, marked as not a workflow step with the reason: reporting, access or data). Priority only if it was said; otherwise leave it blank and say so. Then the story it gets: the user story sentence, and whether it is one story, split into more (and why), or folded into an existing story.
- Changed: which row, what changes, and the quote that changes it. Name the stories it touches.
- Said again: which row gets a second quote (the same requirement heard on a later call is not a new row).
- Conflicts: a statement that disagrees with an earlier row or a closed decision, with both quotes. The SC decides; nothing is overwritten on its own.
- Withdrawn: a requirement the client walked back, with the quote.
- Past the SOW: anything outside the SOW's scope list. It goes in the list marked Past SOW, never silently in scope.

**Workflows**
- Steps added, changed or removed on an existing workflow, by W-ID and step number, and which requirement IDs now point at them.
- A new workflow the call described that has no screen yet. Propose it; do not add it unasked.
- Anything that moved from "not decided yet" to decided, so the dashed box becomes solid.
- Coverage: any requirement with no workflow and no reason, and any step that does something new with no requirement behind it. Each one gets a home, a reason, or a question for the next session.

**What we heard**
- Themes strengthened: an existing theme that gained a quote.
- New themes or pain points, each with the quote and speaker.
- Numbers heard, each with its source. Only figures the client gave or that come from their own exports.
- Systems named, and whether each one is replaced or stays.

**Open items**
- Questions answered on this call, with the answer and the quote, and the stories and criteria the answer changes. Use the plan's Q numbers; they are the same as the Open items numbers.
- New questions, with an owner if one was named, otherwise "SC to assign", and the planned session each one belongs to. Mark the ones that block the design. This includes the gaps a story cannot be written without (an empty state nobody described, a value list nobody gave); those are marked as ours.
- Decisions closed. A decision is logged only when the client says it is decided or picks between stated options. A preference is a requirement with status Heard, not a decision.

**Coverage**
- Against the plan's must-leave-with list for this session: each item done, partly (and what remains), or not reached. Then the agenda items that were not covered and where they go (the flex slot, another session, dropped with a reason).
- SOW lines this session covered (by S-ID on the plan): which moved from unknown or needs confirming to known, with the quote.

**Session plan**
- Sessions to add, split, merge, move or drop, each with the reason (a session whose date or time the client already has is not moved; propose the change for the SC to take to the client), and attendee changes (someone who should have been there, someone who need not come again).
- Client inputs received on or before this call, and the ones now overdue against the session that needs them.
- Decisions closed on this call, and decisions now slipping past their target session.
- The next session's agenda, revised: the blocking questions first, then what this session left partly covered, then its own topics, timed, with who needs to attend.
- Sign-off check: if a blocking question or an SOW decision is behind the session it was planned for and there is no later session to catch it, say that discovery is at risk and name the slot that would recover it. Say this on the day, not at the readout.
- Anything heard that the plan does not have a line for: a new SOW-level topic, a new person, a new risk. Propose the line; do not add it unasked.

Rules for the proposals:
- Only the client's statements become requirements: what they said on a call or wrote in an email. A Kicksaw suggestion goes to open items marked as ours. Internal Slack, the PM bot report and Jira are context only.
- Before proposing anything as new, search the requirements list and the later sessions for the topic. If a row already covers it, propose the quote on that row instead.
- Never invent a requirement, number, name, priority, owner or quote. If it was not said, it is not proposed.

## 4. Write what was accepted

- Requirements list (Google Sheets): add and edit rows in place; never rebuild the sheet, and keep its tabs, formulas and formatting as they are. The count on each epic's grey row ("· 2 requirements") is typed text, not a formula: whenever rows are added to an epic or withdrawn from it, update that count to the epic's rows that are not Withdrawn. A new row gets the status Heard. A second quote goes under the first in the same cell, each with its source. Open items keep their numbers; a closed one gets its answer and the date and stays. Update the Sessions and sources row for this call.
- User stories (the User stories tab of the same sheet): draft the full story for every accepted new requirement and update every story the accepted changes touch, as "Drafting the user stories" below says. Write the story IDs in column Q of each requirement row.
- Workflow document (Artifact tool): read the page by URL, change only the `wf-data` block (nodes, edges, reqs, settle, updated, after), publish to the same URL. Put this call's changes in that workflow's "updated" list so the client sees what moved. Never edit the SVG; the page draws it.
- What we heard (Artifact tool): the same, in the `wwh-data` block: themes, pains, numbers, replaced, stays, constraint, and the page's "updated" list.
- Discovery plan (Artifact tool): the same, in the `dp-data` block, and only what was accepted:
  - the session: `status` to held or partly, a `coverage` sentence, and an entry at the front of its `updates` list (when, what was covered, what moved);
  - questions: `status` answered with `answer` and `src`, or `target` changed when a question moved;
  - SOW lines: `state` to known with the `heard` quote when the client's words settled it;
  - inputs: `status` received or overdue; decisions: `status` closed with `outcome`, or slipping;
  - sessions added, moved (new `when`), or cancelled (status, never deleted); attendees changed;
  - new people on the people list; new risks only when accepted;
  - `project.updated` to this session and a new entry at the front of `project.changes` listing what moved, so the cover shows it first.
  Keep every ID. Add new lines at the end. Publish to the same URL.
- Each document's version or "updated after" line moves to this session.
- Keep each document's tone, structure and look as it is. Add to it; never restyle it.

When the SC says a workflow was played back to the client and confirmed, move its requirements from Heard to Confirmed.

## Drafting the user stories

Every requirement gets its user story and acceptance criteria in the same pass that adds it, written to the standard in `/start-motion:user-stories` (its SKILL.md is the full standard; it ships in the same plugin), so the stories are close to ready for Jira by sign-off. The rules below are the ones that matter at this stage. If the SC points you at stories already pushed to Jira on another project, match their granularity and tone.

**How many stories.** Be thorough: every behavior the client described ends up in some story's acceptance criteria, and every requirement row except a withdrawn one names at least one story in column Q.
- One story per requirement is the default, and takes the requirement's ID (E1.2).
- Split a requirement into more stories when it mixes a system build with data cleanup or migration (always two stories), when it covers two separate capabilities or two different roles, or when one story is doing more than one job (a long list of criteria is the usual sign; it is judgment, not a count). The stories take letters (E1.2a, E1.2b).
- Fold requirements into one story when they are one behavior on the same record at the same step and would be built and tested together. The story takes the first requirement's ID and lists every requirement it covers in the Requirements column.
- No meta or framework stories ("a rule exists for every type"); the rules live in the criteria of the functional stories they belong to.

**The columns,** which map one to one to the Jira fields:
- **Title**: `{Object or area}: {plain-language outcome}`, such as "Lead: assigned to a rep by territory". Match the client project's convention if it has one.
- **User story**: one sentence, "As a/an [operational role], I should have the ability to [capability], so that [outcome]." The role is the client's own name for it, never "user". No technology (no flow, trigger, component). The sentence says in plain words what is built and why; the "so that" is the practical outcome for that person. No criteria detail in it.
- **Description**: the business situation today and what this story does about it, in the client's vocabulary; short explainers only where a criterion would not make sense without one; where the neighboring stories hold the boundaries ("assigning the lead is E1.2"). Then a **Source traceability** block: the client's words verbatim from the tl;dv transcript or the client's own email, never from the session note, the requirement row or an internal message, lightly cleaned of filler and trimmed with "..." but never paraphrased, each cited with speaker, role, S-ID and call name, date, timestamp and the requirement ID it supports: "..." Jordan Lee, Sales Operations Manager, S-02 Discovery 1: lead intake, Sep 15 2026, 00:14:32 (E1.1). Then the footer lines: Source (S-IDs and dates, workflow and steps), Dependencies (story IDs), Priority (the requirement's Priority column: Launch, Future phase or Past SOW, or "not stated yet"). Jira priority and size are set later by the user stories skill.
- **Acceptance criteria**: a plain numbered list, usually five to nine, each one true or false check. Each states the trigger and what the system then does: "When a lead is created with a State/Province in the United States, it is assigned to the rep who owns that state's territory." Keep each one short and simple; split a criterion rather than piling qualifiers into it. Name existing objects, fields and picklist values by their real names, but do not prescribe new components; the architect decides how to build. Checkable from outside by a tester; never an internal system step or a user action. Exact values and error behavior; a worked check with real numbers for any math or dates; the empty, error and cancel cases where the client described them. One behavior per criterion; field-level detail goes in a fields table at the end (Field label, Field type, Values, Notes), with the last criterion pointing at it. Never use should, might, could, may, usually, generally, appropriately, properly, quickly, seamlessly, user-friendly, intuitive, as needed or where applicable.
- **Open questions**: every gap the story still has, one per line: a short name (bolded when it goes to Jira), the question, the Open items number, and "Affects AC #n". Where the client touched the point without settling it, add their quote. Never write a criterion around an unknown and never put "blocked" lines in the criteria; the gap goes here and on the Open items tab, so the two lists always match.
- **Story status**: Draft when written or changed; the SC sets Reviewed by SC. In Jira and the key are set by the user stories skill when it pushes.
- **Updated after**: the S-ID of the last call that changed the story.

**Keeping the stories current.** On every later call:
- A changed requirement changes its stories in the same pass. Later client statements override earlier ones: quote both in Source traceability, say which governs and from which call, and rewrite the affected criteria.
- An answered open question comes off the story's Open questions and goes into its criteria.
- A story the SC already reviewed that changes goes back to Draft, and the report says so.
- A withdrawn requirement sets its stories to Withdrawn; the rows stay. A story covering other live requirements loses only the withdrawn part.
- A Past SOW requirement still gets its story, with "Priority: Past SOW" in the footer, so a change order or future phase has it ready.
- Never fill the architect's fields (build or solution details, metadata, test steps), and never invent a value, field name, quote, date or owner: if it was not said or is not in the org, it is an open question.

## 5. Prep the next session

The Session plan block above already revised the next session's agenda. Write it to the plan (step 4). The day before the session, the SC runs `/start-motion:discovery-plan` ("prep me for [Client] [session]"), which updates that session in the plan, gives the headlines in chat and offers a session deck. Give the SC the three to five workflows to play back at the weekly playback.

## 6. Report back

Three short paragraphs: what this call changed in our understanding, what moved in each document (with counts, including stories drafted and stories changed, questions answered, SOW lines now known), and what the SC should check or decide before the next session and the playback. Then the stories waiting for the SC's review, by ID, with the ones that went back to Draft marked. Then the sign-off check from the Session plan block, if anything is at risk. Then the items not applied and why, and any coverage gaps still open. No recap of steps.

End with one line naming what comes next: the day before the next session, `/start-motion:discovery-plan` preps it ("prep me for [Client] [session]"); when the bar in `references/method.md` is met and the discovery playback is held, `/start-motion:readout`.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:discovery-call (v0.1.0) · discovery · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- No em dashes anywhere.
- Product names, staffing, commercial notes and SOW risk stay in the session note's Build notes and on the discovery plan (internal), never in the three client-facing documents or the stories.
- Section numbers, W-IDs, step numbers, requirement IDs, story IDs, S-IDs, D-IDs and Q-IDs never change once given. Add new ones at the end; never renumber.
- The SC reviews every change before it is played back to the client.
- Email, Slack and Jira: email threads with the client's email domain, the internal Slack channel (threads included, and the PM bot report posted there) and the Jira project, as the Discovery documents note lists them. Read only what is new since the last call. Client emails are the client's own words and are cited like a call, with sender, role, date and subject. Internal messages are context only and never count as something the client told us.
- Session dates and times already shared with the client stay put. Propose any new session or move to the SC first.
