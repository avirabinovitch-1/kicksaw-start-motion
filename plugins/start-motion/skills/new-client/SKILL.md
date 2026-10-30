---
name: new-client
description: Start Motion setup (/start-motion:new-client). Sets a new Kicksaw client up for the delivery kit before the first stage runs. Finds the signed SOW and whatever sales shared, finds or makes the client's Google Drive folder and its Discovery subfolder, checks that the person is working in a Claude Project for the client and that the connectors the stages read are connected, offers to set up the discovery documents, and names the first stage command to run. Use whenever someone says "set up [client]", "new client [client]", "we just signed [client], where do I start", or runs a stage command for a client that has nothing set up yet.
---

# Kicksaw new client setup

One request ("set up Tog") gets a new client ready for the stage commands. It runs once per client, takes a few minutes, and ends by naming the first stage to run. Every stage command can also do this setup on its own when it finds nothing for the client; this command is the way to do it on purpose, before the first stage.

## Start: what already exists

Read `references/method.md` in this skill's folder at the start of every run: what the setup is for, the checks, and the link to the Start here page on the Start Motion page.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then look for each of these and report what you found in a few lines, before doing anything else:

1. **The signed SOW.** Search Google Drive for the client's name and "SOW" or "Statement of Work"; also the person's Claude Project files if you are in one, and the Notion Closed Won task if Notion is connected. Take the latest signed edition, not a redline or a draft. The SOW is the one thing every stage needs.
2. **Whatever sales shared.** Everything else in the client's Drive folder and in tl;dv for this client: call transcripts and recordings, an IKT or handoff doc, the contracts (MSA, order form, BAA, NDAs), client documents. List what is there and what is not. Delivery gets the SOW plus whatever was shared with it; this skill does not expect a sales calls folder, a handoff doc or any transcript, and it does not ask anyone in sales for anything.
3. **The client's Drive folder.** A folder named for the client in Google Drive, and inside it a Discovery subfolder (or Engagement docs, when that is the subfolder the client folder uses). The outputs the stages save for the whole team go there: the requirements list, the Discovery documents note, every session note and the readout sign-off record.
4. **The Claude Project.** Whether this conversation is inside a Claude Project named for the client (a Project tool is available and its name is the client's). The stage commands keep their working files in the client's Project and read them back on every run, so one Project per client is strongly recommended. It is not required: the kit also runs outside a Project, and in Codex, with the Drive copies as the shared record.
5. **The connectors.** Which of these the person has connected, judged by the tools available in this conversation: Google Drive (the client folder, the templates and the requirements list), Gmail and Slack (what the client and the team said between calls), tl;dv (call transcripts), Jira (user stories), Notion (the Closed Won task). Name the missing ones; do not stop for them.

For example: "Tog. SOW: found, signed Oct 3, in Tog / 00 Contracts. Shared by sales: three call transcripts in tl;dv, the order form, no handoff doc. Drive folder: Tog, with no Discovery subfolder yet. Claude Project: this conversation is in a Project named Tog. Connectors: Drive, Gmail, Slack and tl;dv connected; Jira not connected."

## What to ask: one message

Ask once, in one message, and only for what the Start did not find:

- The SOW, if no signed edition turned up anywhere: a link or the file. Nothing starts without it.
- Where the client's Drive folder should go, if no folder named for the client exists: the parent folder that holds Kicksaw's client folders. Never guess a parent folder. If one exists, say which one you will use and carry on.
- Whether to set up the discovery documents now (the four documents and the Discovery documents note, built from the SOW by `/start-motion:discovery-call`) or leave that for the first stage that needs them.

Then read back what you heard in one line and run: "Setting up Tog: SOW from 00 Contracts, Discovery subfolder in the Tog folder, discovery documents now."

## 1. The Drive folder

Make what is missing, through the Google Drive connector, and say what you made:

- The client's folder, named for the client, in the parent folder the person named. Never at the top level of someone's My Drive without being told to.
- A Discovery subfolder inside it. Leave an existing Engagement docs subfolder as the one the client uses, when that is what the folder already has; make nothing new beside it.
- If the SOW came as a file or a link outside the folder, save a copy into the client folder (a Contracts subfolder when one exists, otherwise the client folder itself) so every stage finds it in one place. Never move or edit the original.

Nothing else is created here. The requirements list and the three discovery pages are made by `/start-motion:discovery-call`; the handoff doc by `/start-motion:handoff`; the kickoff deck by `/start-motion:kickoff`.

## 2. The Claude Project

Claude cannot make a Project for the person; say what to do instead, in plain steps, only when the conversation is not already inside the client's Project:

1. In Claude, make a new Project named for the client (the client's name alone, as it appears on the SOW).
2. Add the signed SOW to the Project's files, and anything sales shared that is a document (the handoff doc, the contracts). Call transcripts stay in tl;dv; the stages read them from there.
3. Run every stage command inside that Project. The working files the stages keep (the Discovery documents note, the session notes, the readout content) live there and are read back on every run.

If the person says they will not use a Project (Codex, or a shared account), say that the kit still runs: every stage reads the Drive copies when there is no project copy, and the outputs the team needs are always in the Drive folder.

## 3. The discovery documents

If the person said yes to setting them up now, hand over to `/start-motion:discovery-call`'s setup ("set up the discovery documents for [Client]") and let it run as that skill describes: it copies the requirements list into the Discovery subfolder, makes the three pages from the templates in the plugin, writes the Discovery documents note into the Project and as a Google Doc in the Discovery subfolder, and asks the SC only for what none of the inputs say. Do not rebuild any of that here, and never make a second note.

If the person said later, say which command will do it when it is needed (`/start-motion:discovery-call`, or `/start-motion:discovery-plan`, which offers it first because the plan seeds the requirements list's tabs).

## 4. Report back

A few short lines: what exists now and where (the folder and subfolder with links, the SOW, what sales shared), what was made, what is still missing and never blocks (a handoff doc, transcripts, a connector), and the Project instructions if they were needed.

End with one line naming what comes next, picked from what exists:

- Sales shared a packet (calls, contracts, a handoff doc): `/start-motion:handoff` drafts delivery's questions for the handoff call.
- Only the SOW: `/start-motion:discovery-plan` plans discovery from it before kickoff, then `/start-motion:kickoff` builds the deck.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:new-client (v0.1.0) · setup · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to the client's Drive folder>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- No em dashes anywhere.
- The signed SOW is the only required input. Transcripts, the handoff doc and client documents make the work more specific; nothing stops without them, and nobody in sales is asked for anything by this skill.
- Make folders only where the person said; never guess a parent folder, never move or edit an original file.
- One Discovery documents note per client, written by the discovery call setup; this skill never writes its own.
- Say plainly what Claude cannot do for the person (make a Claude Project, connect a connector) and give the steps instead.
