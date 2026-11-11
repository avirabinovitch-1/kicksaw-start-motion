---
name: build-plan
description: Start Motion build plan (/start-motion:build-plan). Turns a client's approved user stories and approved solution design into an ordered list of build tasks, each small enough to build and review in one sitting, each naming what is created or changed, the acceptance criteria it satisfies and the check that proves it. Saved in the client's repo for the solution architect to approve before anything is built. Use whenever someone says "build the plan for [client]", "break the stories into build tasks", "update the build plan" or "what is left to build for [client]".
---

# Kicksaw build plan

One request ("build the plan for [Client]") turns the approved stories into build tasks. The build plan is the bridge between a story a client approved and a change in the org: it settles the order, the dependencies and what "built" means for each story before anyone builds, so a developer who was not in discovery can pick up any task and build it without asking a question. The solution architect owns the plan and approves it. Nothing is built from a plan the SA has not approved.

## Start: where the build stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the Start Motion page.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask. Then report what you found, in a few lines, before doing anything else: the stories (how many are refined or approved in Jira, how many are still New or have open questions); the solution design (Final, Draft, or none); the client's repo (found, with its main branch, or none); the org summary (`docs/org-summary.md` and its date, or none); the sandbox (an alias signed in through the Salesforce CLI on this computer, or not); and whether a build plan already exists (`docs/build-plan.md`, with how many tasks are planned, built and merged). For example: "Neo. Stories: 18 refined, 4 with open questions. Design: Final, Nov 12. Repo: neo-salesforce, main. Org summary: Nov 10. Sandbox: signed in as neo-dev. Build plan: none yet. Next: draft the plan for the 18 refined stories."

Three things stop the run, each with one line saying what is waiting and on whom:
- No approved or refined stories. The plan is built from stories the client's product owner has been through.
- No design, or a design still marked Draft. The SA can say "plan from the draft"; that is recorded at the top of the plan.
- No client repo. Offer to set one up (section 1).

## What to ask: one message

Ask once, in one message, and only for what the Start did not find: which stories to plan when the request did not say (all refined stories is the default); the sandbox alias when more than one is signed in; and whether the team wants the tasks as sub-tasks in Jira as well as in the repo. Then read back what you heard in one line and run.

## 0. Load what you need

- The stories from Jira, with every field: user story, description, acceptance criteria, open questions, status, dependencies. Plan only stories with no open question that affects a criterion; list the others with the question that holds each one.
- The solution design, the version marked Final (or the draft, when the SA said so).
- `docs/org-summary.md` in the client's repo. If there is none, or the sandbox has changed since it was written, start the org reader first (section 2).
- The SOW's countable limits (custom fields per object, record types, flows, integration endpoints, source files), so each task can be checked against them.
- The existing `docs/build-plan.md`, when there is one: tasks already built or merged are never re-planned.

## 1. The client repo, when there is none

One GitHub repo per client holds the Salesforce metadata, the design, the build plan and a note for every build task. If the client has none, say so and offer to set it up with the person: they create the empty private repo in Kicksaw's GitHub organization and clone it; you add the standard Salesforce project layout, a `docs/` folder and a README naming the client and the sandbox alias (never a username or a login). Do not create a repo, change its settings or invite anyone on your own.

## 2. Read the org

The plan has to start from what is already in the sandbox. Start the org reader when `docs/org-summary.md` is missing or older than the last change anyone made in the sandbox. Hand it the client's name, the sandbox alias, the repo path, the SOW's countable limits and the date of the last summary.

**Starting an agent.** This stage needs a terminal with the Salesforce CLI and the client's repo: Claude Code, Cowork with the repo folder connected, or Codex. Start the agent by name (`start-motion:org-reader`, `start-motion:story-reviewer`) and hand it only what its file says it is handed. In Claude chat with no terminal, the org cannot be read: say so, and plan from the existing org summary if there is one, marked "planned from the org summary of <date>".

The plan is read from the sandbox. If the only org to read is production, ask the person first and wait for a plain yes that names the org; hand the org reader their name with the confirmation. Nothing in this stage or the next one ever changes a production org.

The org reader commits what it retrieved on its own branch. Show the person its answer and ask them to merge that branch before the plan is written, so every task branches from what is really in the org.

## 3. Check the stories once more

Before breaking stories into tasks, start the story reviewer on the stories being planned, handing it the stories and the org summary's list of existing objects and fields. A story with a finding that would stop a builder (a criterion that cannot be tested, no trigger, a value that is not exact) is not planned: list it with the finding and send it back to the SC. A story too large to build safely in a few tasks goes back to be split. Do not rewrite a story here.

## 4. Break the stories into tasks

For each story that passed:

- **Small enough to build and review in one sitting.** One task creates or changes a handful of closely related things: the fields for one object, one validation rule with its message, one flow, one class with its test, the page placement for one record type. If a reviewer would need more than a few minutes to read the change, it is two tasks.
- **Ordered by what depends on what.** Objects before fields, fields before layouts and permission sets, data model before automation, automation before reports. Across stories, follow the stories' own dependencies.
- **Each task names:**
  - its ID: the story ID and a number (`E1.2-T1`);
  - what is created or changed, by real name where the design or the org summary gives one, and marked "name from the design" where a new name is the design's;
  - the acceptance criteria it satisfies, by number. Every criterion of every planned story is covered by at least one task; say which task;
  - the check that proves it: the validation, the Apex test and what it must assert, or the step a person does by hand in the sandbox when metadata cannot show it;
  - what it depends on (task IDs);
  - whether it has code (the test writer writes tests for it) or is configuration only;
  - any SOW limit it counts against, with the count before and after.
- **Only what the stories ask for.** A task with no criterion behind it does not go in the plan. Something useful nobody asked for is listed at the end under Suggestions for the SA.
- **Manual steps are tasks too.** Anything metadata cannot carry (a setting switched on in Setup, a connected app's secret, a queue's members) is a task marked "by hand", with who does it.
- **Removing something is its own task, and a person does the removing.** A task that deletes, renames, deactivates or narrows anything already in the org (a field, a flow, a rule, a picklist value, a permission) is marked "removes", names the exact item, lists everything in the org summary that refers to it, and says what happens to any data it holds. The builder may take the item out of the repo for such a task; taking it out of the org is done by hand by the person named on the task. The SA sees every "removes" task listed on its own at the top of the plan before approving.
- **The fewest tasks that do the job.** No task adds a field, record type, status or branch that no criterion needs. Where the design gives a choice, plan the simpler build: standard before custom, configuration before code, a relationship or formula before a stored copy.
- **Data work is its own task and never the builder's.** Loading, cleaning or backfilling records is marked "by hand: data", outside what an agent builds.

## 5. Write the plan

Save `docs/build-plan.md` in the client's repo, on a branch named `build-plan/<date>`, in this shape:

- A header: the client, the date, the stories planned (count, and the Jira filter or keys), the design version, the org summary date, and a status line: "Draft, not approved". When the SA approves, the line becomes "Approved by <name> on <date>"; you write that only when the SA says so in this conversation.
- A table of every task in build order: ID, story, what it creates or changes, criteria covered, check, depends on, code or configuration or by hand, status (Planned, Built, Merged, Handed back).
- Under the table, one short block per task with the detail a builder needs: the names, the exact values from the criteria, the check in full.
- A coverage list: every planned story with its criteria and the task that covers each. A criterion with no task is a defect in the plan; fix it before showing the SA.
- Stories not planned, each with why (open question, a reviewer's finding, too large) and who it waits on.
- SOW limits: each one with the count today and the count when the plan is built.
- Suggestions: useful things nobody asked for, for the SA to raise or drop.

If the team wants them, create one Jira sub-task per task under its story, titled with the task ID and what it changes. Only after the SA approves the plan.

No em dashes. Real API names in code style. Never invent a name, a value or a limit: if the design does not give it, the task says "name from the SA" and the plan lists it as a question.

## 6. Keep it current

When asked ("update the [Client] build plan"): read the stories that changed in refinement since the plan was written, the design's changes and the tasks' statuses. Add tasks for new stories, change tasks whose criteria changed, and mark tasks whose story was withdrawn. A task that is Built or Merged is never edited; a change to its story becomes a new task. The plan goes back to "Draft, not approved" for the changed tasks only, and the SA approves those.

## 7. Report back

Three short paragraphs: what the plan covers (stories, tasks, how many have code), what the SA has to decide before approving (names to give, stories sent back, limits near), and what is not planned and why. No recap of steps.

End with one line naming what comes next: the SA reads and approves the plan; then `/start-motion:build` builds it one task at a time.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional. Write it quietly. The row, as plain text:

```
Run log · start-motion:build-plan (v0.2.0) · build plan · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own. "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- Nothing is built from a plan the SA has not approved, and you never mark a plan approved yourself.
- Every criterion of every planned story has a task. Every task has a criterion.
- Never invent an object, field, API name, value or limit.
- The plan never widens the signed scope.
- Agents never delete from an org and never touch a production org. A removal is a person's task; a production deployment is a person's job.
- Sign-in details never go in the repo. The alias is enough.
- No em dashes.
