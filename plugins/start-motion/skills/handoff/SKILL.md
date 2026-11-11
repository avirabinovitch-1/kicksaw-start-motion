---
name: handoff
description: Start Motion stage 0 (/start-motion:handoff). Builds the sales-to-delivery handoff document for a new Kicksaw project on DJ's standard, from the signed SOW and contracts and the sales call transcripts, then draft delivery's questions for the salesperson. Use whenever someone says "build the handoff for [client]", "draft the handoff doc", or shares a sales handoff folder. The handoff call itself happens on every project; this command, which builds the document, runs when sales shares a packet beyond the SOW, and nothing downstream waits for it.
---

# Kicksaw sales handoff builder

## Start: where the packet stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

The handoff call with sales is held and recorded on every project; that discussion is what Kicksaw's Delivery Methodology requires. This command, which builds the handoff document, is optional. Delivery cannot count on more than the signed SOW and whatever else sales shares into the client's folder; `/start-motion:new-client` starts a client from the SOW without any of this, and no later stage waits for a handoff. The stage is here so the process is visible and sales can adopt it; when a packet beyond the SOW arrives, this is how it is handled.

This skill covers three moves that are three separate prompts on the page: building the handoff document (sales), drafting delivery's questions (the SC, PM, SA and EM/DM), and updating the document from the recorded handoff call. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the sales call transcripts (how many, named by date and call or not, and any recording with no transcript); the signed SOW (found, and whether it is the countersigned final); the contractual documents (MSA, order form, BAA when PHI is in scope, NDAs, amendments: which are there); the handoff doc (exists on DJ's standard, exists in another shape, or none); named client contacts; the handoff call (booked, and whether it is at least 24 hours after the packet). For example: "Tog. Transcripts: three Chorus exports, one MP4 with no transcript. SOW: countersigned Oct 3. Contracts: MSA and order form present; BAA not in the folder and PHI is in scope. Handoff doc: none. Contacts: sponsor named in the SOW. Handoff call: not booked. Next: build the handoff document." If nothing at all turns up for the client (no Drive folder, no SOW), offer `/start-motion:new-client` first: it sets the client up and names the stage to run next.

When the folder holds nothing beyond the SOW (no transcripts, no contracts past the SOW itself, no IKT, no client documents), say so in one line and stop: "Tog. Only the SOW in the folder; nothing to hand off yet. `/start-motion:new-client` starts from the SOW." A handoff document that restates the SOW is not worth anyone's reading time, and nothing downstream is waiting for it.

## What to ask: one message

Ask once, in one message, and only for what the Start did not find: the client's Drive folder, only when none turns up under the client's name, the transcript of any recording that has none, and a readable copy of any packet file that cannot be opened (section 0 stops on those). Nothing else; the document is built from what is there, and the gaps are flagged in it.

Then read back what you heard in one line and run: "Building the Tog handoff document from the SOW, the order form and three transcripts. The BAA and one transcript are flagged as missing."

## 0. Gather the packet

Look in this order, and record where each item came from:
1. The client's Google Drive folder and everything in it, every subfolder included: the signed SOW, and whatever sales shared (transcripts, contracts, a handoff doc). Subfolder names vary by client; read them all rather than looking for one by name.
2. A separate handoff folder, if sales shared one outside the client's folder.
3. Salesforce Opportunity Files for the signed SOW and contracts, when a Salesforce connector is available.
4. The Closed Won record or task (amount, opportunity ID, start date, lead source).

Sales calls are every call before the SOW was signed: discovery, demo, proposal and SOW review. Kickoff and later calls are not sales calls; use them only if labelled post-sale. Chorus has no connector, so sales exports each Chorus transcript into the folder as a file. A video or audio file is not a transcript: Claude cannot read MP4 or other recordings. List each one under "Where this came from" as not read and ask sales for its transcript. tl;dv holds delivery calls, not sales calls.

The contractual documents are the signed SOW, the MSA or PSA, the order form, a BAA when PHI is in scope, NDAs and amendments. Add the proposal and estimate if they exist.

Stop and build nothing if:
- the SOW is missing or is not the countersigned final;
- you cannot open a file in the packet.

In each case say exactly what is missing and where it should be, and ask sales to share the folder with the person running this.

No sales call transcripts is not a stop, as long as there is something beyond the SOW to hand off (contracts, an IKT, the deal's Slack thread, client documents). Build the document from the SOW, the contracts, the Closed Won record and anything else in the folder. Sections that need the calls (why they bought, client expectations, what was promised) read "No sales transcript provided". Put a line under the title saying which packet items sales did not provide. The delivery questions get longer, because the handoff call is now where those answers come from.

## 1. Read everything

Every transcript in full, in date order. Note each speaker and their role. The SOW decides what was sold; the transcripts explain why, and what was promised. If the lead source is a partner (for example Conga), ask sales for the partner's call notes too.

Check the SOW figures and dates against the Closed Won record and flag any mismatch.

Also read what was said internally when it exists: the internal KT or IKT notes, the deal's Slack thread, and the order form or license schedule. None of these is required; say in the "Where this came from" table which ones were there.

## 2. Build the handoff document on DJ's standard

The model is DJ's Industrial Software Solutions handoff: https://docs.google.com/document/d/1wgFsLosgKDtrcU50oo60nqfywvt48RjS/edit. Match its voice: a briefing from someone who sat on every call. Delivery judgement is welcome when labelled "Delivery read:". Never state a fact or number without a source.

Sections, in order:
1. Purpose of the document, in three lines
2. Summary table: engagement model, commercial value, initial priority, parallel priority, ongoing value, most important takeaway
3. Executive summary
4. Delivery thesis
5. Top delivery risks
6. Roadmap in waves, each with its primary outcome. Managed services: waves of capacity. Implementation: SOW phases
7. Project context: the first month, the rest of the engagement, how to read scope, how success is measured
8. Commercial structure and guardrails: term, hours, fees, payment, what uses capacity, what is excluded. Implementation: SOW phases, milestones and hours by role
9. What was sold: each element, the known requirement, the delivery interpretation
10. Current-state process and target operating model
11. Client expectations from the sales calls: what they said, what it means for delivery
12. Critical design decisions to resolve early
13. Client and Kicksaw responsibilities
14. Explicit scope boundaries: each exclusion with its SOW section number; quote only where the wording matters
15. Risk analysis: risk, why it matters, mitigation
16. Recommended delivery approach and a 30/60/90 focus (managed services: add a months 4 to 6 row)
17. Key open decisions for kickoff: decisions the client makes with us in the first sessions
18. Bottom line
19. Call recordings: one link per call

DJ's callouts (delivery thesis, top risks, design implication, delivery warning, the one-line mantra) can sit beside the sections they belong to.

Under the summary table: "Prepared from the signed SOW and the sales call transcripts", with the call dates.

## 3. Flag what does not line up

These go beyond DJ's model on purpose:
- A "Promised on a call, not in the SOW" table: quote, speaker, call. For a partner-sourced deal, add the partner's promises.
- Anything in the SOW nobody discussed on a call.
- Any date the client was promised, and any date that differs between the SOW and the Closed Won record.
- The SOW against what was said internally (the KT or IKT, the Slack thread, the Closed Won record): the billing model (monthly, milestone, fixed), what is built versus only surfaced or demonstrated, and any go-live date that differs between the SOW, our plan and what the client was told. Each disagreement is a flag with both versions quoted and where each came from.
- Licensing against the SOW: every promise that needs a license or a product (portal logins need Experience Cloud, payer-facing reports need the users who will read them, and so on) against what the order form shows was bought. A gap is a flag and a delivery question; never assume it will be sorted out later.
- A "Where this came from" table: each packet item and its location.
- A section with nothing to say reads "Not discussed in sales". Never fill it with a guess.

## 4. Draft delivery's questions

Add a "Delivery questions" section at the end for the SC, PM and SA to edit. These are internal questions for sales, unlike section 17. Only questions this packet raises, grouped by why they bought, people, what was promised, how it was sized, the environment, and watch-outs. Each question notes what prompted it. Leave out anything a transcript already answers.

## 4b. Delivery's questions, when delivery asks

When the SC, PM, SA or EM/DM asks ("read the [Client] handoff packet and draft the questions delivery should ask sales"): read the packet, including the handoff doc if sales already built it, and draft the questions only this packet raises, nothing a transcript already answers, grouped by why they bought, people, what was promised, how it was sized, the environment and watch-outs, with what prompted each one. Keep it to the 10 to 15 questions only sales can answer, most important first, and move anything only the client can answer to the open decisions for kickoff. If the handoff doc exists, write them into its Delivery questions section; otherwise hand them back in chat for the team to send to sales ahead of the call.

## 5. Deliver

Save the doc as a Google Doc in the client's Drive folder, in the Discovery subfolder (or the Engagement docs subfolder when that is the one the client folder has; never at the top level), unless the team asks for another format. Reply briefly: what is in it, the flags, and the sections marked "Not discussed in sales". Remind sales to share the packet at least 24 hours before the handoff call. End with one line naming what comes next: delivery reads the packet and runs `/start-motion:handoff` to draft its questions for sales; after the recorded call, `/start-motion:handoff` folds the answers in.

## 6. After the handoff call

When asked ("update the [Client] handoff from today's call"): pull the recorded call, fold sales' answers into the doc, and mark each question answered or owned with a name and a date. If the client's Claude Project exists, add the call to it as a source, numbered by date after the sales calls; if there is no project, add the call to the Discovery documents Google Doc in the client's Drive folder instead. End with one line naming what comes next: once the SC and PM accept the packet, `/start-motion:kickoff` builds the kickoff deck, and `/start-motion:discovery-plan` plans discovery from the same folder.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:handoff (v0.1.8) · handoff · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- Never invent a number, name, date or quote.
- No em dashes.
- The handoff doc is internal. It is never sent to the client.
