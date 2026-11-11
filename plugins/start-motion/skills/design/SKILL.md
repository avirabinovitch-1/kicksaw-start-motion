---
name: design
description: Start Motion stage 2.1 (/start-motion:design). Drafts, updates and finalizes a Kicksaw solution design document: the data and object model, one section per capability or integration, security and access, reporting, and the diagrams needed. Written for the SA from the SOW and the discovery documents, finalized once the client has confirmed scope. Use whenever someone says "start the solution design for [client]", "update the design", or "get the design ready to share".
---

# Kicksaw solution design

The design shows how we will build the solution in Salesforce, capability by capability. It is written for the delivery team and shareable with the client. It is not a scope recap: the readout covers what and why; the design covers how. The SA owns it; Claude drafts and keeps it current.

Reference examples, by Steph McAllister: the Crossroads Treatment Centers Solution Design (https://claude.ai/artifact/E45dBFHcyYyk8R3Pxnw1pw), organized by integration, and the Healthcare Legal Solutions Client Portal Solution Design (https://claude.ai/artifact/Gdit1JR6FzURLvhq67jqAm), organized by capability. Match their structure, depth and look, not their content.

## Start: where the design stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page. Read `references/decisions.md` too: how every design choice is sorted, logged and put in front of the SA (section 3d). And read `references/drive-copies.md`: the design's master copy is an HTML file in the client's Drive folder, one running document saved as a new version each run, never a file that lives only in someone's Claude account.

This skill covers three moves that are three separate prompts on the page: starting the draft, keeping it current from calls and decisions, and getting it ready to share once scope is signed. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the signed SOW; the discovery documents (current to which call; the Integrations and Open items tabs; the data list if there is one); the readout (none, draft at which version, or signed on which date); the current org (access or not, when the client already runs Salesforce); third-party contacts and any access worksheet or data dictionary; and whether a design already exists (look in the client's Drive folder, `Design` subfolder, first; then its version, status, Draft or Final, the TBDs still open, and the Decisions tab: how many Decided and how many Proposed, by kind). For example: "Tog. SOW found. Discovery documents current to S-09. Readout v1.1, not yet signed. Org: client runs Salesforce, access not granted. Design: draft started Nov 18, 14 TBDs open, 3 answered on calls since. Next: fold in the calls since Nov 18."

## What to ask: one message

Ask once, in one message, and only for what the Start did not find. Starting the draft needs nothing beyond the client; organized by capability or by integration is proposed in the section plan (section 1), not asked. Updating needs nothing; the calls since the last update are read. Getting it ready to share needs the readout version that was signed, if readout/sign-off.md does not say.

Then read back what you heard in one line and run.

## 0. Load what you need

From the client's Claude Project and the places it links:
- The signed SOW: confirmed architecture decisions and the section numbers to cite.
- The discovery documents: the requirements list (with its Integrations, Open items and Decisions tabs), the workflows, the session notes and their build notes, and the data and migration list when the project has one.
- The readout as it stands: recommended build, scope in and set aside, open decisions.
- The current org, when the client has one (an existing org, or a sandbox the team has started building in): the org summary at `docs/org-summary.md` in the client's repo, with a copy in the client's Drive folder. It lists the objects, fields, automation, access and pages that already exist, by their real names. When there is no summary, or the org has changed since it was written, get one first ("Start from the org" below).
- Any access worksheet or data dictionary.
- The design itself, when one exists: the current version from the client's Drive folder (`Design` subfolder), as `references/drive-copies.md` sets out. Every update starts from that file.

If the SOW, the requirements list or the workflows are missing, say which and stop. A missing data list is not a reason to stop; say the design has no data section to draw on. Never design from memory or from raw transcripts.

### Start from the org

A design written from the requirements alone can name a new field where one already exists, or miss automation the new build will collide with. So when the client has an org, the design starts from what is in it.

- Read a sandbox when there is one. A production org is read only when there is no sandbox to read and the person says so plainly in this conversation, naming the org ("yes, read Harborlight production"). Ask, and wait for that answer; "go ahead" to something else is not it. Hand the org reader the person's name with the confirmation. Reading changes nothing in the org, and it is still the client's live system.
- Where the session has a terminal with the Salesforce CLI signed in to the org and the client's repo on this computer (Claude Code, Cowork with the repo folder connected, Codex), start the org reader: `start-motion:org-reader`. Hand it the client's name, the org's alias, the repo path, the SOW's countable limits (custom fields per object and the like) and the date of the last summary. It pulls the org's configuration into the repo on its own branch and writes `docs/org-summary.md`. It reads configuration only, never records, and changes nothing in the org.
- Save a copy of the summary to the client's Drive folder so the SC and PM can read it.
- In Claude chat with no terminal, the org cannot be read from here. Use the summary in the client's folder if there is one and say its date; if there is none, say the design is being drafted without a read of the org, and mark every object and field it names as "to check against the org".
- Name existing objects, fields and picklist values exactly as the summary has them, and say plainly what is new. Where the design adds automation to an object that already has some, say how the two will work together.

## 1. Propose the sections

Before writing, reply with a one-screen plan and wait for the SA:
- Organized by capability or by integration, and why.
- The capability or integration sections, in order, each with the SOW section it comes from.
- The optional sections in or out, with the reason: building on an existing build, users and licensing, prototype screens.
- The diagrams each section needs.
- What is still TBD and what each one waits on.

## 2. The sections

Always in:
1. How to read this document. One paragraph on what the document is and is not; a current state to target state strip of three to five rows; a "what this covers" list with a link to each section.
2. Data and object model. A short lede, then a table: Object, API name, Relationship, Populated by (or Portal access and How access is granted for external users), Notes. Then the ERD.
3. One section per capability or integration (see step 3).
4. Security and access model. Who sees what, drawn for each kind of user when there are external users, then a table by layer: Layer, Salesforce feature, What it does for [client]. Cover org-wide defaults, record access, hierarchy, and object and field access.
5. Reporting and dashboards. Table: Component, Audience, Details, naming the objects and field API names behind each metric and any formula still to confirm. Then what is out of scope for reporting.
6. Diagrams needed. Each diagram, the section it belongs to, and where it lives.

Add when it fits:
- Building on an existing build: when this phase extends a foundation build. What it reads from that build and what can start before it is live.
- Users and licensing: when licence type or user counts shape the design.
- Prototype screens: when there is UI the client will react to.

## 3. Write each capability section

Four parts, in this order:
1. Lede: two or three lines on what it does, citing the SOW section that puts it in scope.
2. Flow: numbered steps, each with its actor (client, agent, system, or the integrated system) and what the step produces. Dashed for steps not decided yet.
3. Spec: an Element and Spec table. For an integration: trigger, direction and pattern, fields exchanged, fallback. For a new object: label and API name, record name format, record types, statuses, relationships, ownership.
4. Terms and callouts: a "What it means for [client]" table for every Salesforce term in the section, then callouts as needed: Recommendation (with the reason and what would change it), Dependency, Open, Note. Every Recommendation and every Open callout that is a design choice carries its decision ID ("Recommended · D-04", "Open · D-07, SA call") and matches its row on the Decisions tab.

## 3b. Design it simple and sound

Every section is written to these. The design reviewer checks them, and so does the Salesforce quality reviewer when the design is built.

- **Only what the scope needs.** Every object, field, record type, status and automation in the design answers a requirement in scope. Nothing is added "for later"; a later phase designs its own.
- **Standard before custom.** Use the standard object, field or feature when it does the job, and say which. A custom one needs its reason in the section.
- **Configuration before code.** A formula, roll-up or validation rule before a flow; a flow before Apex. Recommend code only where volume or complexity calls for it, as a Recommendation callout with the reason.
- **One copy of every fact.** Relate records with a lookup or master-detail instead of typing another record's name or values into flat fields, and show related values with a formula or roll-up instead of storing them twice. A flat field is right when it has to keep a value as it was on a date, when the thing it describes is not a record in Salesforce, or when a relationship would pass a platform limit. Say which, in the Notes column, so nobody "fixes" it later.
- **Lookup or master-detail on purpose.** Say which and why: who owns the child, what happens when the parent is deleted, whether roll-ups are needed.
- **Picklists over free text** for anything reported on, and a record type only where the process, the layout or the values really differ.
- **One automation per object and event.** Where the org already has automation on the object, say how the new behavior joins it. Never a second flow beside the first without a reason.
- **Access through permission sets,** as narrow as the requirement allows. Say what each kind of user can see and do, not only what exists.
- **Nothing in the org is removed or replaced quietly.** When the design retires a field, a flow, a rule or a sharing setting, it says so in an Open or Dependency callout: what goes, what depends on it (from the org summary), what happens to the data it holds, and that a person carries out the removal. Agents never delete from an org.
- **Limits counted.** Where the SOW or the platform sets a limit, the design shows the count before and after.

When the simplest sound design and what the client asked for pull apart, say so as a Recommendation with the reason and what would change it. Do not quietly design the heavier thing, and do not quietly drop what they asked for.

## 3c. The solution map: design the whole, build a slice at a time

Stories are refined and built a slice at a time (a sprint, which often holds part of one epic and part of another, or an epic), but the data model, the automation on each object and the access model are shared by every epic. A choice that suits the first epic can force rework in the fourth. So the design covers every epic in the signed scope, even ones whose stories are not refined yet, and settles the structure all of them share. Later epics can be thinner on detail; they cannot be missing from the structure.

The design carries a **Solution map** section, after the data model:

- **Every object the solution touches**, standard and custom, with each epic that creates, changes or reads it, and its relationships.
- **One automation owner per object and moment** (before save, after save, on a schedule, from a screen): the one flow (or trigger) that runs there, and which epics add a branch to it. A later epic extends that flow; it never adds a second one beside it.
- **Shared values and structure**: picklists more than one epic reports on, record types, the sharing model of each object, the permission set structure, naming conventions, and the integration touchpoints.
- **Open structural questions** that more than one epic depends on. Each is a row on the Decisions tab, and it has to be decided before the first epic that depends on it is planned.

Build only what an epic needs, but in the shape the whole map calls for: the field type, relationship, record type, flow structure and naming that the later epics will need, so they add to it instead of reworking it. Building in the right shape is not building for later; adding fields, values or branches no story in this epic asks for still is.

When a later epic's discovery or refinement changes the map, update the map first, then check what is already built against it, and log what has to change as a decision for the SA.

## 3d. Decisions: what moves and what waits

The kit's standard is `references/decisions.md`. In short: every design choice with a real alternative gets a row on the Decisions tab, sorted into one of four kinds, and only the work that depends on an open one waits.

- **Clear** (one sound answer under the SOW, the org, what the client said or 3b): make the call, write it in the design, log it as Decided by Claude. Nothing waits.
- **Recommended** (more than one sound answer, and a pick you can defend in a line): write the design on the pick with a "Recommended · D-n" marker, log it as Proposed with the pick. Nothing waits until the design goes Final.
- **SA call** (a real trade-off, or no defensible lean): write the options side by side in an Open callout, log every option's trade-off and your lean if you have one. Draft every other section.
- **Client call** (only the client can answer): Open callout, log it, and add an Open items question for the SC with its number in the row.

When unsure between two kinds, take the one that involves the SA more. A choice that sets aside a rule in 3b is never Clear.

Do not stop the draft to ask about any of them. Finish everything you can, then put the open ones in front of the SA at the end of the run (section 7). Names, layouts and formatting are not decisions; do not log them.

## 4. Render and save

- One running HTML document on the Kicksaw design system (list Design System artifacts; colors from the Kicksaw Brand Playbook V2). Header: "Solution design · [platform]", the client, a one-line subtitle, prepared by the SA, the date, the version, and a status: "Draft" until scope is confirmed, then "Final".
- Contents on the side with every section linked; numbered sections; tables over prose.
- Real API names in code style. TBD as a small chip wherever a detail waits on something, with what it waits on.
- The Solution map (3c) as its own section after the data model, as a table by object, with the epics in columns.
- Once a build plan exists, a link at the top to its design and build review page (`references/build-review.md`), where the SA sees every component the design turns into.
- A **Key decisions** section after the data model: each Decided row in a line the client can read (the decision, what was chosen, why, from the Chosen and Why columns), then the open ones with who decides each. Internal reasoning (effort, margin, anything about the relationship) stays on the Decisions tab.
- Diagrams: draw flows in the document as numbered steps. When the SA draws a diagram by hand in Lucid, embed or link it and caption it. A diagram that also appears in the readout is identical in both.
- Each capability section's flow names the workflow steps it carries out (W-IDs and step numbers from the workflow document), so the build plan can trace a task back to the client's process.
- A change log at the end: one line per version.

Save it as `references/drive-copies.md` sets out: the new version as HTML and PDF in the `Design` subfolder, the previous version moved to `Older versions`, then the Claude link republished from the same HTML. A run that changes the design always ends with a new version saved; a run that changes nothing saves nothing.

## 4b. Have the design checked

After a first draft, after an update that changes more than a TBD, and always before getting it ready to share, start the design reviewer: `start-motion:design-reviewer`. It did not see the design being drafted. Hand it the design as it stands; the requirements in scope (ID, statement, status, Scope), saying whether the scope is signed yet; the workflows in scope (each W-ID with its numbered steps and actors, from the workflow document, or from the signed readout's future state workflows once it is signed); the user stories when they exist; the org summary when there is one; the Decided rows of the Decisions tab (ID, Decision, Chosen, Why); and, when the run covers one epic's part of the design, the requirements of the later epics, so it can report what would close a door on them. Never hand it the Proposed rows, the transcripts or your notes.

Where the session cannot start a separate agent (Claude chat often cannot), read `references/agents/design-reviewer.md` in this skill's folder and run it yourself as a second pass, working from the requirements list and the org summary, not from memory of drafting. Say in the report which way it ran; a second pass in the same conversation is weaker than a separate reader.

What to do with the findings:
- An uncovered requirement: add it to the section it belongs in when the discovery documents say how it is met; otherwise add it as a TBD with what it waits on. Never design around a gap with an assumption.
- A conflict with the org where the summary settles it (a field that already exists, a name spelled differently): correct the design to the org's name. A conflict that needs a decision (two automations on one object, an access model that changes) becomes a row on the Decisions tab (usually an SA call) and an Open callout in that section.
- Something designed beyond the confirmed scope: mark it in the design and list it for the SA. The SA takes it out or raises it with the PM. Do not remove it on your own.
- Something heavier than it needs to be: where the lighter way is plainly sound and changes nothing the client would see, change the design and say so in the report. Where it is a real trade-off, log it as Recommended or an SA call with both options, and mark the section.
- A choice with a real alternative that no row records (the reviewer's Unlogged choices): log it under the right kind.
- Work that contradicts a Decided row: correct the design to the decision. If the design was right and the decision is now wrong, write a new row for the SA; never edit a Decided row.
- An unconfirmed detail: mark it TBD with what it waits on.
- Run the reviewer once, fix, and run it once more. Two passes at most. Whatever is still flagged goes to the SA as it is.

## 5. Keep it current

When asked ("update the [Client] solution design from today's call"): start from the current version in Drive, read the call, fold in what was decided, close the TBDs it answered with the date and source, and add new TBDs. A decision the call settled closes its row on the Decisions tab (Chosen, Why, Decided by the person who settled it, Source with the call and timestamp); a call that reverses a Decided row gets a new row and the old one is set to Superseded. Keep the document's tone, structure and look; add to it, never restyle it. Save it as the next draft version (v0.4 after v0.3), add the change log line, and list what changed.

## 6. Get it ready to share

When asked ("get the [Client] design ready to share"), once the client has confirmed scope:
- Check every section against the confirmed scope. Anything set aside comes out; anything added is in.
- Close every TBD the readout review answered. List the ones still open, each with an owner.
- No Recommended row or SA call still Proposed. If there are any, show the decision picker for them and wait; that is the one thing this step waits on. Client calls still open are listed with their owner and do not stop it, unless a capability in scope cannot be designed without the answer.
- Clear rows: when the SA approves, mark each "Claude · accepted by <SA> with the design, <date>".
- Check the bar: every capability in scope has a section; the data model is complete; security is layer by layer; every recommendation has its reason; every term the client may not know is explained; nothing confidential about the relationship is in it.
- Set the status to "Final", the version to v1.0, and list what the SC, PM and build lead should review before it goes to the client.
- Save v1.0 to Drive with its PDF (the PDF is what goes to the client). When the client has a repo, also commit the same HTML as `docs/solution-design.html` on a branch for the SA to merge, with the version in the commit message: the build plan plans against that version.
- Any change after Final (a change order, a decision reversed during build) is v1.1 and up, saved the same way, and the change log says which stories and build tasks it touches.

## 7. Report back

Three short paragraphs: what the design covers and how it is organized, the version saved (with the Drive file and the Claude link), what is still TBD and who answers each one, and what the SA should check. Then the design reviewer's findings that are still open, each in one line (uncovered requirements by ID, conflicts with the org, anything beyond scope), the date of the org summary or record of the org the design was written against (or that there was none), and one line on how the reviewer ran. No recap of steps.

Then the decisions, the way `references/decisions.md` sets out: in Claude chat when an interactive visual can be shown, the decision picker (`references/decision-picker.html`, only its `CFG` line changed) with the SA calls and client calls, the recommendations to confirm and the clear calls you made; everywhere else, the same in the plain text block that file gives. One line above it, for example: "Two calls need you, three I went ahead on, eleven I made. Everything else is drafted." When the answers come back, write them to the Decisions tab, update the sections they unblock, and say in one line what changed. Skip this when no row is Proposed and no Clear row was added in this run. Then the design reviewer's findings that are still open, each in one line (uncovered requirements by ID, conflicts with the org, anything beyond scope), the date of the org summary the design was written against (or that there was none), and one line on how the reviewer ran. No recap of steps.

End with one line naming what comes next: after the first draft, keep it current with `/start-motion:design` after each systems session, third-party call or decision; after scope sign-off, `/start-motion:design` gets it ready to share and the SC, PM and build lead review it; once it is shared, `/start-motion:user-stories` writes the stories with the design in hand; once the stories are refined and the SA has approved the design, `/start-motion:build-plan` turns them into build tasks.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:design (v0.1.7) · design · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- Never invent an object, field, API name, number, date or quote. If it is not confirmed, it is TBD.
- Never record a decision as made by a person who did not make it. Claude decides only Clear rows, and says so in Decided by.
- A decision never stops the whole run. Only the work that depends on it waits.
- Follow the confirmed scope. The design never widens it.
- No requirement IDs or traceability tables; the requirements list holds that.
- No em dashes.
- The SA reviews every draft; the team reviews it before the client sees it.
