# Working choices: what to plan or build, and how

`/build-plan` and `/build` start by settling two things with the person: what this run covers (a sprint, an epic or specific stories) and how they want to work (Build together or Run with it). Both are asked together, on one picker, right after the Start report and before anything else is asked. The answers hold for this run only, unless the person saves them as their default.

## 1. Saved defaults come first

Before showing the picker, look for the person's saved default in the client's repo at `.start-motion/my-defaults.json`. That file is the person's own: it is listed in the repo's `.gitignore` and is never committed, so each person on the team keeps their own.

```json
{"build-plan": {"scope": "sprint", "mode": "together", "saved": "2026-11-11"},
 "build": {"scope": "sprint", "mode": "run", "saved": "2026-11-11"}}
```

`scope` is `sprint` (the next sprint in Jira, worked out fresh each run, section 3) or `epic` (the next epic in build order with refined stories not yet planned, or with approved tasks not yet built). Specific stories are never a default. `mode` is `together` or `run`.

When a default is saved for this command, do not show the picker. Work out what it means today and say so in one line, then start: "Using your default for Neo: Sprint 3 (9 stories across Referrals and Intake), Build together. Say "pick again" to change it." When a default no longer resolves (no future sprint in Jira, every epic planned), say so in that line and show the picker instead.

The person can say "pick again" (show the picker for this run, keeping the default), "clear my default" (delete this command's entry and show the picker) or name the scope or mode in the request ("/build-plan Neo Sprint 4", "build Neo, run with it"), which overrides the default for this run only.

In Claude chat with no repo folder, there is nowhere to keep a default: show the picker every time and do not offer to save.

## 2. The picker

In Claude chat and Cowork, show `references/mode-picker.html` as an interactive visual. Change only the `CFG` line at the top of its script; send the rest as it is:

- `cmd`: `plan` for `/build-plan`, `build` for `/build`.
- `client`: the client's name.
- `sprints`: the open sprints from Jira (the active sprint and future sprints, in start order), each `{key, when, stories, epics, note}`: the sprint name, when it starts ("Active, ends Nov 21", "Next sprint, starts Nov 17"), how many stories it holds (for `/build`, how many approved tasks are ready for its stories), the names of the epics those stories belong to, and a short note on where it stands ("0 of 9 planned", "3 of 12 tasks built"). Leave out sprints with nothing left to plan or build. Leave the list empty when the project has no sprints, and the picker shows only epic and specific stories.
- `epics`: each epic with something left to plan or build, `{key, name, stories, note}`.
- `scope`: the choice to show selected: `sprint` when the project has sprints, otherwise `epic`.

Every number comes from Jira and the build plan, never an estimate. The picker returns one message: what the run covers, the mode, and whether to save it as the default. When it says save, write `.start-motion/my-defaults.json` (and add `.start-motion/my-defaults.json` to the repo's `.gitignore` if it is not there), then say in one line what was saved and how to change it.

In Claude Code, Codex or anywhere the visual cannot be shown, ask the same with the session's pick tool, as up to three questions in one go: what this run covers (the sprints, then epics, then "Specific stories"), how to work (Build together, the default, first; Run with it; and "Explain the two first", which prints section 4 and asks again), and whether to use these every time. Use the one-line descriptions from section 4 as each option's description.

When nobody answers (an unattended run), use the saved default if there is one; otherwise the next sprint (or next epic) and Build together, and say so at the top of the report.

## 3. What each scope means

**A sprint.** The stories assigned to that sprint in Jira (JQL `sprint = "<name>"` in the client's project), whatever epics they belong to. For `/build-plan` this is usually the next sprint; for `/build`, the active one. The next sprint for a saved default is the earliest open sprint with stories not yet planned (`/build-plan`) or approved tasks not yet built (`/build`).

**An epic.** The epic's refined stories (`/build-plan`) or the approved tasks for its stories (`/build`).

**Specific stories.** The keys the person names. For `/build`, task IDs or story keys.

Planning a slice never means planning blind. In every scope:

- **The design is whole.** The plan works from the whole design and its Solution map, whatever slice is being planned.
- **Shared pieces are planned once, the first time any story needs them.** When a sprint holds three of an epic's five stories, the objects and the one flow per object and moment those stories share are planned in this sprint as foundation tasks, shaped for all five stories as the map says. Later sprints add to them.
- **A dependency outside the slice is flagged, never pulled in quietly.** When a story in this slice depends on a story that is not in it (a later sprint, or not in any sprint yet), the plan lists it under "Depends on work outside this sprint" with both story keys, plans everything that does not depend on it, and says in the report that the SA and PM need to decide: bring the other story into this sprint, or move this one out. That is a sprint loading question, and it is the PM's to settle with the SA.
- **One running plan.** `docs/build-plan.md` stays one plan for the client. Each run adds its slice under a heading naming it ("Sprint 3, planned Nov 12") and approval is per slice. The review page shows the whole build with the slice marked.

## 4. The two ways to work

The mode changes how often you stop and how much you explain. It never changes what is planned or built, the reviews, the Decisions tab, the review page, the guardrails or the approvals: in both modes the SA approves the plan before anything is built, every task gets both reviews and its own pull request, and a person merges.

One-line descriptions, used on the picker and in the pick tool (`n` is the count for the chosen scope):

- `/build-plan`, Build together: "We go one story at a time. I explain what each story needs and what I'd build, and you confirm every call before I move on."
- `/build-plan`, Run with it: "I turn all n stories into build tasks in one sitting. Anything the design already answers, I decide and note why. Real trade-offs wait for you in one list at the end."
- `/build`, Build together: "We go one task at a time. Before each one I tell you what it will change. After it, I show you what was built and wait for you before the next."
- `/build`, Run with it: "I build all n ready tasks back to back, each reviewed and in its own pull request. Anything that needs your call waits in one list at the end, and the rest keeps going."

A good fit for Build together: a first time with the kit, work that is complex or new to the person, or wanting to see the reasoning behind each piece. For Run with it: the person knows the solution well and wants a full draft fast, then reviews it in one sitting.

The person can switch at any point by saying so ("slow down, one at a time", "just run with it"); switch from the next story or task on and say so in one line. Switching mid-run does not change a saved default.
