# Kickoff deck templates

The kickoff deck is built from finished slides, not from descriptions. Every slide in `templates/kickoff/` is a complete slide file in the Slides format, shown with Tidewell Solar, a fictional client. To build a kickoff deck, copy the template for each slide and change the words, people, dates and icons. Never redraw a layout.

See every template rendered in the **Kicksaw Kickoff Deck Library** deck: https://claude.ai/artifact/EooMRC9rhebaLnRQzEBvce. Slides 1 to 14 are the standard deck (option A of every slide), 15 to 20 are the optional slides, and 21 onward are the alternates.

## How a deck is built from the templates

1. Pick the slides and the option for each one (A unless the person picked another, or the content does not fit A; see "Choosing an option" below).
2. For each slide, copy `templates/kickoff/<id>.html` into the deck as `project/slides/<id>.html`. Keep the section's id and its markup.
3. Replace the Tidewell content in place: titles, sentences, names, initials, dates, owners, speaker notes. Keep every style attribute as it is.
4. Change an icon by changing the file name in its `src` (`project/ds/kicksaw-slides/icons/<name>.png`); the names are listed below. Keep the disc colors as the template has them.
5. Repeating parts (cards, rows, sessions, people) can be added or removed within the limits in the table. Copy an existing item to add one. Past the limit, split the slide in two or switch to the option that holds more. Never shrink type to make things fit.
6. Copy the files the slides use into the deck: the brand files in `brand/` and each icon used from `icons/`.
7. Check the deck slide by slide before handing it over (the skill's design review).

## The slides

| Template | Slide | Option | Use it when | Holds |
|---|---|---|---|---|
| cover | Cover | A | Always the default: navy, chevron blades, client card | Title up to 2 lines |
| cover-b | Cover | B | The deck will be printed, or the client prefers light slides | Title up to 2 lines |
| agenda | Agenda | A | Default: navy, blue disc, numbered list with times | 4 to 7 items |
| agenda-b | Agenda | B | A white agenda drawn as a path | 4 to 6 items |
| divider | Section divider | A | Decks over 15 slides, between agenda sections | One title |
| why | Why we are here | A | Default: three numbers on navy, three problems as cards | 2 or 3 numbers, 3 problems |
| why-b | Why we are here | B | Icon rings, as in the hand-built decks; no figures needed | 3 to 5 rings |
| goals | Goals and success | A | Default: goals in the client's own words, success band | 3 or 4 goals |
| win-themes | Win themes (optional) | A | The handoff shows clear priorities to decide by; after the goals | 5 themes on an arc |
| statement | Statement | A | One client quote that frames the project, after the goals | One quote, exact words |
| team-kicksaw | Kicksaw team | A | Default: one card per person with a first-person line | 3 to 5 people |
| team-kicksaw-b | Kicksaw team | B | A table with focus and first-person line | Up to 5 people |
| team-client | Client team | A | Default: navy, people cards with role tags, role definitions | 3 to 5 people |
| team-client-b | Client team | B | Who works with whom; clients new to projects | 3 to 5 pairs |
| building | What we are building | A | Default: the lifecycle as chevrons, capabilities under each | 3 to 6 stages, 3 lines each |
| timeline | The plan | A | Default: Gantt bars on a month grid, go-live diamond | 4 to 7 phases |
| timeline-b | The plan | B | Phase band with three milestones; dates still rough | 3 to 5 phases |
| timeline-c | Discovery calendar | C | Week by week; discovery or any phase under six weeks | 2 to 6 weeks |
| how-we-work | How we work | A | Default: four-step flow and one example user story | 3 to 5 steps |
| how-we-work-b | How we work | B | A cycle; clients new to agile | 4 steps |
| terms | Salesforce terms (optional) | A | The client is new to Salesforce; after How we work | Up to 8 terms |
| screenshot | What it can look like (optional) | A | The deck library has a screenshot of the product being sold | 1 screenshot, 3 callouts |
| readback | Pre-discovery playback (optional) | A | The handoff gives a real starting picture; before Discovery sessions | 3 columns, 3 to 4 lines each |
| time | Client time commitments (optional) | A | The client is new to a project this size, or the SOW lists client responsibilities; before Discovery sessions | Up to 6 roles, 3 phases |
| discovery | Discovery sessions | A | Always in: one card per session | 4 to 8 sessions (2 rows) |
| readout-preview | Discovery playback preview (optional) | A | The client needs to know discovery ends in a sign-off; after Discovery sessions | 3 to 5 steps, 3 documents |
| communication | Staying in touch | A | Meetings, tools and who decides, on navy | 3 columns, 3 rows each |
| risks | Risks and how you can help | A | Default: rows, each with the client's ask | 3 to 5 risks |
| risks-b | Risks and how you can help | B | Cards in a 2 by 2 grid | Up to 4 risks |
| next-steps | Next steps | A | Default: three time columns with owners, next session band | 2 to 3 items a column |
| next-steps-b | Next steps | B | A dated path when the asks run past the first week | 4 or 5 steps |
| thanks | Closing | A | Default: navy, Kicksaw mark, next session | |
| thanks-b | Closing | B | White, next session panel | |

`alternates` is the divider slide of the library deck only; it never goes in a client deck.

## Swapping a layout after the deck is built

The built deck holds only the chosen slides; alternates are not carried as hidden slides. Each slide's speaker notes end with a line naming its template and the other layouts that exist, for example "Layout: timeline (A). Also: timeline-b (phase band), timeline-c (week by week)". To swap, the person asks Claude ("switch the timeline to C"); Claude copies the other template and carries the content across.

## Rules the templates already follow

- Kicksaw Brand Playbook colors only (tokens.json). Orange is the title rule plus at most one other thing per slide.
- Titles are Inter Bold 72 with the orange rule; everything else is Source Sans 3. Nothing under 24px.
- The logo is the brand file: `brand/logo-full-color.svg` on white, `brand/logo-inverse.svg` on navy, `brand/icon-mark.svg` for the mark. The topographic pattern is `brand/topo-white.png` (navy slides) and `brand/topo-navy.png` (white slides, 5% at most). The pattern files are in the Kicksaw Slides design system only; when they cannot be read, build without the pattern and say so.
- Icons sit in round discs, one meaning per icon, never as bullet decoration.
- Initials circles stand in for headshots until the deck library has them; a headshot replaces the circle at the same size.
- Presenter names go in the speaker notes. No em dashes.

## Icons

White glyphs for discs, from Font Awesome Free (icons under CC BY 4.0), in `icons/`:

address-book, arrow-right-arrow-left, arrows-rotate, arrows-split-up-and-left, award, bolt, box, building, bullhorn, bullseye, calendar-check, calendar-days, calendar-week, cart-shopping, chalkboard-user, chart-line, chart-pie, check, circle-check, circle-question, clipboard-check, clipboard-list, clock, cloud, code-branch, comment-dots, comments, compass, cubes, database, diagram-project, dna, door-open, envelope-open-text, envelope, eye, file-contract, file-import, file-invoice-dollar, file-lines, file-signature, filter, flag-checkered, flag, flask, folder-open, gauge-high, gears, globe, handshake, headset, hourglass-half, house, inbox, industry, key, layer-group, lightbulb, link, list-check, list-ol, lock, magnifying-glass-chart, magnifying-glass, map-location-dot, map, microscope, money-bill-trend-up, network-wired, pen-ruler, people-arrows, people-group, person-chalkboard, phone, plug, puzzle-piece, receipt, robot, rocket, rotate, route, scale-balanced, screwdriver-wrench, server, shield-halved, sitemap, solar-panel, star, stopwatch, sun, table-list, tags, thumbs-up, triangle-exclamation, user-check, user-gear, user-group, user-tie, users, vial, video.
