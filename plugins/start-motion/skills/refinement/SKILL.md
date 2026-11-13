---
name: refinement
description: Start Motion stage 3 (/start-motion:refinement). Prepares and folds in Kicksaw refinement sessions with a client's product owner. Lets the SC pick the stories for an upcoming session by sprint, by epic or one by one, works up each open question with what we know and Kicksaw's proposal, builds the refinement deck from the finished slides (each story with its questions, a detail slide where a question needs a picture, the acceptance criteria to confirm, and where we landed), and briefs the SC in the chat on how to run the call and what each story needs. After the call, folds the product owner's answers into the stories in Jira from the recording. Use whenever someone says "prep refinement for [client]", "build the refinement deck", "which stories should we refine", "get me ready for the [client] refinement call" or "fold in today's refinement".
---

# Kicksaw refinement

Two requests. "Prep refinement for [Client]" before a session: the SC picks the stories, and gets a deck to send ahead and present, plus a short briefing in the chat on how to run the call. "Fold in today's [Client] refinement" after it: the product owner's answers go into the stories in Jira, from the recording.

The stories are already in Jira; `/start-motion:user-stories` put them there as New, each with its acceptance criteria and its open questions. Refinement is where those questions get answered and the criteria get confirmed, ahead of the sprint that builds them.

The deck is for the client. It is the stories in a form a product owner can read, think about before the call and answer on it: each story, the questions still open on it, what we already know, and what Kicksaw proposes. A consultant who prefers to run the call from Jira still sends the deck ahead.

## Start: where the backlog stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the SC makes, the bar, and the link to the full method on the Start Motion page.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found in a few lines before doing anything else: the client's Jira project and its key; how many stories are in it by status (New, Pending Client Approval, Refined and later); the sprints in Jira and which one is next; how many stories in the next sprint are not yet approved, and how many open questions they carry between them; the product owner (named in the Discovery documents note, or not); the next refinement session on the calendar (date, or none found); the last refinement call and whether it has been folded in. For example: "Tog. Jira: TOG, 41 stories: 29 New, 4 Pending Client Approval, 8 Refined. Next sprint: Sprint 2 (Nov 4 to 17), 9 stories, 6 not yet approved with 11 open questions. Product owner: Dana Ruiz. Next session: Thu Oct 29. Last session, Oct 22: folded in."

If the last refinement call has not been folded in, say so and offer to do that first: its answers change what this session needs to cover.

If no stories are in Jira for the client, say so and stop; `/start-motion:user-stories` comes first.

## What to ask: the SC picks the stories

The SC chooses which stories this session covers. Offer the three ways to pick, and propose a starting set so the SC only has to adjust it:

- **By sprint:** every story in one sprint that is not yet approved. The default, on the next sprint.
- **By epic:** the stories under one epic that are not yet approved, in build order.
- **Specific stories:** the SC names them or finds them in the list.

Not yet approved means the story's status is New or Pending Client Approval. Propose, already ticked: the next sprint's stories that are not yet approved, plus any story from the last session that still has a question open. Six to ten stories fit a typical call; if the set carries more than about twelve open questions, say so in one line and suggest which stories could wait for the next session. The SC decides.

For each story the list shows its key, its title, its epic or sprint, how many questions are open on it, and whether it carries a design question (so the SC knows to invite the SA). A design question is one about how something is built or what the platform can do, not about what the business needs.

**In Claude chat or Cowork, when you can show an interactive visual,** show the story picker: `references/story-picker.html`. Change only the `CFG` block at the top of its script: `client`; `session` (the session's name and date, for example "Refinement 2 · Thu Oct 29"); `mode` ("sprint", "epic" or "one") and `pick` (the sprint or epic it opens on); and `stories`, one row per story that is not yet approved, across every sprint and epic, as `[key, title, epic, sprint, open questions, 1 if it carries a design question else 0, 1 if you propose it else 0]`. A story with no sprint has an empty sprint. Send everything else as it is. Write one line above it, for example "Here are the stories I'd bring to Thursday's session. Change anything, then press Build the refinement deck."

**Everywhere else,** send the same list as text, grouped by sprint or epic, with the proposed stories marked, and ask the SC to reply with the keys to bring.

The picker sends back the list of stories in the order to take them. Take that order as it is.

## 1. Read the picked stories

For each story the SC picked, read it in Jira as it stands now: the Summary, the User Story, the Description (the client's words and the Refined on blocks from earlier sessions), the Acceptance Criteria and the Open Questions. Read the epic it belongs to and the sprint it is in.

Then read what the questions depend on: the signed solution readout (the workflow and step each story's Source line points to), the solution design if there is one, the Open items and Decisions tabs of the requirements list, and the session notes for the calls the story cites. Open a tl;dv transcript when a question needs the client's words; quotes follow "The client's words" in `/start-motion:user-stories`: always from the transcript, lightly cleaned, cited with the speaker and the date.

Run the story reviewer on the picked stories as they stand in Jira, since they may have changed since it last read them. Where the session can start a separate agent, start `start-motion:story-reviewer` and hand it the stories only; where it cannot, read its instructions at `references/agents/story-reviewer.md` and run them yourself as a second pass. A gap it finds, where the architect or the tester would have to guess, joins the story's questions for this session, worded as a question to the product owner. The reviewer is advice: it never keeps a story out of a session and never holds back a status.

## 2. Work up each question

A question on a slide has four parts. Write all four for every open question on every picked story:

- **The question,** in the client's language and short enough to read aloud. One decision per question. If a Jira open question holds two decisions, make it two.
- **What we know:** two or three lines on where things stand and where the question came from: how it works today, what the client said and when, what the data shows. Only what the sources say.
- **Our proposal:** what Kicksaw recommends, in one or two sentences the product owner can say yes to. Take it from the story as written, the signed readout, the solution design or a decision already logged. Where the sources give no basis for a recommendation, do not invent one: write "No proposal yet: we need your direction" and say what the choices are.
- **The criteria it affects,** by number, or "a new criterion" when the answer adds one.

Then decide whether the question needs its own slide. Most do not. It does when a picture explains it better than a sentence: a rule over time (a due date, a reminder), things grouped (sources into queues, roles into profiles), or who can do what and what happens in which case. `references/refinement-deck.md` has the three kinds.

Number the questions through the whole deck, 1 to n, in the order the stories are taken.

**Show the SC the questions and proposals before building.** One message: each story, its questions, and the proposal for each in one line, with any "No proposal yet" called out first. Ask the SC to change any proposal they would not stand behind, then to say build. A proposal goes to the client under Kicksaw's name, so the SC sees every one first. If the SC said "just build it", build, and list the proposals in the briefing so they can still be changed.

Proposals are for the deck. Do not write them into Jira; the story changes when the product owner answers.

## 3. Build the deck

Read `references/refinement-deck.md` before writing anything: the slides, their order, what each holds and the rules.

1. Build from the Slides artifact type, not a .pptx, unless a file format is named. Create the deck, named "[Client] refinement: [session or sprint], [date]", and apply the Kicksaw Slides design system the way the Slides type's instructions say, as `/start-motion:kickoff` does.
2. Copy `templates/refinement/deck.css` into the deck as `project/deck.css`, unchanged.
3. For each slide in the order `references/refinement-deck.md` gives, copy `templates/refinement/<slide>.html` into the deck as `project/slides/<id>.html`, with an id of its own (for example `ts21`, `ts21-detail`, `ts21-criteria`). Keep its markup and classes; change only the words.
4. Repeating items (story rows, question cards, criteria, table rows, columns) are added by copying an existing item or removed whole, within what the slide holds. Past that, use the slide that holds more, or split. Never shrink text and never change sizes, colors or spacing.
5. A story's title, sentence and acceptance criteria are copied from Jira. Do not reword a criterion for the slide. Where a criterion in Jira refers to a table or a list too long for the slide, give the sentence and say in the speaker notes where the rest is.
6. Mark each criterion a question could change with that question's number.
7. Upload the two logo files in `brand/` and point the slides at them. Footer on every slide: "<Client> × Kicksaw · <Sprint or session> refinement" and the slide number.
8. Speaker notes on every slide, written for someone who was not in discovery: what to say, what to ask and in what order, where the client spoke about it (the call and the date), and what to do if the answer is not ready.
9. Nothing internal on the slides or in the notes: sizing, hours, cost, staffing, build details, risks, or the reviewer's findings as findings.
10. `landed` lists every question with its proposal and leaves the last two columns to fill in on the call.

Look at every slide once it is built: no text shrank, the logo, title, rule and footer are in the same place on every content slide, every question has its proposal or says there is none, and nothing was invented. Fix what you find before handing over.

Reply with the link, and remind the SC to use the Share menu before sending the deck to the client.

## 4. Brief the SC in the chat

Right after the link, in the same reply, give the SC a short briefing on this session. The deck is what the client sees; the briefing is what the consultant needs to run the call well. Plain sentences, no slide-by-slide recap. Five parts, each a few lines:

- **Before the call:** when to send the deck (the day before, or two days for a long list), who has to be on the call and why (the SA, named, when a story carries a design question; anyone the product owner said decides a point), and anything the SC should check first, such as a proposal that rests on something not yet confirmed.
- **How to run it:** the order of the stories and roughly how long each needs, so the SC can see whether the call fits. For each story the pattern is the same: read the story, take its questions one at a time with what we know and the proposal, then confirm the criteria. Say which stories will go quickly and which one or two will take the time.
- **What each story needs:** one line per story: the questions to close, the criteria to confirm, and what "done" looks like for it today (approved, or approved once a named answer comes back).
- **If an answer is not ready:** it leaves with one owner and one date on the last slide, the story is built on the proposal where that is safe, and it comes back next session. Name any question where building on the proposal would not be safe, so the SC knows that one has to be settled on the call.
- **After the call:** fill in the last slide together before it ends; the call is recorded; the same day, `/start-motion:refinement` folds the answers into Jira ("fold in today's [Client] refinement"). Notes the SC takes during the call are welcome and can be pasted into that request, and the recording stays the source.

Keep it to what is true of this session. For example:

```
Before the call
Send the deck to Dana by Wednesday. Ask Ben to join: TS-33 carries a design question about how installs are scheduled. One thing to check first: the proposal on question 3 assumes the HR calendar is the holiday list, which nobody has confirmed.

How to run it
Three stories, six questions, about 45 minutes. TS-21 and TS-24 should take ten minutes each. TS-27 is where the time goes: three questions on what counts as a duplicate, and the table on slide 9 is the quickest way through them. For each story: read it, take the questions one at a time, then confirm the criteria.

What each story needs
- TS-21: answers to questions 1 and 2, then a yes on six criteria. Approved today if both are answered.
- TS-24: the hours and the holiday list (question 3). Approved today if Dana can confirm the holidays; otherwise it waits on HR.
- TS-27: all three answers. Do not leave question 6 open: web forms cannot be built on a guess.

If an answer is not ready
Give it an owner and a date on the last slide. Questions 1, 2, 4 and 5 are safe to build on our proposal; 3 and 6 are not.

After the call
Fill in the last slide with Dana before you close. The same day, run /start-motion:refinement and say "fold in today's Tidewell refinement".
```

## 5. Fold in refinement

When asked ("fold in today's [Client] refinement"), read the refinement deck for that session if there is one (its questions, their numbers and proposals are what the call worked through), then pull the tl;dv transcript for that session (if more than one call for the client happened that day, ask which) and add it to the Sessions and sources tab with the next S-ID. Read all of it and note each speaker. Then, story by story:

- **Match what was said to the stories in the deck, question by question,** and to any story the product owner brought up that was not on it.
- **For each story discussed, pull the product owner's words** for every answer, correction and addition, cited as "The client's words" in `/start-motion:user-stories` says. Take the passage where they say what they want and why, not where they say "yes".
- **Add a Refined on block to the Description**, one per session, between Source traceability and the footer:

  **Refined on Oct 28 2026 with Dana Ruiz (Refinement 2):**
  - "We never want a lead from a partner to go to a rep... [it goes] to the partner manager" Dana Ruiz, Sales Operations Manager, S-15 Refinement 2, Oct 28 2026, 00:12:05. Changed AC 1: leads with Lead Source = Partner go to the partner manager's queue. Closed open item 2.
  - "Blank is fine, an error would stop my team cold" Dana Ruiz, Sales Operations Manager, S-15 Refinement 2, Oct 28 2026, 00:14:40. Added AC 7: the field shows blank, not an error, when there is no territory.

  Each bullet is one quote and, in plain words, what it changed: the criterion number added, changed or removed, the open question it closed, or the field it added. If a criterion changes, keep the new wording in the AC field only; the block records why it changed.
- **Update the AC and the Open Questions fields** to match: rewrite the criteria that changed, add the new ones, remove the questions answered. A question the product owner raised and could not answer goes in as a new open question with their quote, and on the Open items tab.
- **Anything the product owner asked for that is beyond the signed scope** goes in the requirements list with Scope set to Beyond SOW and Scope decision empty, with the quote and citation; it never widens a story silently. Tell the PM that week.
- **A story the product owner approved** moves to Pending Client Approval or Refined, per the project's workflow. Say which stories moved. Never refuse or hold back a status because a reviewer found a gap: if a story that moved still has one, say so in one line with the question, and leave the call to the SC. Once a story is approved, it is built as written; nothing reviews it again at build.
- **Record new decisions in the Open items tab** with the quote, and update the Source footer line of the story to add the refinement call. A decision that answers a row on the Decisions tab closes that row as well (Chosen, Why, Decided by, Source with the call and timestamp), and the D-ID comes off the story's open question.
- Keep the story's tone and structure; add to it, never rewrite the parts the SC already approved unless the product owner changed them.
- **Notes the SC took during the call,** when they are pasted into the request, say where to look. Every change still comes from the recording: find the passage, and if a note has no passage behind it, say so and leave that change for the SC.
- **Where the product owner agreed with a proposal,** the criterion written on that proposal stands; record the agreement in the Refined on block with their words. Where the answer was different, rewrite the criterion to the answer.
- **Fill in the deck's last slide** if it was left empty: what was agreed, what is still open with its owner and date.

Stories then flow: New, Pending Client Approval, Refined, Build Ready, In Progress, Ready for QA, QA Testing, UAT, Done. The SC and SA size refined stories together; the PM, SC and SA load the sprint from them with input from the team.

## 6. Report back

After a prep: the link, then the briefing (section 4). Nothing else.

After a fold-in, three short paragraphs: which stories changed and the criteria touched, which stories moved status, and what is still open with its owner and date. Then any quote that could not be found in the transcript, and anything the product owner asked for beyond the signed scope. No recap of steps.

End with one line naming what comes next: after a prep, the same day after the call, `/start-motion:refinement` folds the answers in; after a fold-in, the SA adds build details to the approved stories and sizes them with the SC, and the PM loads the sprint; before the next session, `/start-motion:refinement` preps it.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:refinement (v0.1.10) · refinement · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: a proposal they rewrote, stories they swapped, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a project key, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.
