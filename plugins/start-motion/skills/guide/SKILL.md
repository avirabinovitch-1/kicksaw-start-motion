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

## Two things a run cannot go without

- **The sandbox, in a browser.** Claude walks the job itself, in a browser the person is signed in to (Claude in Chrome or the built-in browser), as the test user. This is how it learns the click path, so there is no version of this command that works from screenshots someone else took. Check for the browser before anything else. If the session has none, or the sandbox will not open in it, stop and say so in one line, with what the person has to do (open the session where the browser is, sign in to the sandbox as the test user). Do not go on to an outline.
- **A path it has seen, not one it has guessed.** The stories say what the job must do. They do not say where the buttons are. Every click in the guide is one Claude made in the sandbox, or one the person told it. Where it does not know, it asks (see "When you do not know").

## Start: look before you ask

The client's name comes from the request. If it is missing, that is the one thing to ask before looking anywhere. Then find, without asking:

- The client's Drive folder, and any guides already in it.
- The stories behind the job in Jira, with their acceptance criteria and status. The criteria say what the user does and what the system does in return; the guide documents exactly that.
- The workflow document and the signed readout, for the client's own words for their stages, teams and records.
- The solution design, for how the job was built: which objects, which buttons, flows and screens. This is the best written source for the path.
- A recording of the job being shown (a demo or a UAT session in tl;dv). Someone clicking through it on a call is the path, said out loud.
- The client's logo and brand colors (their website, the kickoff deck).

Report what you found in a few lines: the job, the stories it rests on and whether they are done and accepted, the guides that already exist, and anything missing. Say plainly how much you know about the path: "the design names the button and the flow", "a demo on Nov 12 walks it", or "nothing I found says how a user gets from the lead to the quote".

## What to ask

Ask these together, in one message, with what you would pick for each:

1. **The job.** If the person named it, confirm it in a line. If not, propose the jobs worth a guide from the stories (the things a user does every day come first) and take their pick.
2. **The reader.** Rep, manager, service agent, the client's admin. The guide is written for that reader and captured as that reader.
3. **The path.** Give the path as you understand it, in one or two lines (where the reader starts, the main clicks, where it ends), and ask the person to correct it. Where you found nothing, ask for it: where the reader starts (the app, the tab, the record), and anything on the way that is not standard Salesforce (a custom button, a screen flow, a step in another tool). One or two lines from the person is enough; the walk fills in the rest.
4. **The test user and the demo record.** Which user to sign in as, and which record to run the job on, if they already exist.

If the stories behind the job are not accepted yet, say so and ask whether to go ahead: every change to a screen after the guide is written means new screenshots.

## 1. Get the sandbox ready

The screenshots are only as clean as the org. Tell the person what is needed and do the parts you can reach:

- A test user with the reader's profile and permissions. Never capture as an admin: an admin sees buttons and fields the reader does not have.
- Demo records to show, with clear "(Demo)" names and realistic values. Never a real customer's record.
- Lists and pages free of stray test records and half-filled fields.
- The guide is captured in the sandbox. Check what it shows against production before it is shared, and tell the person if the sandbox is ahead.

## 2. Read the org, then walk the job once without capturing

**Read the org first.** Before the walk, for each object the stories touch, find what a user can do there: the buttons and actions on the page, the screen flows they start, any custom components, the record types, the required fields and the validation rules that can stop a save. Use the Salesforce CLI or a Salesforce connector where the session has one; the solution design is the second source. The standard parts of the path you already know. This step is for the parts you do not: it tells you where the custom steps start and what they are called on the screen. If the session cannot read the org this way, say so in one line and lean on the design and the person's lines instead.

**Then walk it.** Do the whole job as the reader, in the sandbox, with the person's lines and the org reading in hand. Write down:

- Every screen the reader passes through, in order.
- Every place a choice has to be made, and what the choice means in the client's business.
- Everything that was confusing, surprising or easy to get wrong.

The path becomes the "at a glance" diagram. The choices become the reference block. The confusing parts become "Before you start" and the good-to-know cards.

Show the person the outline before capturing: the steps, the screens under each, and what goes in the reference block. Mark each step with how you know it: walked it, read it in the design, or told by the person. Capturing is the slow part, so the outline is agreed first.

### When you do not know

Stop and ask. Never fill a gap with the likely answer. These are the moments:

- **Two ways to do the same thing.** A button and a quick action, the related list and the path component. Ask which one the client's users were shown.
- **A step you cannot find.** The criteria say the user does something and the screen offers no way to do it as this user. It is a missing permission, an unfinished build or a path you have not found. Say which you think it is.
- **The screen and the criteria disagree.** Say what each one says. The person decides whether the guide follows the build or the build gets fixed first.
- **A choice whose meaning you do not know.** A picklist or a record type with no explanation in the documents. Ask what it means in the client's business; do not write a definition from the label.
- **A step outside the browser.** A phone call, an email that arrives, a file from someone's computer, another system. Ask the person to describe it or send a picture.
- **An error or a blank page on the way.** Stop there. Do not try other routes in a client's org to get around it.

Ask everything from one walk together, in one message. For each: what you saw, the options, and the one you would pick. Keep walking past a question only when the rest of the path does not depend on the answer.

## 3. Capture the screens

One screenshot per screen, all at the same window width (1483 pixels wide is what the look was tuned on), saved in the guide's `raw/` folder and numbered in order.

Claude captures, in the same browser and as the same test user as the walk. The person signs in; Claude never types a password. At each screenshot, record the box of everything the reader clicks or fills in: the element's position and size from the page (`getBoundingClientRect`) multiplied by the device pixel ratio, so the numbers are in the screenshot's own pixels.

The person sends a picture only for a screen Claude cannot reach at all: a step in another system, a screen behind a second sign-in, an email as it arrives. Name each one and what should be on it. Those markers are placed by eye, so step 4's check matters more for them, and the report lists them.

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
4. Follow the guide in the sandbox as the reader, doing exactly what it says and nothing else. Anywhere you had to know something the guide did not say, the guide is missing a line.

## 7. Save it and report

1. In the client's Drive folder, in a `Guides` subfolder (make it the first time): the PDF, and a folder of the guide's source (the content file, the marks file and the raw screenshots), so the guide can be rebuilt when the org changes.
2. Publish the page as an artifact, so there is a link to open. Claude cannot change who can open an artifact; the person opens its sharing before sending the link.
3. Report in a few lines: the links, what the guide covers, what was checked and what was not, and anything in the guide the person should read first (a place the build and the criteria disagree, a screen that looked unfinished, a step that rests on what the person told you and not on what you walked, a picture the person sent).

The guide is never sent to the client from here. The person sends it.

## What it cannot do, and what helps

Tell the person these when they ask, and the ones that apply whenever a run hits one.

What it cannot do:

- **Sign in.** The person signs in to the sandbox as the test user. Claude never types a password or a verification code.
- **See what the test user cannot.** If the reader's profile is missing a button, the guide will not have it, and Claude cannot tell a missing permission from a missing build without reading the org.
- **Know which route the client was taught.** Where two routes work, only the person knows which one was shown in training.
- **Know why.** It can read what a choice does. What it means in the client's business comes from the documents or the person.
- **Leave the browser tab.** Phone calls, email as it arrives, files on a computer, desktop apps, a second system with its own sign-in.
- **Capture a generated document live.** A quote PDF or a report goes in as a picture.
- **Promise production matches.** It is captured in the sandbox. If the sandbox is ahead, the guide is ahead too.
- **See through Lightning's cache.** After a deploy, an old page can still show. Reload before capturing.

What makes a run faster and the guide better, in the order it helps:

1. One or two lines on the path: where the reader starts, the main clicks, where it ends.
2. The name of anything custom on the way: the button, the flow, the component.
3. A recording where someone walks the job (a demo, a UAT session).
4. The solution design in the client's folder.
5. A test user with the reader's profile and a clean demo record, ready before the run.
6. What users get wrong, or what was asked most in UAT. This becomes "Before you start" and the good-to-know cards.

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
Notes: <what you had to ask about the path, any screen the person sent as a picture, and anything else worth a sentence, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.
