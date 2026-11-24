---
name: guide
description: Start Motion stage 3 (/start-motion:guide). Makes a client-facing, click-by-click walkthrough guide to one job in Salesforce for a Kicksaw client's users. A branded cover, the whole path at a glance, a reference block, numbered steps where every instruction matches a numbered marker drawn on the screenshot, what the result looks like, and good to know. One page that is also the PDF, saved in the client's Drive folder. Use whenever someone says "make a guide for [job]", "walkthrough guide for [client]", "user guide for [feature]", "training guide", "document how to [do something] in Salesforce for [client]", or "update the [job] guide".
---

# Kicksaw walkthrough guide

One request ("make the lead to opportunity guide for [Client]") ends with a guide that a client's user can follow alone, as a PDF in the client's Drive folder and a link they can open.

A guide covers one job, start to finish, for one kind of reader. It is written once the client has signed off the feature it documents, and it is the thing a user has open beside Salesforce in UAT, in training and in their first week.

Read these at the start of every run:

- `references/method.md` in this skill's folder: what a guide is for, the rules, and the bar.
- `references/example/guide.json` and `references/example/marks.json`: a small made-up guide that builds end to end. Every guide has this shape.

The guide is built by three scripts in this skill's `scripts/` folder. `mark.py` draws the numbered markers on the screenshots, `build.py` builds the page from one content file, and `build-pdf.sh` prints the page to a PDF. They need a session that can run code (Cowork or Claude Code). In a chat that cannot run code, say so in one line, write the content file and the instructions as text, and name what the person needs to finish it.

## Start: look before you ask

The client's name comes from the request. If it is missing, that is the one thing to ask before looking anywhere. Then find, without asking:

- The client's Drive folder, and any guides already in it.
- The stories behind the job in Jira, with their acceptance criteria and status. The criteria say what the user does and what the system does in return; the guide documents exactly that.
- The workflow document and the signed readout, for the client's own words for their stages, teams and records.
- The client's logo and brand colors (their website, the kickoff deck).

Report what you found in a few lines: the job, the stories it rests on and whether they are done and accepted, the guides that already exist, and anything missing.

## What to ask

Ask these together, in one message, with what you would pick for each:

1. **The job.** If the person named it, confirm it in a line. If not, propose the jobs worth a guide from the stories (the things a user does every day come first) and take their pick.
2. **The reader.** Rep, manager, service agent, the client's admin. The guide is written for that reader and captured as that reader.
3. **How the screens get captured.** One of the three ways in section 3.

If the stories behind the job are not accepted yet, say so and ask whether to go ahead: every change to a screen after the guide is written means new screenshots.

## 1. Get the sandbox ready

The screenshots are only as clean as the org. Tell the person what is needed and do the parts you can reach:

- A test user with the reader's profile and permissions. Never capture as an admin: an admin sees buttons and fields the reader does not have.
- Demo records to show, with clear "(Demo)" names and realistic values. Never a real customer's record.
- Lists and pages free of stray test records and half-filled fields.
- The guide is captured in the sandbox. Check what it shows against production before it is shared, and tell the person if the sandbox is ahead.

## 2. Walk the job once, without capturing

Do the whole job as the reader, or have the person do it while you follow. Write down:

- Every screen the reader passes through, in order.
- Every place a choice has to be made, and what the choice means in the client's business.
- Everything that was confusing, surprising or easy to get wrong.

The path becomes the "at a glance" diagram. The choices become the reference block. The confusing parts become "Before you start" and the good-to-know cards.

Show the person the outline before capturing: the steps, the screens under each, and what goes in the reference block. Capturing is the slow part, so the outline is agreed first.

## 3. Capture the screens

One screenshot per screen, all at the same window width (1483 pixels wide is what the look was tuned on), saved in the guide's `raw/` folder and numbered in order. Three ways, in order of preference:

- **Claude captures in the person's browser.** Where the session can use a browser the person is signed in to (Claude in Chrome or the built-in browser), the person signs in to the sandbox as the test user and Claude walks the job. Claude never types a password. At each screenshot, record the box of everything the reader clicks or fills in: the element's position and size from the page (`getBoundingClientRect`) multiplied by the device pixel ratio, so the numbers are in the screenshot's own pixels.
- **The person captures.** Give them the list: each screenshot, what should be on the screen, and the window width. They drop the files into the chat or the client's folder. Claude finds each control on the picture by eye, so step 4's check matters more.
- **A mix.** Claude captures what it can reach and lists the rest for the person.

A generated document (a quote PDF, a report) is captured as a picture for the result section.

## 4. Mark the screenshots

1. Write `marks.json`: for each screenshot, the boxes, numbered in the order the reader acts. Numbers continue across the screenshots of one step and start again at 1 for the next step.
2. Run `python3 scripts/mark.py <guide folder>/marks.json`.
3. Open every marked screenshot and look at it. Each number must sit on the control its instruction names. Fix and rerun until every one does.

## 5. Write the guide

Write `guide.json` in the shape of the example. `references/method.md` has the rules for the words.

- **Cover.** The client's name, the job as the headline, one sentence on what the guide covers, and two or three facts (steps, clicks, minutes).
- **At a glance.** The whole path as lanes and nodes, each node tagged with its step number, then "Before you start" with what the reader needs in hand.
- **Reference.** Anything the reader looks up while doing the job: the stages, the record types, the products, the terms. Left out when there is nothing to look up.
- **Step by step.** One step per stretch of the job. Each instruction is one action, with the exact label on the screen in bold.
- **The result.** What the finished thing looks like and where each part of it came from. Left out when the job produces no document.
- **Good to know.** How the thing behaves afterwards, and what to do when it does not go as expected.

The client's colors, logo and fonts go under `brand`. Kicksaw appears only as "Prepared by Kicksaw" on the cover and in the footer.

## 6. Build and check

1. `python3 scripts/build.py <guide folder>/guide.json`, then `bash scripts/build-pdf.sh <guide folder> "[Client] [Job] Guide.pdf"`.
2. Read the PDF page by page, as a picture:
   - No screenshot is cut across a page, and no heading sits alone at the bottom of one.
   - Every instruction's number can be found on its screenshot.
   - The cover's facts match the guide (count the steps and the clicks).
3. Check every instruction against the acceptance criteria of the stories behind it. A criterion the guide contradicts is either a mistake in the guide or a defect in the build; say which.
4. Where the session can reach the sandbox, follow the guide as the reader, doing exactly what it says and nothing else. Anywhere you had to know something the guide did not say, the guide is missing a line. Where it cannot, ask the person to do this, and say that the guide is a draft until someone has.

## 7. Save it and report

1. In the client's Drive folder, in a `Guides` subfolder (make it the first time): the PDF, and a folder of the guide's source (the content file, the marks file and the raw screenshots), so the guide can be rebuilt when the org changes.
2. Publish the page as an artifact, so there is a link to open. Claude cannot change who can open an artifact; the person opens its sharing before sending the link.
3. Report in a few lines: the links, what the guide covers, how the screens were captured, what was checked and what was not, and anything in the guide the person should read first (a place the build and the criteria disagree, a screen that looked unfinished).

The guide is never sent to the client from here. The person sends it.

## Updating a guide

"Update the [job] guide for [Client]": read the source from the Guides folder, ask what changed (or read the stories closed since the guide's date), recapture only the screens that changed, and run sections 4 to 7 again. The PDF keeps its name; the earlier one is kept with its date added.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:guide (v0.1.10) · guide · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own. "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <how the screens were captured, and anything else worth a sentence, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.
