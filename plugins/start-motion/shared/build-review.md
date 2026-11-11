# The design and build review page

One page per client build, for the SA. The SA is accountable for every component that goes into the org and for the architecture holding together, so this page puts in one place what is being created or changed, why, and where it stands. It is modeled on Ben Bolding's Fred Hutch epic designs in Notion (Stories this design serves, Where the design differs from the stories, Rules that shape the design, Today and after, the objects, the flow, Fields, objects and settings, Who can do what, Automation, The build, Open questions, Verification items, Not built, Sources, Change log), with diagrams added and the component list read from the repo.

The home of this text is `plugins/start-motion/shared/build-review.md`; skills carry copies, written by `scripts/sync-agents.py`.

## How it looks

A plain document in the style of Ben's Notion designs: a small Kicksaw logo, the title, one meta line, a short summary, and a one-line status (how many components are merged, built, planned and waiting, and how many items are open for the SA). Then What this build does, in plain words: what the build accomplishes, what each kind of user can do once it is live, and what is not in it. Then sections in his order: Open for the SA (only while anything is open), Stories this design serves, Where the design differs from the stories, Decisions that shape the design, Today and after, Data model, Across the whole solution, How it works, Automation, Pages, Who can do what, Reporting, Fields, objects and settings, Changes to what is already in the org, The build, Open questions, Verification items, Not built, Sources, Change log. Light tables, plain text for status, color only for what is waiting or was found. Two diagrams, both muted: the data model (each object with its new and changed fields and types, each relationship drawn from its field to the parent) and one per flow.

## It follows the decisions

The page is rebuilt every time a decision is made, so it never shows a decision differently from the Decisions tab:
- Proposed rows are listed under Open for the SA (SA calls as Decide, recommendations as Confirm, client calls as With the client), with their options and Claude's recommendation.
- Decided rows are the numbered list under Decisions that shape the design: what was chosen, why, what else was considered, who decided and when, with the row's ID.
- When the SA answers in the picker, update `content.json` before rebuilding: move the row to Decided with the chosen wording; change every story, planned component and task text that said it waited on that decision; drop the components of options that were not chosen; then republish to the same link.
- Once nothing is Proposed and nothing else is waiting, Open for the SA disappears and the status line says so. The page then reads as the finished design, with every decision and its reason in place.

## When it is made and updated

- `/start-motion:build-plan` makes it when the plan is drafted, before the SA approves: everything is Planned or Waits. The SA reviews the plan from this page.
- `/start-motion:build` updates it after every task that reaches a pull request, after every merge it catches up on, and after an undo: components move to Built and Merged, and their details are read from the metadata files.
- `/start-motion:design` links to it once a plan exists.
- Its link goes in the build plan's header, the decision picker (`review`), every pull request's "Check before you merge", and the story's evidence note in Jira.

## How it is made

1. Write `content.json` (below) from the design, the build plan, the Decisions tab, the stories in Jira and the org summary. Only what those sources say; nothing invented.
2. Run, in the client's repo: `python3 -I build-review.py --content content.json --base <the org reader's commit, or main when the plan was written> --head main [--head task/<ID> for each open pull request] --out build-review.html`. With no repo yet (Claude chat, planning only), leave out `--base` and `--head`; the page is built from `planned` alone and says so.
3. The script reads every changed component's metadata file for its details (field type, length, picklist values, formula, help text, relationship and delete behavior, roll-ups, validation rule formula and message, flow type and trigger, page object, action target, list view columns, permission set object and field access), draws the data model and the flows, and adds what it finds on its own to Needs you: new fields or objects no permission set in the build grants, and two active record-triggered flows on the same object and moment, existing ones included.
4. Publish it: where the session has the Artifact tool, as an artifact (the first time, a new one; after that, a new version of the same one, so the link never changes). Always save the HTML to the client's Drive folder (`Build` subfolder) as `drive-copies.md` sets out, so the page outlives the account that published it; where there is no Artifact tool, also save `docs/build-review.html` in the repo. Where the client's team keeps its designs in Notion (Fred Hutch does), also offer a Notion page under the client's design pages with the same sections as text and tables, linking to the artifact for the diagrams; never write to a client's Notion space without the person saying so.
5. Read the Needs you section before reporting. Anything "Found in the build" goes in the report to the person and, for a task, in the pull request's "Check before you merge".

## content.json

Every field is optional except `client`. Text fields take `**bold**`, `` `code` `` and `[text](url)`.

```
client, title, summary (two to four sentences: how the build hangs together, in plain words),
functional: {overview (two or three sentences: what the build accomplishes for the client, in their words, no API names), roles: [{who, can: [what that kind of user can do once it is live, one line each, from the stories]}], not_in (what someone might expect that this build does not do, in a clause)},
status ("Build plan draft, not approved" / "Approved by <SA> on <date> · 4 of 11 tasks built"), sa, as_of,
links (design, build plan, Decisions tab, repo, as one line of links), jira_base, decisions_url,
needs_you: [{kind: "Review" | "Changes what exists" | "Removes", text}]   (anything else waiting on a person; open decisions come from decisions),
stories: [{key (Jira key), title, gives (what the design gives this story)}],
differences: [{n, says (story and AC), does (what the design does), rec (the recommended rewording or design change)}],
decisions: [{id, status (Decided | Proposed), kind (Clear | Recommended | SA call | Client call), q, chosen (the decision as a statement, for Decided), why, considered (the options not chosen, in a clause), by, date, options: [{k, name}] and recommended (for Proposed)}]   (every row of the Decisions tab this build touches),
today: [{area, today, after}],
flows: [{name, steps: [{actor ("System" for automation), text}], outcomes: [{when, then}]}],
automation: [{name, type, runs_when, does, beside (what else runs on the same object and moment, from the org summary), status}],
pages: [{name, object, shows}],
access: [lines], reporting: [lines],
planned: [{type (metadata type), member (Object.Field and so on), change (New | Changed | Removed), label, details, why,
           story (Jira key), task, decision (D-ID), waits (D-ID or task)}],
solution_map: [{object, epics: {"E1": "creates it", "E3": "adds Status values"}, owner (the one flow per object and moment), later_only (true for an object only later epics build), parent (its parent object, drawn dashed in the data model)}]   (from the design's Solution map, for the objects this build touches),
tasks: [{id, story, holds, waits, status (Planned | Waits | Built | Merged | Handed back), pr}],
open_questions: [{n, q, owner, blocks}],
checks: [the by-hand checks a person makes in the sandbox, each with its worked example],
not_built: [lines], sources: [lines], changelog: [{date, change}]
```

`planned` is the build plan's component list. Once a component is in the repo, its details come from the file and the plan's story, task, decision and why stay attached to it.

## What the SA should be able to answer from it, without asking

- What is new, what changes something that exists, and what is removed, with what depends on each.
- Why each structural choice was made, and who made it (the Decisions tab IDs link back).
- Which story and criterion each component serves, and which components serve nothing (a component with no story or task is reported as a finding).
- Who can see and edit each new object and field.
- What runs on each object and event, including what was already there.
- What is waiting on whom.
