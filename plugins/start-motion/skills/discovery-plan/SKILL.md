---
name: discovery-plan
description: Start Motion stage 2 (/start-motion:discovery-plan). Builds the discovery plan for a Kicksaw client before kickoff, from the SOW and whatever else is in the client's folder (sales and pre-kickoff calls, a handoff doc, client documents), and prep the SC before each session. The plan sorts every SOW line by what the client has already said (known, needs confirming, unknown), turns the gaps into questions, groups the questions into sessions with a timed agenda and a must-leave-with list, and checks that no SOW line is left without a session. Before each session it updates that session in the plan and, if the SC wants one, builds a client-facing session deck. Use whenever someone says "plan discovery for [client]", "build the discovery plan", "what sessions do we need", "prep me for [session]", "make the deck for [session]", or "what do we already know going into discovery".
---

# Kicksaw discovery plan

Two requests. "Plan discovery for [Client]" builds the plan once, before kickoff. "Prep me for [Client] D4" (or a topic), the day before a session, updates that session in the plan, gives the SC the headlines in chat and offers a deck for the session. The discovery call skill updates the plan after every call; this skill does not process calls.

The plan is an internal Kicksaw document. It is direct about risks, politics and gaps. Three client-facing things are produced from it and nothing else is sent to the client: the session list for the kickoff deck's Discovery sessions slide, the inputs request, and a session deck when the SC asks for one.

## What the plan is for

A generic session list tells the SC what discovery usually looks like. A plan tells them what discovery has to find out for this client. The difference is one question asked of every SOW line: do we already know this, or not? Sales calls usually answer a third to half of what a generic plan would ask. The SOW says what has to be true by sign-off. The sessions come from what is left between the two.

The plan is a Claude page made from the Kicksaw Discovery Plan template. Everything on it is drawn from the `dp-data` block at the bottom of the page: the SOW lines, the people, the risks, the sessions, the questions, the inputs, the decisions. Nobody edits the markup.

## Start: where the client stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else.

- "Plan discovery for [Client]": the signed SOW (found, and which edition); everything else in the client's folder, every subfolder included (calls with transcripts and without, a handoff doc or IKT, client documents: what is there, in one clause; nothing beyond the SOW is not a gap, it is the normal case); whether the discovery documents exist yet (the Discovery documents note and the requirements list); and whether a plan already exists for this client (then this is an update, say so and change only what is asked). For example: "Tog. SOW found (Oct 3 edition). Beyond the SOW: four calls, three with transcripts, one MP4 without; no handoff doc. Discovery documents: set up Oct 20. No plan yet."
- "Prep me for [Client] [session]": the session on the plan (ID, name, date, attendees); the last call processed and whether anything since is unprocessed; inputs the session depends on and which have arrived; what the client has been told about it.
- No discovery documents yet: say so and offer to set them up first (`/start-motion:discovery-call` does it from the SOW), because the plan seeds the requirements list's Open items and Sessions and sources tabs and cannot finish without the sheet. If nothing at all turns up for the client (no Drive folder, no SOW), offer `/start-motion:new-client` first: it sets the client up and names the stage to run next.

## What to ask: one card, or one message

Ask once, and only for what the Start did not find.

**In Claude chat, when you can show an interactive visual,** show the Start and the ask together as one card: `references/start-card.html`. Change only the `CFG` object at the top of its script, never the rest:
- `client`, `stage` ("Discovery plan").
- `items`: one per readiness item from the Start, each with `need` (1 for needed, 0 for helps), `state` (`ok` found, `miss` missing, `warn` found with a problem, `none` not there and that is normal) and a one-line `detail` (where it was found, or what to do). A `none` item's `detail` is a short phrase ("no handoff doc from sales"); the card lists those on one quiet line.
- `form`: building the plan asks for the kickoff Monday, the discovery length in weeks, the session days, the mode (remote, on site, mixed), weeks that run differently, and what the SC already knows about the people and the politics. Prefill every value you found (the Discovery documents note's client settings, the SOW's timeline); leave a field empty only when nothing says. Keep the field ids and types the template uses; `calcAfter: 'weeks'` shows when discovery ends.
- `send` ("Plan discovery for [Client]."), `button` ("Build the plan").

The card sends back one message with each field as "Label: value". Treat it as the answer to this ask.

**Everywhere else** (Codex, Claude Code, or a chat that can't show visuals), report the Start in a few lines and ask in one message:
- Building the plan: the discovery window (weeks or dates), the session days, remote or on site or mixed, and anything the SC already knows about the people, the politics and the constraints. Say what you found for each and ask the SC to confirm or correct it.
- Prepping a session: nothing beyond the session, unless the request did not name one.

Then read back what you heard in one line and run: "Planning Tog discovery: four weeks from Nov 10, Tuesdays and Thursdays, remote. Reading the SOW and three calls."

## Where things live

| Thing | Where |
|---|---|
| The template | `templates/Kicksaw Discovery Plan.template.html` in this skill's folder, with the two logo files in `brand/`. A viewing copy sits in the shared Drive folder **Kicksaw Discovery Templates** (https://drive.google.com/drive/folders/12FPcdOBwsCyCN42FsbRB7GW0DdJ2QDmh); the plugin's copy is what Claude builds from. Preview: https://claude.ai/artifact/DG9bga86fMsBuVRY5NYu1t |
| The client's plan | A new artifact, "[Client] Discovery Plan", linked from the Discovery documents note in the client's Claude Project |
| The SOW and the calls | The client's Drive folder: the signed SOW (the latest revised edition, not a redline), whatever sales shared (call transcripts as PDF, VTT or Google Docs, and the IKT or handoff doc, in a sales subfolder when there is one), and tl;dv for any call recorded there |
| The questions | Also seeded as the Open items tab of the client's requirements list, with the same numbers, so the call skill can mark them answered |
| The session list | Also seeded as the Sessions and sources tab of the requirements list (S-IDs for the sales calls, D-IDs for the planned sessions) |
| Email, Slack and Jira | Listed in the Discovery documents note in the client's Claude Project: the client's email domain, the internal Slack channel and the Jira project |
| A session deck | A new Slides artifact, "[Client] [session ID]: [session name]", made only when the SC says yes during prep |

## Building the plan

### 0. Gather

Read everything before writing anything. Ask only for what cannot be found.

- The SOW: find the signed or latest revised edition in the client's Drive folder. If there are several, use the one with the latest date and say which one in `builtFrom`. Read all of it: scope, confirmed decisions, assumptions, change-order triggers, out of scope, deliverables, acceptance criteria, timeline, roles.
- Every sales and pre-kickoff call: whatever sales shared in the client's Drive folder, and tl;dv. A VTT needs decoding; a PDF transcript reads straight through the Drive connector. Note each speaker and whether they are client, Kicksaw, Salesforce or vendor. Claude cannot read video or audio files (MP4, M4A, MOV). For each one, look for its transcript in tl;dv, the Google Meet or Zoom transcript, or a Chorus export; if there is none, list it in `builtFrom` as not read, ask the seller for one and carry on. Calls recorded on a Salesforce AE's account are usually not shared with Kicksaw; ask the AE for those transcripts. If a transcript has no speaker names, attribute a quote to a person only where the call makes it clear who is speaking; otherwise attribute it to the client side as the call shows it (for example "client leadership") and mark the line confirm, not known.
- The IKT or sales handoff doc, if there is one: names, products licensed, risks and gotchas the seller wrote down, open items.
- Any client documents in the folder, from the sales cycle or since: questionnaires, reverse demo notes, exports, system or vendor PDFs. Read them like the calls; what the client wrote down is the client's own words.
- Only the SOW is required. With no sales calls and no handoff doc, build the plan from the SOW and whatever else is there, and list in `builtFrom` what was read; nothing beyond the SOW is a fact in the report, not a gap.
- What the SC already knows: the prompt may carry dates, the mode (remote or on site), constraints and names. Use them.

### 1. List what the SOW commits to

Make one line per thing discovery has to settle. Not the SOW's paragraphs: the commitments inside them. Each line gets an ID (S-01 onward, by area), the SOW reference, and an area. Areas are the SOW's own shape (workstreams, then cross-cutting: security, migration, reporting, governance). Include:
- every in-scope capability, flow and integration
- every confirmed architecture decision (these are things to confirm, not to re-open)
- every assumption that discovery is meant to confirm (volumes, counts, release levels, API dates, access)
- every decision the SOW says is made during or by the end of discovery
- every deliverable discovery produces
- the roles and named people the SOW expects
- the out-of-scope items and change-order triggers (so the scope watch list starts on day one)
- the timeline constraints

Sixty lines for a three-workstream SOW is normal. Fewer than twenty means something was summarized that should have been listed.

### 2. Sort every line by what the calls already told us

For each SOW line, search the transcripts and mark it:
- **known**: the client said it, with a quote. The quote, the speaker with their role, and the call and timestamp go on the line. Lightly cleaned of filler, trimmed with "...", never paraphrased.
- **confirm**: heard once, or from one person, or a Kicksaw or Salesforce person said it and the client agreed with a word, or the SOW's figure is a reconciliation rather than the client's own number. Quote what was heard and say in `note` why it still needs confirming.
- **unknown**: nothing on the calls. Say in `note` what exactly is missing.

With no sales calls, most lines start as confirm or unknown. That is expected, not a gap in the plan; say so in the report.

Rules:
- Only the client's statements make a line known. A seller's summary of the client does not.
- A line is known when its substance is known, even if its details are not; the details become questions.
- Never invent a quote, a number, a name or a date. If it was not said, the line is unknown.
- Things said on a call that are not in the SOW go on the scope watch list, not on the SOW lines. Tell the SC about each one.

### 3. The people

From the calls and the handoff: everyone met, with their role, what they decide, what they care about (with a quote), and the sessions they belong in. Then everyone the SOW or the calls say exists but nobody has met: the role, why discovery needs them, and the sessions. Mark a person whose name conflicts between sources (an IKT says VP of IT, the SOW says CIO) as to confirm. List anyone who has stepped back so nobody schedules them.

### 4. The risks

Three to eight things that could stop discovery closing on time, from the SOW and the calls, not from a generic list: a vendor dependency that lands after discovery, a decision with no owner, a single client contact carrying everything, a political decision, a system nobody understands, a compressed calendar. For each: what it is (with the evidence), and how the plan handles it (which sessions, inputs and decisions). The risk is only worth listing if the plan does something about it.

### 5. The questions

Every unknown and every needs-confirming line becomes one or more questions, Q-01 onward. Each question has: who can answer it (a person who decides, knows, or does the work; never "the client"), the session it belongs to, and whether it blocks design (a story cannot be written without the answer). Keep each question answerable in a sentence. Forty to sixty questions for a three-workstream SOW is normal.

### 6. The sessions

Group the questions and the SOW lines into sessions by who has to be in the room and what has to come first. Then:
- A reverse demo comes first, or right after the kickoff: the people who do the work, in the systems they use today. Design nothing in it.
- When there were no sales calls or handoff doc, the kickoff or the first session gives ten minutes to what the client was told during the sale and what they expect, so a promise nobody wrote down comes out in week one.
- Each session is 60 or 90 minutes. If a group of topics needs more, split it by audience, not by cutting the agenda.
- The attendees are named by role with why they are there: decides, knows, or does the work. Every session has at least one knower or doer besides the client lead.
- `heard`: the quotes from the calls that this session would otherwise re-ask. These open the session as a two-minute confirmation, never a re-ask. This is what makes the plan feel specific to the client and saves the time for the unknowns.
- `must`: the two or three things the session cannot end without. This is what tells the SC what to cut mid-call. Everything else on the agenda can slip to the flex slot.
- `agenda`: timed items that add up to the length. Known items get the short slots; unknowns get the long ones. A note on an item says what to put on screen or who speaks first.
- `questions`: the Q-IDs the session answers.
- `inputs`: what the client must send before the session, with an owner and a by-when. These also go on the inputs list.
- `dependsOn` and `feeds`: which sessions come first, and which document, decision or deliverable the session produces for.
- `covers`: the S-IDs.
- Put a flex slot in the last week, unscheduled with the client, for whatever is still partly covered.
- The calendar: week and day numbers from kickoff, morning or afternoon. No day has more than two sessions. Check holidays inside the window (a kickoff "week of" a Monday holiday is a four-day week). Note in `window.flex` the moves that are possible when a key person can only give one day.
- The playback or close-out is the last session, with the sponsor present and every SOW decision on its agenda.

Do not copy a session list from another client. The sessions fall out of the questions.

### 7. Inputs and decisions

- Inputs: everything the client must provide, I-01 onward, with owner, by-when and the sessions that use it. "Before kickoff" items are the readiness checklist that keeps day 1 off logistics: access, named roles, vendor contacts, API documentation, exports. Each line should be pasteable into the request email.
- Decisions: every decision the SOW says is made during discovery, plus any the calls show is open, numbered, with an owner, the target session, and a note on where it stands from the calls.

### 8. Check coverage

Before writing the page: every SOW line has at least one session; every working session covers at least one SOW line (kickoff, playback and the flex slot are the exceptions); every question sits in a session; every agenda adds up to its length; every known line has a quote. Check each of these yourself before writing, and list any gap in the report. Fix the gaps or say why a gap is intentional.

### 9. Write the page and seed the lists

- Take `templates/Kicksaw Discovery Plan.template.html` and the two logo files in `brand/` from this skill's folder. Never take them from anyone's artifact. Check that `project.template` is true in its `dp-data` block; if not, stop, it is not the template.
- Replace the `dp-data` block with the client's data: `template` false, `updated` "before the first session", `builtFrom` listing every source read and any not read, `changes` with one entry saying the plan was built and nothing is covered yet. Set the `<title>` to "[Client] Discovery Plan". Publish as a new artifact with the two logos in `files` as `brand/primary-full-color.svg` and `brand/primary-inverse.svg`.
- Requirements list: add the questions to the Open items tab with the same Q numbers, and the sessions to the Sessions and sources tab (the sales calls and the handoff call as S-01 onward, in date order, with their links; planned sessions as D-01 onward with the planned date and attendees). If the requirements list does not exist yet, run `/start-motion:discovery-call` setup first.
- Add the plan's link to the Discovery documents note in the client's project.

### 10. Report back

**In Claude chat, when you can show an interactive visual,** report with the plan review card: `references/plan-review.html`. Write one line above it ("The Harborlight plan is built. Here it is to check.") and change only the `CFG` object at the top of its script:
- `client`; `url` (the plan's link); `known`, `confirm`, `unknown` and `lines` (the SOW line counts); `qs` and `blocking` (questions, and how many block design).
- `gaps`: every SOW line with no session, each with `id`, a short `text` and `why` (an intentional gap says so: "On purpose: introduced at kickoff, not a client question"). Empty when every line is covered.
- `risks`: the risks' titles, one line each.
- `weeks`: a label per week number ("Nov 23 to 27 · Thanksgiving week, sessions Mon and Tue only").
- `sessions`: each with `id` (D-01 style), `wk`, `date`, `slot` (Morning or Afternoon), `len` (minutes), `name`, `who` (client attendees as on the plan), `room` (up to three first names and "+n", for example "Dana, Priya, Marcus +3"), `must` (the must-leave-with list) and `n` (SOW lines covered; 0 for the flex slot).
- `scq`: the three to five questions only the SC can answer.

The card sends back one of four messages: the plan looks right; session changes and answers to apply (show what changed, then update the plan and the requirements list); put the sessions on the kickoff deck's Discovery sessions slide (`/start-motion:kickoff` does it); or draft the inputs request. Below the card, give the inputs request ready to send only when asked.

**Everywhere else,** reply in text: four short paragraphs: what we walk in knowing (the known / confirm / unknown counts and the three or four biggest unknowns); the risks the plan is built around; the sessions in one line each with who is in the room; and what the SC should settle before kickoff. Then the client-facing session list (ID, name, length, attendees by role) ready for the kickoff deck, and the inputs request ready to send. Then the three to five questions only the SC can answer: things the calls do not settle about politics, availability, on site or remote, and who really decides.

Either way, keep the plan's internal notes out of anything client-facing, and end with one line naming what comes next: `/start-motion:kickoff` builds the kickoff deck, and its Discovery sessions slide takes the session list above; if the discovery documents are not set up yet, `/start-motion:discovery-call` sets them up from the SOW.

## Prepping for a session

"Prep me for [Client] D6" the day before. The prep goes into the plan itself, not a separate page, so the plan stays the one place the SC looks and nothing drifts from it. Then a few lines in chat, and an offer of a deck.

### Read first

- The plan, the requirements list (Open items, Sessions and sources) and everything since the last call: the latest session note and the call skill's last report.
- Email, Slack and Jira since the last session, from the places the Discovery documents note lists (see the rule below). If one of them is not listed or not connected, say so in the headlines and carry on without it.
- What the client has already been told about this session: the kickoff deck's Discovery sessions slide, the calendar invite, and any email to the client about it.

### Update the session in the plan

Read the plan by URL, change only this session in the `dp-data` block, and publish to the same URL. Keep every ID.
- **Questions**: put the session's questions in the order to ask them, blocking ones first. A question already answered on another call or in a client email is marked answered with the quote and its source and comes off the agenda.
- **Must leave with**, as it stands now.
- **Heard**: add the quotes from discovery calls and client emails since the plan was built, so the first minutes confirm them rather than re-ask.
- **Agenda**: revise the timing if the must-leave-with list or the attendees changed. Each item's note says what to put on screen, who speaks first and what to have ready: the inputs that arrived, and for the ones that did not, the fallback (who can pull it live, or what to cover instead).
- **Attendees**: anyone added or dropped since the plan was written.
- An entry at the front of the session's `updates` list, marked as prep, in one or two lines: what changed since the plan was written and what is still unconfirmed.

Do not move the session's date or time if it has been shared with the client.

### Check against what the client was told

Compare the session as it now stands with what the client has already been told: date, time, length, attendees, topics and what they were asked to bring. List every difference in the headlines, with what the client was told and where. Do not change what was shared; the SC decides whether to tell the client.

### The headlines in chat

A few lines, not a page:
1. Any input the session depends on that has not arrived, first, with the fallback.
2. What changed since the plan was written.
3. Must leave with.
4. The two or three questions that matter most, and who in the room can answer each.
5. Anything that differs from what the client was told.

**In Claude chat, when you can show an interactive visual,** give the headlines as the start card (`references/start-card.html`) instead of lines: `stage` is the session ("D-04 Triage, assignment and the ownership line, Thu Nov 19"); `items` are the headlines (an input not arrived is `miss` with its fallback in `detail`; a change since the plan, or a difference from what the client was told, is `warn`; must leave with and the top questions are `ok`); `form` is empty; `alt` is one button, "Build the session deck", whose prompt asks for the deck; `button` is "I'm set, no deck" and `send` says so ("Prep for Harborlight D-04 is done; no deck."). Everywhere else, give the lines above and ask: "Do you want a deck for this session?" If the SC says no, the prep is done. If yes, build it as below.

### The session deck (only when the SC says yes)

Build it from the session as just updated in the plan, as a Slides artifact named "[Client] [session ID]: [session name]".
- Six to eight slides: a cover; the timed agenda; what we heard, to confirm; one slide per working topic with its questions; a wrap-up with the actions, their owners and the next session.
- The look follows the kickoff skill's design rules (`/start-motion:kickoff`, its `references/kickoff-templates.md`): the Kicksaw Design System, the Brand Playbook colors, Inter and Source Sans 3, and the logo rules. If the client already has a Kicksaw deck (the kickoff deck), match it. The footer reads "<Client> × Kicksaw · [session name]" plus the slide number.
- Plain language for client staff: about six bullets a slide at most, tables wherever there are rows. The quotes on the what we heard slide are the client's own words from calls or client emails, lightly cleaned.
- Brief speaker notes, written for someone presenting who is new to the client: what the slide is for, who in the room to turn to, and what to cut if time runs short.
- Nothing internal on the slides or in the notes: licenses, cost, risks, staffing, politics, or the plan's own notes.
- Reply with the link, and remind the SC to use the Share menu before sending the deck to the client.

Whether or not a deck was built, end the prep with one line naming what comes next: after the session, `/start-motion:discovery-call` processes the call the same day.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:discovery-plan (v0.1.2) · discovery · <client> · <date>
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
- Plain language a consultant would use. No invented terms.
- Quotes come from transcripts or the client's own emails, never from notes, summaries or internal messages. A call quote carries speaker, role, call and timestamp; an email quote carries sender, role, date and subject.
- Email, Slack and Jira: read them where the Discovery documents note lists them: email threads with the client's email domain, the internal Slack channel (threads included, and the PM bot report posted there) and the Jira project. Read only what is new since the last session. Client emails are the client's own words: they can make a line known and are cited like a call. Internal Slack messages, the PM bot report and Jira are context only: they never count as something the client told us and are never quoted to the client.
- Session dates and times already shared with the client stay put. Work inside them. A new session, or a move, is proposed to the SC first and never written to the plan unasked.
- Never invent a name, number, date, owner or quote. If it was not said and is not in the SOW, it is a question.
- Staffing, commercial notes and SOW risk belong on the plan (it is internal) but never in the client-facing session list or the inputs request.
- IDs never change once given. New lines, questions and sessions are added at the end; a dropped session is marked cancelled, not deleted.
- The plan is updated by the discovery call skill after every call. This skill builds it once, and during prep changes only the session being prepped.
