---
name: build
description: Start Motion build (/start-motion:build). Builds a client's approved build plan one task at a time in a sandbox. For each task a builder agent makes the change as metadata in a branch and validates it, two reviewer agents check it against the story and against Salesforce practice, and the result is a pull request with its evidence for a person to review and merge. Agents never deploy to production, never touch records and never merge. Use whenever someone says "build [client]", "build the next task", "build E1.2-T1", "what is left to build" or "write the UAT script for [story]".
---

# Kicksaw build

One request ("build the next task for [Client]") takes one task from the approved build plan to a pull request a person can read and merge. The work is done by agents, each with one job and no memory of the others' reasoning: a builder makes the change, a test writer writes the tests from the criteria, and two reviewers check the result. You run them in order, pass along only what each is meant to see, and stop when a person is needed. A person reviews every pull request and merges it. That is the gate, and nothing here goes around it.

This stage needs a terminal with the client's repo and the Salesforce CLI signed in to the sandbox: Claude Code, Cowork with the repo folder connected, or Codex. In Claude chat with no terminal, say so in one line and stop; the build plan can be read and discussed there, but nothing can be built.

## Start: where the build stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the rules the agents cannot break, what "done" means, and the link to the Start Motion page. Read `references/decisions.md` too: what the agents are handed from the Decisions tab and what happens when a task needs a decision.

Look before you ask. Report in a few lines: the build plan (`docs/build-plan.md`: approved by whom and when, or still Draft); the tasks (how many Planned, Built, Merged, Handed back); the next task in build order whose dependencies are merged; the sandbox alias and that it is a sandbox; the repo's main branch and whether it is clean and up to date; any pull request still open from an earlier task; and the decisions the next tasks wait on.

Before reporting, catch up on what happened while nobody was in the conversation: fetch the repo, and for every task marked Built whose pull request has since been merged (`gh pr view <number> --json state,mergedAt` where the GitHub CLI is signed in; otherwise `git branch -r --merged origin/<main>`), set it to Merged in the plan with the date and update its story in Jira (section 3). Say how many you caught up in one line. Nobody should have to tell you a pull request was merged. For example: "Neo. Plan approved by Steph McAllister, Nov 12. 31 tasks: 6 merged, 1 built and waiting on review (E1.1-T3, PR 7), 24 planned. Next: E1.2-T1, four fields on Referral. Sandbox: neo-dev, confirmed a sandbox."

A task marked "removes" in the plan is shown to the person before it starts: the exact item, what refers to it, what happens to its data. Wait for a plain yes that names the item. The builder then takes it out of the repo only; the person removes it from the sandbox by hand.

These stop the run, each with one line on what is waiting and on whom:
- The build plan is not approved. Nothing is built from a draft. The SA can say "build from the draft" for a named task; record that in the task note.
- The alias is not a sandbox, or cannot be confirmed as one. There is no override for this one: this stage never runs against production, whoever asks.
- The task's dependencies are not merged, or the task waits on a decision still Proposed. This holds that task only: say which, and build the next task that is ready.
- The main branch has changes that are not committed.

## What to ask: one message

Ask only for what the Start did not find: which task, when the request did not say and more than one is ready (the next in build order is the default); the sandbox alias, when more than one is signed in. Then read back in one line and run: "Building E1.2-T1 for Neo in neo-dev: four fields on Referral, AC 1 to 3."

Build one task per request unless the person says to keep going ("build the next five", "build the Referral epic"). Even then, each task gets its own branch, its own reviews and its own pull request. A task that needs a person is handed back (section 4) and the run carries on with the next task that does not depend on it; tasks that do depend on it are skipped and listed. The run stops early only for what stops every task: the org is not a sandbox, the main branch is not clean, or the CLI sign-in has expired.

## 1. One task, start to finish

**Starting an agent.** Start each agent by name (`start-motion:builder`, `start-motion:test-writer`, `start-motion:story-compliance-reviewer`, `start-motion:salesforce-quality-reviewer`) and hand it only what its file says it is handed. Never pass one agent another's reasoning: the reviewers get the branch and the criteria, not the builder's answer; the builder gets the reviewers' findings, not their working. Where the session cannot start a separate agent, the instructions are at `references/agents/<name>.md`; run them yourself as separate passes, re-reading the branch from the files each time, and say on the pull request that the reviews ran in one session. That is weaker than separate readers and the person reviewing should know.

1. **Branch.** From the up-to-date main branch, create `task/<task ID>`.
2. **Tests first, when the task has code.** Start the test writer (Apex tests) with the task ID, the story, the criteria the task covers and the names from the plan. It commits the tests to the branch.
3. **Build.** Start the builder with the task (with its story's Jira key and its workflow line), the repo path and branch, the sandbox alias, the part of the design the task touches (from the design version the plan names), the org summary, the SOW limits, the Decided rows the task builds to (ID, Decision, Chosen, Why) and the Solution map rows for the objects it touches. It makes the change, validates it against the sandbox and commits.
4. **If the builder stopped** (a decision nobody made, a limit reached, an error it could not clear), go to "Handing a task back". When it wrote a Decision needed, first log it on the Decisions tab as a Proposed SA call (Raised in: the task ID, Affects: this task and the ones that depend on it), with the builder's options and lean as written.
5. **Review.** Start both reviewers on the branch at the same time; neither waits for the other:
   - the story compliance reviewer, with the story's criteria and which ones this task covers;
   - the Salesforce quality reviewer, with the org summary, `docs/house-rules.md` when it exists, the Decided rows the task builds to and the Solution map rows for the objects it touches.
6. **Findings go back to the builder.** Hand the builder the findings as written, nothing more. It fixes, validates and commits; the reviewers read the branch again from the start. **Three rounds at most.** After the third round with a criterion still not met or a must-fix still open, go to "Handing a task back".
7. **When both reviewers pass,** tell the builder so; it writes the task note at `docs/tasks/<task ID>.md`.
8. **Open the pull request** from `task/<task ID>` into the main branch (section 2), update the story in Jira (section 3), and set the task to Built in `docs/build-plan.md`.
9. **Ask whether to deploy it to the sandbox.** One line, with what and where: "E1.2-T1 passed both reviews. Deploy it to neo-dev (a sandbox) so you can check it by hand before you merge?" On a yes, run the deploy of the task branch's changed files; the org guard shows the person the command and their confirmation there is the one confirmation. Never deploy without being asked each time, and never to an org the client is testing in unless the person says that is the org they mean. Add a line to the task note and the pull request: "Deployed to <alias> on <date> from commit <id>". On a no, carry on; the by-hand checks then wait until after the merge.
10. **Stop.** A person reviews the pull request and merges it. Never merge, never approve your own pull request, and never push to the main branch.

When a pull request is merged (the person says so, or the next run finds it merged), set the task to Merged in the plan, with the date, and update the story's Metadata field (section 3).

After every task that reaches a pull request, every merge caught up on and every undo, update the design and build review page (`references/build-review.md`): refresh `content.json` (the task's status and pull request, any decision logged) and run `scripts/build-review.py` with `--head main` and a `--head` for each open task branch, then publish it to the same artifact and save the new HTML to the client's Drive folder (`Build` subfolder) as `references/drive-copies.md` sets out. Anything it finds on its own for this task goes in the pull request's Check before you merge.

## 2. The pull request

Title: `<Jira key> <task ID>: <what changed>` ("HLS-157 E1.2-T1: four fields on Referral"). The Jira key at the start, in the title, the branch's commits and the body, is what puts the pull request on the story's Development panel in Jira when the client's Jira has the GitHub app; the evidence note links it either way. The person reviewing reads the top of the body and decides from there, so the top is short and in plain words:

- **What this does:** one or two sentences, in the story's language, no API names.
- **Check before you merge:** the link to the design and build review page, then the checks only a person can do, as a short list ("open a Referral as an intake specialist and confirm Court date shows under Intake"). "Nothing to check by hand" when there is nothing.
- **Decide:** names the builder chose, anything removed, should-fix items left. "Nothing to decide" when there is nothing. Design decisions are never decided in a pull request: they are on the Decisions tab, and the evidence below lists the ones this task built to.

Then the evidence, in this order:
- The story (ID, title, Jira link) and the criteria this task covers.
- What changed: each file, created or changed.
- The validation: the command's result against the sandbox, and the tests that ran.
- The story compliance result: each criterion as Met (with the file), or Cannot tell from the files (with what to check by hand in the sandbox). The person reviewing does those checks.
- The Salesforce quality result: Pass, and any should-fix items left, each with its reason.
- How many rounds it took, and whether the reviews ran as separate agents or in one session.
- Names the builder chose that the design did not give, for the SA to confirm.
- The decisions this task built to, by ID with what was chosen.
- The metadata in this pull request, as the Metadata field will list it (section 3).
- Suggestions: anything useful the task did not ask for. Not built.

Nothing in the pull request claims more than was checked. "It should work" is not evidence.

## 3. The story in Jira

The Jira story is where the team, the PM and the client's QA look, so what was built is recorded on the story as well as in the repo. Find each field by its name on the story (`getJiraIssueTypeMetaWithFields` for the project and issue type), never by a field ID from another project. Never write a field the project does not have; say which ones it lacks once, and put that content in the evidence note instead.

**Metadata.** The story's Metadata field lists every component built for it, one `Type/Member` per line, in the form the team already uses (`CustomField/Note__c.Matter__c`, `Layout/Case-Matter Layout`, `Flow/Audit_Before_Save_Set_Matter_Owner`). The list comes from git, never from your own reading:

1. `python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/metadata-list.py" list <main> task/<task ID> > .start-motion/meta/<task ID>.txt` in the client's repo. Anything it prints as "not named" goes in the Decide line of the pull request for a person to add by hand.
2. When the task's pull request is merged: read the field as it is into a file, then `metadata-list.py merge <field.txt> .start-motion/meta/<task ID>.txt` and write the result back. Lines already there stay, in their order, including lines a person added; only new lines are added, at the end. The field holds what is merged, so a pull request still open is not in it.
3. What a task removed (`list ... --removed`) never goes in Metadata. It goes in the Build/Solution Details field as "Removed in <task ID>: <items>, removed from the org by <person> by hand".

**The evidence note,** a comment when the pull request opens, short enough to read in a minute:

```
Built: <task ID> · <date> · pull request <link> · commit <short id>
Validation: passed against <sandbox alias> (<result line>)
AC 1: Met · <how it was checked: the file, the test, or "by hand in the sandbox, to do">
AC 2: Met · ...
Decisions: <the IDs this task built to, or "none">
Waiting on: review and merge by <the person>
```

**Deployment URL,** when the project has the field: the pull requests for the story, `https://github.com/<owner>/<repo>/pulls?q=<Jira key>`, so one link covers every task. Write it only when the field is empty or already holds a GitHub link; a link to another tool (a Copado flow, say) belongs to whoever put it there and stays.

**Build Environment,** when a task is deployed to the sandbox (step 9): the sandbox's kind from the field's own values (Developer Sandbox, Partial Sandbox, Full Sandbox). The kind is in the client repo's README next to the alias; if it is not, ask once and add it there. Never set Production; a production deployment is a person's, outside this stage.

**Test Steps,** when the story's UAT script is written (section 6): the script's steps, in the same words, so the tester has them on the story.

Never set Acceptance Criteria Validated?, Testing Feedback or the story's status: those are the tester's and the team's.

When the story's last task is merged, add one line: "All tasks merged <date>. Ready for QA." Do not move the story's status yourself unless the person says to.

## 4. Handing a task back

A task goes back to a person when the builder stopped, when three rounds did not clear it, or when a reviewer found that a criterion cannot be checked as written. Do not keep trying.

- Leave the branch as it is, pushed, with no pull request (or a draft one marked "handed back").
- Set the task to Handed back in the plan.
- Tell the person in a few lines: the task, what was built, what is still wrong (the finding, word for word), what was tried in each round, and what decision or fix it needs. A criterion that cannot be checked goes to the SC; a design question goes to the SA, as a row on the Decisions tab shown in the decision picker (`references/decision-picker.html`, stage "Build", or the plain text block in `references/decisions.md`); an error in the org goes to whoever owns the sandbox.
- Then carry on with the next task that does not depend on this one, if the person asked for more than one.
- The person builds the rest by hand, or answers and says "try again", which starts a fresh run of the task from step 3. An answered decision is written to the Decisions tab first, and the fresh run hands the builder the Decided row.

## 5. Deploying to the sandbox

The builder validates; it never deploys. A deploy happens in two places, each on the person's word: step 9 above, for one task that has passed its reviews; and when the person says "deploy what is merged to the sandbox", for the main branch. Either way, say in one line exactly what is going where ("Deploying main, 6 merged tasks, to neo-dev, a sandbox"), then run it. The org guard checks the org is a sandbox, shows the person the command, and their confirmation there is the single yes; do not ask a second time in chat. The guard refuses any saving deploy to an org that is not a sandbox.

## 5b. Undoing a rejected task

A task that was deployed for a by-hand check and then rejected has left its change in the sandbox. When the person rejects or closes the pull request, or says "undo E1.2-T1", take it back out. This is the one removal the kit runs, and it is narrow on purpose:

- only a task whose branch is **not merged**;
- only what **that task's branch created**, worked out from git by a fixed script, never from your own reading of the org;
- only in a **sandbox**;
- never records, and never anything that was in the org before the task.

Steps:
1. Run `bash "${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/undo-task.sh" prepare <task ID>` in the client's repo. It writes `.start-motion/undo/<task ID>/` and prints three lists: what the task created (to remove), what it changed (to put back to the main branch's version), and what it created that the script cannot name (to remove by hand).
2. Show the person the three lists as printed. Say what removing means for them: a removed field takes any values typed into it during the check with it, and stays recoverable in Setup under Deleted Fields for 15 days. Never edit the lists or the files the script wrote.
3. Put back what was changed: deploy the main branch's copy of each file in `restore.txt` to the sandbox. The guard asks the person to confirm.
4. Remove what was created: `sf project deploy start --manifest .start-motion/undo/<task ID>/package.xml --post-destructive-changes .start-motion/undo/<task ID>/destructiveChanges.xml --target-org <alias>`. The guard checks the list against git again, checks the org is a sandbox, and asks the person to confirm. If the guard refuses, do not look for another way; tell the person what it said.
5. Report what was removed, what was put back, and what is left for a person: anything on the by-hand list, an active flow that has to be switched off in Setup before it can be removed, and picklist values added to an existing field (putting the field back does not take a value away). Set the task to Handed back in the plan with "undone in <alias> on <date>". If the task was ever merged into the story's Metadata field (it cannot have been, since merged work is never undone this way, but check), take its lines out with `metadata-list.py drop`, keeping any line another task of the story still needs.

Work that is already merged is never undone this way. Taking merged work out is a new task in the build plan, named, approved by the SA and carried out by a person. This is the only deploy this stage runs, it runs only on a person's word in this conversation, and it never targets production. Production deployments are run by a person, outside this stage.

## 6. UAT scripts

When a story's tasks are all merged, or when asked ("write the UAT script for E1.2"), start the test writer (UAT script) with the story and the labels of what was built for it. It saves `docs/uat/<story ID>.md`. Tell the SC the script is there; the SC reads it before any client sees it. Once the SC has read it, write its steps to the story's Test Steps field (section 3).

## 7. The build log for the client

When asked ("update the build log for [Client]"), write or update the build log in the client's folder from the merged pull requests only: the date, what was built in the client's words (from the story's title and user story sentence, never API names), the story it belongs to, and whether it is ready for them to test. Nothing that is not merged goes in it.

## 8. Report back

For one task, a few lines: the task, the result (pull request link, or handed back and why), the review page's link, what the person needs to check by hand in the sandbox, names to confirm, and the next task in order. For a run of several, a short table: task, result, rounds, pull request. No recap of steps. Then, in one place, everything waiting on a person: pull requests to review, by-hand checks, and decisions (the picker, when any task was handed back on one).

End with one line naming what comes next: review and merge the pull request, then `/start-motion:build` for the next task; or, if the change is not right, reject it and say "undo <task ID>" to take it back out of the sandbox.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional. Write it quietly. The row, as plain text:

```
Run log · start-motion:build (v0.2.0) · build · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Tasks: <each task ID with its result: pull request opened, or handed back; and the rounds it took>
Corrected: <what the person corrected during the run, in one to three plain sentences. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own. "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- Metadata only. No agent and no step of this stage reads, queries, loads, changes or exports client records.
- Sandbox only. Nothing here ever targets production.
- Everything is a commit. No change is made in the org that is not in the repo.
- A person merges. Nothing reaches the main branch on an agent's say.
- Only what was approved. A task builds what the approved plan names; anything else is a suggestion.
- No agent deletes anything from an org: no records, no metadata. The one removal this stage runs is the undo of a rejected, unmerged task (section 5b): only what that task created, in a sandbox, from a list the script builds and the guard checks, on the person's confirmation. Every other removal is a named task a person carries out.
- The simplest build that satisfies the criteria: standard before custom, configuration before code, relationships and formulas before stored copies, nothing added for later.
- SOW limits are counted before anything is added.
- Sign-ins stay in the Salesforce CLI on the person's computer. Never in the repo, a pull request, a Jira comment or the chat.
- Three rounds, then a person.
- One task needing a person never stops the others. Hand it back, log what it needs, and build what does not depend on it.
- What was built is on the story: the Metadata field from git once merged, the evidence note, and the other fields in section 3. Never a field the tester or the team owns.
- No em dashes.
