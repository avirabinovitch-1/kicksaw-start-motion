# Refinement deck slides

The refinement deck is built from finished slides, not from descriptions. Every slide in `templates/refinement/` is a complete slide file in the Slides format, shown with Tidewell Solar, a fictional client. To build a deck, copy the slide for each part and change the words. Never redraw a layout.

The slides share one stylesheet, `templates/refinement/deck.css`. It goes into the deck as `project/deck.css`, unchanged.

## The order of a deck

1. `cover`
2. `today`
3. For each story, in the order the SC confirmed:
   - the story with its open questions: `story`, `story-one` or `story-short`
   - a detail slide for a question that needs one: `detail-groups`, `detail-timeline` or `detail-table`
   - `criteria`, unless the story used `story-short`
4. `landed`

A story with no open questions uses `criteria` alone, with the story sentence in the speaker notes: it is there to be read and approved.

## The slides

| Slide file | What it is | Use it when | Holds |
|---|---|---|---|
| cover | Title | Always first | Client, session, date, the sprint's dates |
| today | Today's stories | Always second | 2 to 6 stories, each with what needs settling and its question count. Past six, a second slide |
| story | A story and its open questions | The story has two questions | The story sentence and two question cards, each with what we know and our proposal |
| story-one | A story and one open question | The story has one question | The story sentence and one question, the proposal beside it |
| story-short | Story, criteria and questions on one slide | Up to four criteria of two lines each and up to three questions with a one-line proposal | Left: the criteria. Right: the questions |
| criteria | Acceptance criteria to confirm | Every story that did not use story-short | Up to nine criteria. Past nine, a second slide |
| detail-groups | A question about how things are grouped | Sources into queues, roles into profiles, record types into teams | 3 to 5 columns of up to four lines, one sentence, one client quote, up to three numbers |
| detail-timeline | A question about a rule over time | Due dates, reminders, escalations | Two rows of up to eight days, a worked example |
| detail-table | A question about who can do what, or what happens when | Permissions, matching rules, routing by case | Up to ten rows and five columns |
| landed | Where we landed | Always last | Up to seven questions. Past seven, a second slide |

A story with three or more questions that does not fit `story-short` uses `story` twice: two questions on the first, the rest on the second, with "(continued)" after the eyebrow.

## Rules the slides already follow

- Kicksaw Brand Playbook colors only. Orange is the title rule and nothing else on these slides.
- Titles are Inter Bold with the orange rule; everything else is Source Sans 3. Nothing under 24px.
- The logo is the brand file: `brand/logo-full-color.svg` on white, `brand/logo-inverse.svg` on navy. The topographic pattern on the cover comes from the Kicksaw Slides design system; when it cannot be read, build the cover without it and say so.
- The footer reads "<Client> × Kicksaw · <Sprint or session> refinement" with the slide number.
- A story's title, sentence and criteria are the words in Jira. A question, what we know and the proposal are written for the client in plain language.
- A criterion a question could change carries that question's number on the right.
- Speaker notes on every slide say what to ask and in what order. Remove the template's "Layout:" guidance and write notes for this client; keep one last line naming the layout, as the template does.
- No em dashes.

## Fitting the words

- Never shrink type. When the words do not fit, use the slide that holds more, or split.
- A story title of more than two lines at this size is shortened on the slide only when the SC agrees; the Jira title stays as it is.
- "What we know" is two or three lines. A longer history goes in the speaker notes.
- A proposal is one or two sentences. If it needs more, the question needs a detail slide.
