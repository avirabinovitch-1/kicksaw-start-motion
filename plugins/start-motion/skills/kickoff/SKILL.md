---
name: kickoff
description: Start Motion stage 1 (/start-motion:kickoff). Builds or updates a client-facing Kicksaw project kickoff deck as a Slides artifact by copying the finished kickoff templates and filling them from the SOW and whatever else is in the client's folder (sales calls, a handoff packet, client documents), with real headshots and screenshots from the Kicksaw deck library. Use whenever someone asks for a kickoff deck, kickoff slides, or a change to one, including a layout swap.
---

# Kicksaw kickoff deck

One request is enough: "Make the kickoff deck for [Client]." Find what you can, show the plan on one screen, build when the PM or SC says go, and fill the images from the deck library.

Every slide is copied from a finished template and only its content changes. Some slides have a standard layout (A) and an alternate (B). The standard deck, with every optional slide and alternate, is the Kicksaw Kickoff Deck Library, shown for Tidewell Solar, a fictional client: https://claude.ai/artifact/EooMRC9rhebaLnRQzEBvce

Where the templates live: this skill's folder carries `templates/kickoff/` (every slide as a finished file), `templates/kickoff-manifest.json`, `icons/` (the white glyphs), `brand/` (the logo files and the icon mark), `references/kickoff-templates.md` (how a deck is built from the templates, when to use each one, its limits, the swap rule and the icon list), and `tokens.json` and `design-system.json` (the Kicksaw Slides design system's tokens). The Kicksaw Slides design system (https://claude.ai/artifact/Dz63JoG9fN8CMu86q1sB7a) holds the master copy; the plugin's files are what you build from. The topographic pattern files (`brand/topo-white.png`, `brand/topo-navy.png`) are in the design system only; when they cannot be read, build without the pattern and say so in the report. If the templates cannot be opened at all, say so and stop before building: a deck drawn without the templates is not the standard.

## 0. Start: where the client stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the signed SOW (found, and its date); what else is in the client's folder beyond the SOW (transcripts, a handoff doc, client documents, in one clause; nothing beyond the SOW is not a gap, it is the normal case); the Kicksaw team (who is named, and where); the client team (sponsor, champion, SMEs named or not); the discovery plan (built, with how many sessions, or not yet); the phase plan (go-live and break weeks firm or not); images (client logo in the folder or not; headshots from the deck library); the kickoff date (set or not); and whether a kickoff deck already exists for this client (then the request is a change to it, section 1). For example: "Tog. Signed SOW: found (Oct 3). Beyond the SOW: three transcripts, no handoff doc. Kicksaw team: four people named in the SOW. Client team: sponsor and champion named; no SMEs yet. Discovery plan: built, nine sessions. Phase plan: go-live in the SOW, break weeks not set. Images: client logo in the Drive folder. Kickoff date: not set. No kickoff deck yet."

If no discovery plan exists, say that the Discovery sessions slide (the one slide that is never dropped) will carry placeholders, and offer to run `/start-motion:discovery-plan` first. If nothing at all turns up for the client (no Drive folder, no SOW), offer `/start-motion:new-client` first: it sets the client up and names the stage to run next.

## What to ask: propose the deck, then let the person pick

When no slide list was given, look first (section 0 and section 1), then propose the deck and let the person answer once. Every core slide is in. Of the optional slides, propose the ones whose reason holds for this client (section 3), each with a one-line reason drawn from the sources ("the phase plan is firm, with go-live the week of Apr 12, 2027"). The person has the final say. Every slide starts on its standard layout (A); layouts can be changed in the picker or after the deck is built (section 9). Don't ask who presents each slide: the owners go in the plan and the speaker notes.

**In Claude chat, when you can show an interactive visual,** show the slide picker: `references/slide-picker.html`. Change only the `CFG` line at the top of its script: `client` (the client's name), `date` (the kickoff date, for example "Monday Nov 16"), and `add` (the optional slides you propose, keyed by their ids in the script's slide list, each with its reason). Send everything else as it is. The picker shows a picture of every slide, ticks the core slides and your proposals, lets the person switch layouts and open any picture full size, and sends the picks back in the picked-list format (section 1). Write one line above it, for example "Here's the deck I'd build for Harborlight. I added Timeline and Client time commitments; change anything, then press Build this deck."

**Everywhere else** (Cowork, Claude Code, Codex, or a chat that can't show visuals), send this, filled in for the client:

```
Here's the kickoff deck I'd build for [Client], Monday [date]: the 13 standard slides plus [n] optional ones.

Adding:
- [Optional slide]: [reason from the sources, one line]

Also available, if any of these fit:
- A client quote: the sponsor's own words from a sales call
- Win themes: the priorities to decide trade-offs by
- What it can look like: product screenshots
- Timeline: phases and the go-live date
- Week by week calendar: the first weeks, day by day
- Salesforce terms in plain language
- Client time commitments by role
- Pre-discovery playback: what we've already heard
- Discovery playback preview: what the readout will look like

Every slide starts on its standard layout. You can switch any of them once you see the deck, or look through the options first in the Kicksaw Kickoff Deck Library: https://claude.ai/artifact/EooMRC9rhebaLnRQzEBvce

Want to add or drop anything? And who opens the call, and how long is it?
```

Leave out of "Also available" the slides already under "Adding". If the kickoff date isn't set, ask for it in the same message (it should be a Monday).

Read the answer back in one line ("Harborlight kickoff, Monday Nov 16. 15 slides: the core 13 plus Timeline and Client time commitments, Title in B. Plan next."), then show the plan (section 2) and build on a yes. Two stops, picks then plan, the same as the page.

## 1. Start from whatever was given

Any of these is a valid start. Combine them when more than one is given.
- **Only a client name.** Look up the signed SOW first, then everything else in the client's Drive folder, every subfolder included (sales call transcripts, a handoff packet if sales shared one, client documents; subfolder names vary by client), the Notion Closed Won task, and the client's Claude Project. The SOW is enough to build from. Then propose the deck as in "What to ask" above.
- **The SOW,** attached or linked, with or without anything else from the folder.
- **An outline:** one numbered line per slide, presenter in brackets, tables as rows. Build it as written, choosing the template that fits each line.
- **A picked slide list,** usually the prompt from the slide picker on the Start Motion page: numbered slides with an owner role in brackets ([PM], [SC], [All]), sometimes a layout ("3. Why we're here · layout B (icon rings) [SC]"), sometimes core slides left out on purpose, and notes. No layout means A. Build exactly those slides in exactly that order with exactly those layouts. Don't add or drop slides by the rules in section 3; if a pick looks wrong for this client (a timeline with no dates, "What it can look like" with no screenshots in the library), say so in the plan and let the person decide. Draft the content from the sources.
- **An existing kickoff deck to change.** Read it by its URL, change only what was asked, keep its layouts. Never rebuild it. A layout swap follows section 9.

Don't ask for anything you can look up.

## 2. Show the plan before building

Reply with one short plan and wait for a yes:
- The slides in order: template and layout, presenter, where the content comes from, and the image each slide will use. Turn each owner role into the person who holds it on this project (from the SOW, the handoff packet when there is one, or the team named in the request); keep the role and list it as missing when no one is named.
- When the content will not fit the chosen layout (more people, phases, risks or sessions than it holds; the limits are in `references/kickoff-templates.md`), say so and propose the layout that holds it, or splitting the slide.
- When no slide list was given: the optional slides you added or left out, each with its reason (rules in section 3).
- What is missing: placeholders, people with no headshot, the client logo.
- The kickoff date. It should be a Monday; say so if it isn't.

The picks are already given, so the plan is the last stop: ask a question in it only when a pick does not fit this client or a source leaves a gap that changes the deck, and at most three. If the person says "just build it", build with your best reading and list the guesses in the reply.

## 3. The slide set

Core slides, always in unless the person removes them, with their templates:
1. Title: `cover` (A, navy with blades) or `cover-b` (B, white with the mark)
2. Agenda: `agenda` (A, navy list) or `agenda-b` (B, white path)
3. Why we're here: `why` (A, numbers and problems) or `why-b` (B, icon rings)
4. Goals and success: `goals`
5. Meet the Kicksaw team: `team-kicksaw` (A, cards) or `team-kicksaw-b` (B, table)
6. Meet the client team: `team-client` (A, navy cards) or `team-client-b` (B, who works with whom)
7. What we're building (this phase vs future phase): `building`
8. How we work (user stories, acceptance criteria, sprints with demos, standard features first, one example user story in the client's terms): `how-we-work` (A, flow and story) or `how-we-work-b` (B, cycle)
9. Discovery sessions (session, focus, agenda, who attends): `discovery`. Critical; never drop it.
10. Communication and tools: `communication`
11. Risks and how the client can help: `risks` (A, rows) or `risks-b` (B, cards)
12. Next steps (action and owner): `next-steps` (A, by date) or `next-steps-b` (B, path)
13. Questions and thank you: `thanks` (A, navy) or `thanks-b` (B, white)

Optional slides. When no slide list was given, add one when its reason holds or the person asks for it, in the place shown:
- **A client quote** (after 4): `statement`. A sponsor's own words from the sales calls frame the project. Never paraphrase it into a quote.
- **Win themes** (after 4): `win-themes`. The handoff shows clear priorities or trade-offs to decide by.
- **What it can look like** (after 7): `screenshot`. The deck library has screenshots of the product being implemented.
- **Timeline** (after 7): `timeline` (A, Gantt) or `timeline-b` (B, phase band). The SOW or the PM gives phase and go-live dates. Tentative dates make it a "Draft timeline". No dates, no slide.
- **Week by week calendar** (after the timeline): `timeline-c`. The first weeks are actually scheduled.
- **Salesforce terms in plain language** (after 8): `terms`. The client is new to Salesforce.
- **Client time commitments by role** (before 9): `time`. The client is new to a project this size, or the SOW lists client responsibilities.
- **Pre-discovery playback** (before 9): `readback`. The sales calls and anything else in the folder give enough real understanding to play back what we reviewed, what is still needed and our current read.
- **Discovery playback preview** (after 9): `readout-preview`. The person asks for it, or the client needs to know discovery ends in a playback they confirm.
- **Section dividers**: `divider`, only in decks over 15 slides.

## 4. Content

- Draft every slide from the sources in section 1. Never invent a figure, name, date, quote or commitment; use a bracketed placeholder like [Title] instead and list it.
- Why we're here and Goals and success use the client's own words from the sales calls and the handoff packet. Without them, use the SOW's stated objectives and any client documents, and say in the speaker notes that the PM confirms them with the client at kickoff.
- What we're building matches the SOW. Don't walk back sales promises on the kickoff deck; they are explored in discovery.
- Kicksaw team: name, role, focus, and one first-person line on how the client will work with that person.
- Client team: name the business sponsor, the project champion and the subject matter experts.
- Discovery sessions start with a reverse demo of the client's core processes and systems; the workflow deep dives follow from it, and discovery closes with a playback.
- Week by week calendar: the kickoff Monday is the first day; discovery and refinement sessions are on Tuesdays and Thursdays; sprints start on Wednesdays; the last refinement session of each sprint is a demo ("Sprint N demo"); break weeks and multi-day phases (UAT, production migration and training) are single bars; hypercare is a one-line note. If the schedule doesn't fit cleanly, explain the options in plain language and ask which to use before building.
- Next steps: what the client brings to week 1 (access, data samples, attendees), each with an owner.
- Audience is non-technical client leadership and staff: plain language, sentence-case headings, curly quotes and apostrophes, no em dashes.
- Presenter names go in the speaker notes, never on the slide. The agenda slide shows topics only.
- The EM/DM opens the call and sales introduces the team; say so in the Title and Agenda speaker notes. On Communication and tools, show the executive checkpoint and the weekly playback with the client lead.

## 5. Build from the templates

1. Build from the Slides artifact type, not a .pptx, unless a file format is named. Create the deck and apply the tokens in this skill's `tokens.json` (the Kicksaw Slides design system's tokens) the way the Slides type's instructions say; if the design system artifact itself can be opened, applying it is the same thing. Read `references/kickoff-templates.md` before writing anything.
2. For each slide in the plan, copy `templates/kickoff/<template>.html` into the deck as `project/slides/<id>.html`. Keep its markup and every style; change only text, names, initials, dates, owners, speaker notes and icon file names.
3. Repeating items (cards, rows, sessions, people, phases) are added by copying an existing item or removed whole, within the template's limits. Past a limit, split the slide or switch to the layout that holds more. Never shrink text, never change sizes, colors or spacing.
4. Icons: choose from the list in `references/kickoff-templates.md`, one meaning per icon, by changing the file name. Upload every icon and brand file the slides use.
5. The client card on the title slide holds the client logo when there is one (section 6); otherwise it holds the client name. Headshots replace the initials circles at the same size.
6. Footer on every slide: "<Client> × Kicksaw · Project kickoff" and the slide number.
7. Only the chosen slides go in the deck; alternates are never added as hidden slides. End each slide's speaker notes with one line naming its layout and the others that exist, for example "Layout: timeline (A, Gantt). Also: timeline-b (B, phase band)."

## 6. Images: the Kicksaw deck library

The deck library is one Google Drive folder, "Kicksaw Deck Library", with subfolders for headshots, screenshots and client logos, and an index sheet, "Deck library index". Each image has one row: File, Type (headshot, screenshot, logo, photo), Person or subject, Role or product, Use on (slide names), Tags, OK for clients (yes or no), Updated.

- Read the index through the Google Drive or Sheets connector before planning. Find images through the index, never by file name: headshot files are numbered.
- **Headshots:** match each Kicksaw team member by name. Anyone without a row keeps the initials circle and goes on the missing list.
- **Screenshots:** use one when its "Use on" or tags match the slide and the product being implemented. For example, the Jira board on How we work; Slack and tl;dv on Communication and tools; the product sold on What we're building or What it can look like. One screenshot per slide at most, with a one-line caption. None on the title, agenda or team slides.
- Only use rows marked "OK for clients: yes". A screenshot that shows another client's data never goes in a deck.
- Download each file through the connector and add it to the deck the way the Slides type's instructions say. Never link to a Drive URL from a slide.
- **Client logo and client photos:** from what was attached, the client's Drive folder, or the library's client logos folder, in that order. Never from the web.
- If the library or its index can't be opened, say so, keep the initials circles and image placeholders, and keep building.
- When someone attaches a new headshot or screenshot during a build, offer to add it to the library with an index row.

## 7. Review before handover

Look at every slide once it is built:
- No text shrank to fit. A slide whose content is taller than its space is split, or moved to the layout that holds more.
- The frame is intact on every content slide: logo, title, orange rule and footer in the same place.
- Nothing invented: every placeholder is bracketed and listed.
- Orange is the title rule plus at most one thing per slide (go-live, or what needs attention).

Fix what fails, then hand over.

## 8. Finish

- Put each assumption in the speaker notes of the slide it affects.
- Reply briefly: what was built, each slide's layout, where the content came from, the placeholders still to fill, the people and logos with no image, and the assumptions. Remind the person to use the Share menu before sending the deck to the client, and that any layout can be swapped by asking ("switch the timeline to B").
- End with one line naming what comes next: the day before the reverse demo, `/start-motion:discovery-plan` preps it ("prep me for [Client] D1"); if the discovery documents are not set up yet, `/start-motion:discovery-call` sets them up from the SOW.

## 9. Layout swaps

When asked to swap a layout ("switch the timeline to B", "use the white cover"): copy the other template over that slide, carry its content across, keep the slide's position, update the layout line in the notes, review that slide by section 7, and say what moved or did not fit. Change nothing else in the deck.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:kickoff (v0.1.2) · kickoff · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.
