---
name: user-stories
description: Start Motion stage 2.2 (/start-motion:user-stories). Finishes, refines, splits and pushes Kicksaw user stories and acceptance criteria from a signed scope, carrying the client's own words from the call transcripts into every story and every refinement update. Starts from the stories the discovery call skill already drafted on the requirements list's User stories tab, checks them against the signed solution readout and the tl;dv transcripts, proposes the epics, takes the stories to the SC one at a time, creates them in the client's Jira project, and preps and folds in refinement sessions with the client's product owner. Use whenever someone says "write the stories for [client]", "build the backlog", "push the stories", "draft AC", "split this story", "prep refinement" or "fold in today's refinement".
---

# Kicksaw user stories

One request ("write the stories for [Client]") turns the signed scope into a Jira backlog. The scope comes from two documents: the requirements list, which the discovery call skill built from every call, and the solution readout, which is what the client signed. The stories are not written from scratch here: the discovery call skill drafted a story for every requirement on the requirements list's User stories tab, from the call where the requirement was heard, and kept it current as later calls changed it. This skill checks those drafts against what the client signed, finishes them, pushes them to Jira, and runs the refinement loop. The client's words come from the calls themselves: every story carries what the client actually said, pulled from the tl;dv transcript, and every change made in refinement carries what the product owner said on that call. Ask only for what step 0 cannot find.

A story is read by three people at once: the client product owner, who approves it in refinement; the solution architect, who decides how to build it; and the tester, who marks each acceptance criterion true or false. Every choice below serves all three: plain language the client can approve, precise behavior the architect can build from, and checks a tester can run. The client's own words are what let the product owner recognize the story as theirs and let the architect and tester see why a criterion is there.

## Start: where the backlog stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

This skill covers five moves that are five separate prompts on the page: proposing the epics, finishing the stories epic by epic, pushing approved stories to Jira, prepping refinement, and folding a refinement session in. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: written sign-off on a named readout version (recorded, or not); the requirements list (how many approved, how many still heard or confirmed, whether the User stories tab exists and how many drafts it holds); every discovery call on Sessions and sources with its tl;dv link (any missing); the client's Jira project and its key (and what is already in it); the product owner (named in the note or not); the solution design (shared, draft, or none); refinement sessions on the calendar or not; and the epic plan (stories/epic-plan.md exists or not, and which epics are finished, pushed or refined). For example: "Tog. Sign-off recorded Dec 4 on readout v1.2. Requirements: 38 approved, 5 confirmed (stay on the sheet). User stories tab: 41 drafts. Calls: all nine linked. Jira: TOG, empty. Product owner: Dana Ruiz. Design: shared Dec 3. Epic plan: none yet. Next: propose the epics."

If the readout is not signed, or there are no approved requirements, say so and stop (section 0).

## What to ask: one message

Ask once, in one message, and only for what the Start did not find: the epic to finish next when more than one is open and the request did not name it; the product owner when the note does not name them; the Jira project key when none is found; and, when folding in a refinement session, which call, if more than one for the client happened that day. Everything else comes from the documents.

Then read back what you heard in one line and run: "Finishing the Tog stories for the Lead intake epic, six drafts, one at a time for your review."

## 0. Load the signed scope, the drafts and the calls

Read these before anything else:
- the "Discovery documents" note in the client's Claude Project: links to the requirements list, the workflow document, the What we heard page, the readout, and the client team with roles (the product owner for refinement is named here; if not, ask the SC who it is)
- the signed solution readout, at the version that was signed (readout/content.json and readout/sign-off.md in the client's Claude Project; when the sign-off file is not in the project, the Google Doc "Readout sign-off: [Client]" in the client's Drive folder holds the same record): section 5 (Recommended build), section 8 (Future state workflows, with W-IDs and step numbers, and the requirement IDs behind each step when the readout shows them), section 9 (Scope at a glance) and section 13 (Key design decisions)
- the requirements list (Google Sheet), to the end of its data: the Requirements tab (status, and the User stories column naming each requirement's stories), the User stories tab (one row per drafted story, in the shape Jira takes: Title, User story, Description, Acceptance criteria, Open questions, Story status, Jira), the Open items tab and the Sessions and sources tab with every call's tl;dv link. Only stories whose requirements are all Approved go to Jira; stories for Confirmed or Heard requirements are listed for the SC, not pushed
- the session notes for every discovery call, as the index of what was said on which call
- the calls themselves in tl;dv: the transcripts are read when a story needs them (see "The client's words"), not all at once up front
- the solution design doc, if there is one: the data model and the objects and fields that already exist, so stories reference metadata by its real name
- the client's Jira project key, and whether the project already has epics or stories (read the highest key used and the existing epic names before creating anything)

If the readout is not signed, or the requirements list has no approved requirements, say so and stop. If the sheet has no User stories tab (a client set up before it existed), draft the stories here from the approved requirements using the same columns, and add the tab. If a call the requirements list cites is not in tl;dv, say so and keep going; the story then carries the list's quote, marked "from the requirements list, transcript not found".

## The client's words

This applies to every quote in this skill, in drafting and in refinement.

- **Always from the transcript.** When a story needs a quote, find the call from the requirements list or the session notes, open that tl;dv transcript and take the words from there. Never from the requirements list, the session notes or memory, even when they already hold a quote. Those are pointers; the transcript is the source. A drafted story's quotes were taken from the transcript when it was drafted; spot check them, and recheck any you change.
- **Choose the words that set the behavior.** One or two passages per story: the ones that say what the client needs and why, in their words. Not the longest passage, and never a Kicksaw team member's words presented as the client's. If the client only agreed to something Kicksaw proposed, say so plainly ("agreed when Ben proposed...") and quote the agreement. Include the quote that closed a decision, and when a later call changed the requirement, quote both and say which governs.
- **Lightly cleaned.** Take out filler words (um, like, you know, repeated words, false starts). Mark a cut with an ellipsis and a clarification in square brackets. Never change a word that carries meaning, never reorder, never complete a sentence the speaker did not finish. If the cleaned version would read differently from what the person meant, use more of the passage instead of cleaning it.
- **Cited so anyone can find it.** Every quote reads: "..." Speaker name, role, S-ID and call name, date, timestamp (requirement ID). The call name is the one on the Sessions and sources tab; the timestamp is where the passage starts in the recording. Example: "Right now I have to open every single lead to see if anyone called them" Dana Ruiz, Sales Operations Manager, S-04 Discovery 3: Lead routing, Oct 7 2026, 00:41:20 (E1.3). A requirement that came from a document cites the document by name and revision.
- **Never invent, never paraphrase as a quote.** Anything in quotation marks is in the transcript. Something the client meant but did not say is written in plain prose with no quotation marks, and goes on the open questions list if the story depends on it.

## 1. Propose the epics

Before finishing any story, produce a one-page epic plan and wait for the SC to confirm.

- Start from the readout's workflows (section 8): each W-ID is a candidate epic, named for the workflow in the client's words ("Lead intake", "Renewals", "Order to cash").
- Fold in the capability groups from section 5 that are not a workflow (a core record and its data points, reporting and dashboards, security and access, integrations). Each becomes its own epic.
- Data migration is always its own epic, even when it is one story. Cleanup and migration work never shares a story with build work.
- Merge two workflows into one epic when they share a record and a team; split one workflow into two epics when it carries more than about twelve stories.
- For each epic: name, the W-IDs and section 5 rows it covers, the approved requirement IDs under it, the drafted story IDs under it, the calls those requirements came from, and the rough story count.
- Say where the drafts do not line up with the signed scope: an approved requirement with no story, a story whose requirement is not approved, a story the readout changed.

Save the confirmed plan as stories/epic-plan.md. Epic names and the mapping are stable from here; a story's source line depends on them.

## 2. Finish the stories, one at a time

Work through the epic plan story by story, starting from each story's row on the User stories tab. For each one:
- Check it against the signed readout and the Open items tab: what the readout decided that the draft does not reflect yet, decisions closed since the draft, open questions now answered. Fold those in; later statements override earlier ones.
- Check it against the standard below, line by line, and fix what falls short. Check the split: a story that mixes build with data work, or is doing more than one job (a long list of criteria is the usual sign), is split now (letters on the ID); two stories that are really one behavior are merged.
- Add the readout to the Source footer line.
- Write the finished story back to its row on the User stories tab, so the sheet and what goes to Jira match.

A story keeps the status Draft while you work on it. Then show the stories to the SC one at a time for review, edit and approval; when the SC approves one, set it to Reviewed by SC on the sheet. Create nothing in Jira until the SC says the story is ready. A Withdrawn story is never pushed; list it for the SC with the quote that withdrew it. Before showing the SC anything for an epic, run the two reviewers on that epic's stories ("The two reviewers" below) and act on what they find.

### The two reviewers

Two reviewers read every story before the SC does. Each has one job and reads the story without having seen it written.

- **The source checker** opens every quote's call at its timestamp and checks that the quote is there, that the speaker is right, and that the acceptance criteria say what the client said: not more, not less. Hand it the epic's stories (ID, acceptance criteria, each quote with its citation), the tl;dv link for every S-ID the stories cite, the signed readout, and the calls held after each story was drafted.
- **The story reviewer** reads each story as the architect and the tester will, with only the story in hand, and reports the criteria that cannot be built or tested as written. Hand it the stories only, plus the list of objects and fields that already exist when the solution design or an org summary has one. Never hand it the requirements list or the transcripts.

**Starting a reviewer.** Where the session can start a separate agent (Claude Code, Cowork, Codex), start it by name (`start-motion:source-checker`, `start-motion:story-reviewer`) and hand it only what its file says it is handed: never this conversation, your notes or your reasoning. Where the session cannot start one (Claude chat often cannot), read its instructions at `references/reviewers/<name>.md` in this skill's folder and run them yourself as a second pass, working from the sources and the story text, not from memory of drafting. Say on the report which way each reviewer ran; a second pass in the same conversation is weaker than a separate reader, and the SC should know which one they got.

What to do with the findings:
- Fix what is plainly wrong and what the sources settle: a quote that differs from the transcript is replaced with the transcript's words; a wrong timestamp or speaker is corrected; a criterion with no trigger gets the trigger the client stated; a quote inside the criteria moves to the Description; Given/When/Then is rewritten as plain behavior.
- Never settle a finding by guessing. A criterion that is not exact because the client never gave the value becomes an open question on the story and on the Open items tab.
- A story the source checker found narrower or broader than what the client said, or contradicted by a later call, is not reworded on your own. Show the SC the row and the source lines side by side; they fix the wording, ask the client, or mark the point as Kicksaw's recommendation so nobody reads it as something the client asked for.
- A finding that a story should be split or merged is the SC's call; list it.
- Run each reviewer once, fix, and run it once more on the stories that changed. Two passes at most. Whatever is still flagged goes to the SC as it is.
- When you show the SC a story, show its open findings under it, each in one line. A story with none says "Both reviewers passed".

### The title

`{Object or area}: {plain-language outcome}`. "Lead: assigned to a rep by territory". "Conversion: one step from lead to opportunity". Match whatever convention the target project already uses if it has one.

### The User Story field

One sentence: **"As a/an [operational role], I should have the ability to [capability], so that [business outcome]."**

- The role is a specific operational role the client uses: "intake coordinator", "sales rep", "operations manager", "finance staff member". Never "user", never a generic persona. Use the role name the client uses on the calls.
- The capability describes functionality, never technology. No "flow", "trigger", "LWC", "validation rule" in the sentence.
- Plain English test: the sentence says in ordinary words what is being built and why. If it needs a paragraph to explain, it is wrong. The "so that" is the practical outcome for the person in the role, in the client's terms. No criteria detail in the sentence (how fields get set, values, rules); role, capability, outcome only.

### The Description field

Narrative context in plain prose. The test for every line: it helps the product owner approve, the architect build, or the tester test. If it does none of those, it is clutter and comes out. Keep as much useful context as that test allows.

In order:
1. The business situation and what this story does about it. Two to five sentences, written in the client's vocabulary: their names for the records, the teams and the steps, as heard on the calls, not Salesforce names. Say which neighboring stories hold the boundaries ("assigning the lead is E1.2").
2. Short bolded explainer subsections where a concept needs unpacking ("**How territories are set:** ...", "**Why the match runs first:** ..."). Only when the AC would not make sense without them.
3. **Source traceability:** the quotes that drive the story, pulled and cited as "The client's words" says. Each on its own line.
4. **Refined on [date]:** one block per refinement session that changed the story, added by step 5. Nothing here before refinement.
5. Footer lines, each on its own line:
   - `Source: Solution readout v{n} (signed {date}), section 8 W-01 Lead intake, steps 2 to 4; section 5 "Lead capture" row. Calls: S-04 Discovery 3: Lead routing (Oct 7 2026), S-06 Discovery 5: Conversion (Oct 14 2026)`. The readout is the shared source the client signed; the calls are where the words came from.
   - `Supersedes: {key}` when this story replaces an earlier one, with one line on what changed.
   - `Dependencies: {key} ({short name}), {key} ({short name})`.
   - `Priority/size: Launch · M · 5 points`: the readout's go-live priority, then the T-shirt size and points once the SC gives them (the SC and SA usually size after refinement; until then write "Launch · size after refinement"). The Jira Priority field stays Medium unless the SC says otherwise.
   - A backlog note when one applies: "BACKLOG per {name} {date}: the model works without it; build when scheduled."

### The Acceptance Criteria field

A plain numbered list, usually five to nine items, each a single true or false check written as declarative, present-tense system behavior. No Given/When/Then. No "AC-" prefixes. No quotes inside the AC; the words behind a criterion live in the Description.

Keep each criterion simple and short. It states the trigger and what the system then does: "When a lead is created with a State/Province in the United States, it is assigned to the rep who owns that state's territory." A flat "X has Y" statement is not enough; say what triggers it and what happens. Do not pile qualifiers, parentheticals and cross-references into one criterion; split it or cut it.

What makes a criterion good:
- **An explicit trigger that names existing metadata**: "When a lead's State/Province changes, ...". Name existing objects, fields and picklist values by their real names. Do not prescribe new components; the architect reads the AC and decides how to build.
- **Testable from outside.** A tester can mark it true or false by looking at what a person sees or what the record holds. Never a system-internal step, and never a user action ("the rep sets..."); state what the system offers or does.
- **Exact values and error behavior**: "A lead cannot be closed without a Closed Reason; a save without one is blocked with a clear error."
- **A worked check with real numbers** for anything with math or dates: "(worked check: created 2026-01-10, close date 2026-03-11, which is 60 days later)". Take the numbers from what the client said on the call when they gave any.
- **Edge and failure states**: the empty state ("a territory with no rep sends the lead to the sales manager's queue"), divide by zero ("shows blank, not an error, when the denominator is zero"), the cancel path ("cancelling leaves the record exactly as it was"), exclusions ("newsletter sign-ups never create a lead").
- **Anything referenced is defined**: list the values rather than "all the values".
- **One behavior per criterion.** Field-level detail goes in a fields table at the end, after a lead-in line ("Every lead has the following fields, as described in the table below."): Field label, Field type, Values, Notes. The criterion that points at the table ("Every lead has the fields described in the table below") is the last one, right above it. Long value lists get their own Values table. A field that must be answered is a Yes/No picklist, never a checkbox.
- **Banned words in the acceptance criteria**, because they cannot be tested: should, might, could, may, usually, generally, appropriately, properly, quickly, seamlessly, user-friendly, intuitive, as needed, where applicable. The story sentence's "I should have the ability to" is the standard form and is fine.
- **Boundaries by story ID**, never a "not built here" table: "the review steps are E9.3".

### The Open Questions field

What discovery did not settle and the product owner has to answer. One per line: a bold short name (plain on the sheet, bolded in Jira), the question, the Open items number, and "Affects AC #n". Where the client touched the point on a call without settling it, add the quote so the product owner sees where the question came from. Never write a criterion around an unknown and never put a "blocked" line in the AC. Every story goes into Jira as New, open questions and all; refinement closes them.

### Fields the story author leaves empty

Build/Solution Details, Metadata, Test Steps and build or QA sub-tasks belong to the solution architect and are added after refinement. Never fill them.

### Hard rules

- Only stories whose requirements are all approved go to Jira. Stories for confirmed or heard requirements stay on the sheet, on the SC's list.
- No meta or framework stories ("a validation rule exists for every type"). Rules live in the AC of the functional story they belong to.
- Build and data work are separate stories, and data work lives in the migration epic.
- Anything the client said on a call is a requirement unless they said it is out or it is beyond the SOW. Never drop one silently; place it in another story by ID or keep it.
- No stories for things Salesforce may not deliver; that is a nice-to-have or an open question for the architect.
- Derive before you add: prefer roll-up and formula behavior over new keyed fields.
- Never invent a value, a field name, a quote, a date or an owner. If it was not said or is not in the org, it is an open question.
- No em dashes anywhere.

## 3. Create the stories in Jira

When the SC approves a story, create it in the client's Jira project under its epic (create the epic first if it is not there): Summary from the Title, and User Story, Description, Acceptance Criteria and Open Questions in their own fields, Priority Medium unless the SC says otherwise, T-Shirt Size when the SC has sized it, unassigned, the story ID as its label. Status New, with or without open questions. Link dependencies with "blocks". A story the SC edited after the reviewers ran goes through the story reviewer once more before it is created; a finding goes back to the SC, not into Jira. Read the issue back to confirm the custom fields landed. Then confirm the key to the SC, add it to stories/epic-plan.md, and on the requirements list set the story's row on the User stories tab to In Jira with its key, and write the key in the Jira column of every requirement the story covers.

From here Jira is the story's home: refinement changes go to Jira, and the sheet row keeps the key and status.

The first pass is the whole signed scope in Jira, gaps and all. Discovery never covers every detail; refinement is where the details get closed.

## 4. Prep refinement

Refinement is a live call with the client's product owner. Before each session:
- Propose which stories to refine, by epic and in build order, enough for one session (usually six to ten).
- For each one, list its open questions and what else the SC should ask: "Does this look right? What did we miss? What would make this wrong?"
- Draft the agenda: stories in order, each with its questions, and the decisions the session has to close.

## 5. Fold in refinement

When asked ("fold in today's [Client] refinement"), pull the tl;dv transcript for that session (if more than one call for the client happened that day, ask which) and add it to the Sessions and sources tab with the next S-ID. Read all of it and note each speaker. Then, story by story:

- **Match what was said to the stories on the agenda,** and to any story the product owner brought up that was not on it.
- **For each story discussed, pull the product owner's words** for every answer, correction and addition, cited as "The client's words" says. Take the passage where they say what they want and why, not where they say "yes".
- **Add a Refined on block to the Description**, one per session, between Source traceability and the footer:

  **Refined on Oct 28 2026 with Dana Ruiz (Refinement 2):**
  - "We never want a lead from a partner to go to a rep... [it goes] to the partner manager" Dana Ruiz, Sales Operations Manager, S-15 Refinement 2, Oct 28 2026, 00:12:05. Changed AC 1: leads with Lead Source = Partner go to the partner manager's queue. Closed open item 2.
  - "Blank is fine, an error would stop my team cold" Dana Ruiz, Sales Operations Manager, S-15 Refinement 2, Oct 28 2026, 00:14:40. Added AC 7: the field shows blank, not an error, when there is no territory.

  Each bullet is one quote and, in plain words, what it changed: the criterion number added, changed or removed, the open question it closed, or the field it added. If a criterion changes, keep the new wording in the AC field only; the block records why it changed.
- **Update the AC and the Open Questions fields** to match: rewrite the criteria that changed, add the new ones, remove the questions answered. A question the product owner raised and could not answer goes in as a new open question with their quote, and on the Open items tab.
- **Anything the product owner asked for that is beyond the signed scope** goes in the requirements list with Scope set to Beyond SOW and Scope decision empty, with the quote and citation; it never widens a story silently. Tell the PM that week.
- **A story the product owner approved** moves to Pending Client Approval or Refined, per the project's workflow. Say which stories moved.
- **Record new decisions in the Open items tab** with the quote, and update the Source footer line of the story to add the refinement call.
- Keep the story's tone and structure; add to it, never rewrite the parts the SC already approved unless the product owner changed them.

Stories then flow: New, Pending Client Approval, Refined, Build Ready, In Progress, Ready for QA, QA Testing, UAT, Done. The SC and SA size refined stories together; the PM, SC and SA load sprint 1 from them with input from the team.

## 6. Report back

Three short paragraphs: what was finished or changed and under which epics, what the SC needs to check or decide, and what is still open with the client. Then a short list of every story waiting for review, each with the reviewers' findings still open on it, and one line on how the reviewers ran (as separate agents, or as a second pass in this conversation). After a refinement, also list every story that changed with the criteria touched, and any quote that could not be found in the transcript. No recap of steps.

End with one line naming what comes next, by move: after the epic plan, `/start-motion:user-stories` finishes the stories epic by epic; after the SC approves a story, `/start-motion:user-stories` creates it in Jira; before each refinement session, `/start-motion:user-stories` preps it; the same day after it, `/start-motion:user-stories` folds the answers in; once sprint 1 is refined, the SA adds build details and sizes the stories with the SC, and the PM loads the sprint.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:user-stories (v0.1.6) · stories · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Reference

Read references/example-stories.md before drafting, when it exists. It holds full stories from Kicksaw projects to pattern-match against: match the closest example's granularity and tone, then adapt to the new client's domain. Never copy its content.
