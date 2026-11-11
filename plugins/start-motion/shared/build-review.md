# The design and build review page

One page per client build, for the SA. The SA is accountable for every component that goes into the org and for the architecture holding together, so this page puts in one place what is being created or changed, why, and where it stands. It is modeled on Ben Bolding's Fred Hutch epic designs in Notion (Stories this design serves, Where the design differs from the stories, Rules that shape the design, Today and after, the objects, the flow, Fields, objects and settings, Who can do what, Automation, The build, Open questions, Verification items, Not built, Sources, Change log), with diagrams added and the component list read from the repo.

The home of this text is `plugins/start-motion/shared/build-review.md`; skills carry copies, written by `scripts/sync-agents.py`.

## How it looks

On the Kicksaw brand: a navy header band with the logo, a cyan eyebrow and the orange rule; Inter for headings, Source Sans 3 for text; orange only for what needs the SA. The side navigation groups the page into Review (Needs you, decisions, stories, differences), Design (today and after, data model, flows, automation, pages, access, reporting), Build (every component, changes to what exists, tasks, checks) and Reference. Needs you is sorted by urgency: decisions, then what the page found on its own, then changes to what exists, then what to confirm and review. The data model is an entity diagram: each object with its new and changed fields and their types, and each relationship drawn from its field to the parent. Every component is grouped by object, so the SA reviews one object at a time.

## When it is made and updated

- `/start-motion:build-plan` makes it when the plan is drafted, before the SA approves: everything is Planned or Waits. The SA reviews the plan from this page.
- `/start-motion:build` updates it after every task that reaches a pull request, after every merge it catches up on, and after an undo: components move to Built and Merged, and their details are read from the metadata files.
- `/start-motion:design` links to it once a plan exists.
- Its link goes in the build plan's header, the decision picker (`review`), every pull request's "Check before you merge", and the story's evidence note in Jira.

## How it is made

1. Write `content.json` (below) from the design, the build plan, the Decisions tab, the stories in Jira and the org summary. Only what those sources say; nothing invented.
2. Run, in the client's repo: `python3 -I build-review.py --content content.json --base <the org reader's commit, or main when the plan was written> --head main [--head task/<ID> for each open pull request] --out build-review.html`. With no repo yet (Claude chat, planning only), leave out `--base` and `--head`; the page is built from `planned` alone and says so.
3. The script reads every changed component's metadata file for its details (field type, length, picklist values, formula, help text, relationship and delete behavior, roll-ups, validation rule formula and message, flow type and trigger, page object, action target, list view columns, permission set object and field access), draws the data model and the flows, and adds what it finds on its own to Needs you: new fields or objects no permission set in the build grants, and two active record-triggered flows on the same object and moment, existing ones included.
4. Publish it: where the session has the Artifact tool, as an artifact (the first time, a new one; after that, a new version of the same one, so the link never changes). Elsewhere, save `docs/build-review.html` in the repo and a copy to the client's Drive folder. Where the client's team keeps its designs in Notion (Fred Hutch does), also offer a Notion page under the client's design pages with the same sections as text and tables, linking to the artifact for the diagrams; never write to a client's Notion space without the person saying so.
5. Read the Needs you section before reporting. Anything "Found in the build" goes in the report to the person and, for a task, in the pull request's "Check before you merge".

## content.json

Every field is optional except `client`. Text fields take `**bold**`, `` `code` `` and `[text](url)`.

```
client, title, summary (two to four sentences: what is built and how it hangs together, in plain words),
status ("Build plan draft, not approved" / "Approved by <SA> on <date> · 4 of 11 tasks built"), sa, as_of,
links (design, build plan, Decisions tab, repo, as one line of links), jira_base, decisions_url,
needs_you: [{kind: "SA call" | "Confirm" | "Review" | "Changes what exists" | "Removes", text, link}],
stories: [{key (Jira key), title, gives (what the design gives this story)}],
differences: [{n, says (story and AC), does (what the design does), rec (the recommended rewording or design change)}],
rules: [{id (D-ID), rule, why, by, date}]   (Decided rows only),
today: [{area, today, after}],
flows: [{name, steps: [{actor ("System" for automation), text}], outcomes: [{when, then}]}],
automation: [{name, type, runs_when, does, beside (what else runs on the same object and moment, from the org summary), status}],
pages: [{name, object, shows}],
access: [lines], reporting: [lines],
planned: [{type (metadata type), member (Object.Field and so on), change (New | Changed | Removed), label, details, why,
           story (Jira key), task, decision (D-ID), waits (D-ID or task)}],
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
