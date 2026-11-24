# Walkthrough guides: the method in short

The full method, with the example and the bar, is on the Start Motion page under Walkthrough guides: https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S#guides

## What the stage is for

A new system fails on the first morning a user cannot work out what to click. The guide is what that user has open beside Salesforce: one job, start to finish, with every click shown on a picture of their own screen. It is used in UAT, in training and in the first weeks after go-live.

## Why it is more than a screen recording

- It starts with the whole path and the order that matters, before any clicks.
- It explains what the reader is choosing at each point, not only where to click.
- Several clicks share one screenshot, each numbered to its instruction, so the reader keeps their place.
- It ends with what the result looks like and where each part of it comes from.
- It carries the client's branding and prints cleanly.

## The calls the consultant makes

- **Which jobs get a guide.** The jobs a user does every day, and the ones that are easy to get wrong. Not every feature.
- **Who the reader is.** One kind of reader per guide.
- **When.** After the client has accepted the stories behind the job, in time for UAT or training.
- **What to leave out.** Anything the reader does not need to finish the job.

## Rules

- One job per guide. If a guide covers two jobs, split it.
- Written and captured as the reader, never as an admin.
- Client-ready wording only: no story keys, no internal notes, no record links.
- The client's branding leads. Kicksaw appears only as "Prepared by Kicksaw".
- The overview is a real diagram, not a list.
- Screens show demo records, and the guide says so.
- The guide matches production before it is shared.
- The source is kept in the client's Drive folder, so the guide can be rebuilt when the org changes.

## Rules for the words

- One action per instruction. "Click **Save**." Not "Fill in the fields and save."
- The exact label on the screen, in bold, spelled as it is spelled there.
- The client's own words for their stages, products and teams.
- Say what a choice means in their business, not what it does in Salesforce.
- No Salesforce terms the reader does not see on their screen.
- A tip goes between the instruction and its screenshot, at most one per screenshot.
- Sentence case, no em dashes.

## The bar: a guide is ready when

- Someone who has never seen the org can finish the job from it without asking anyone
- Every instruction's number is on the control it names
- Every instruction agrees with the acceptance criteria of the stories behind it
- The path diagram shows the whole job on one screen
- Every choice the reader makes is explained in the client's own terms
- No screenshot shows a real customer's record, an admin-only button or a stray test record
- The PDF has no screenshot cut across a page
- The source is in the client's Guides folder
