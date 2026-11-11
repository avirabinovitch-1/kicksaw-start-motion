---
name: build
description: Start Motion build (/start-motion:build). Builds a client's approved build plan one task at a time in a sandbox. For each task a builder agent makes the change as metadata in a branch and validates it, two reviewer agents check it against the story and against Salesforce practice, and the result is a pull request with its evidence for a person to review and merge. Agents never deploy to production, never touch records and never merge. Use whenever someone says "build [client]", "build the next task", "build E1.2-T1", "what is left to build" or "write the UAT script for [story]".
---

# Kicksaw build

One request ("build the next task for [Client]") takes one task from the approved build plan to a pull request a person can read and merge. The work is done by agents, each with one job and no memory of the others' reasoning: a builder makes the change, a test writer writes the tests from the criteria, and two reviewers check the result. You run them in order, pass along only what each is meant to see, and stop when a person is needed. A person reviews every pull request and merges it. That is the gate, and nothing here goes around it.

This stage needs a terminal with the client's repo and the Salesforce CLI signed in to the sandbox: Claude Code, Cowork with the repo folder connected, or Codex. In Claude chat with no terminal, say so in one line and stop; the build plan can be read and discussed there, but nothing can be built.

## Start: where the build stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the rules the agents cannot break, what "done" means, and the link to the Start Motion page.

Look before you ask. Report in a few lines: the build plan (`docs/build-plan.md`: approved by whom and when, or still Draft); the tasks (how many Planned, Built, Merged, Handed back); the next task in build order whose dependencies are merged; the sandbox alias and that it is a sandbox; the repo's main branch and whether it is clean and up to date; and any pull request still open from an earlier task. For example: "Neo. Plan approved by Steph McAllister, Nov 12. 31 tasks: 6 merged, 1 built and waiting on review (E1.1-T3, PR 7), 24 planned. Next: E1.2-T1, four fields on Referral. Sandbox: neo-dev, confirmed a sandbox."

These stop the run, each with one line on what is waiting and on whom:
- The build plan is not approved. Nothing is built from a draft. The SA can say "build from the draft" for a named task; record that in the task note.
- The alias is not a sandbox, or cannot be confirmed as one.
- The task's dependencies are not merged.
- The main branch has changes that are not committed.

## What to ask: one message

Ask only for what the Start did not find: which task, when the request did not say and more than one is ready (the next in build order is the default); the sandbox alias, when more than one is signed in. Then read back in one line and run: "Building E1.2-T1 for Neo in neo-dev: four fields on Referral, AC 1 to 3."

Build one task per request unless the person says to keep going ("build the next five", "build the Referral epic"). Even then, each task gets its own branch, its own reviews and its own pull request, and the run stops at the first task that needs a person.

## 1. One task, start to finish

**Starting an agent.** Start each agent by name (`start-motion:builder`, `start-motion:test-writer`, `start-motion:story-compliance-reviewer`, `start-motion:salesforce-quality-reviewer`) and hand it only what its file says it is handed. Never pass one agent another's reasoning: the reviewers get the branch and the criteria, not the builder's answer; the builder gets the reviewers' findings, not their working. Where the session cannot start a separate agent, the instructions are at `references/reviewers/<name>.md`; run them yourself as separate passes, re-reading the branch from the files each time, and say on the pull request that the reviews ran in one session. That is weaker than separate readers and the person reviewing should know.

1. **Branch.** From the up-to-date main branch, create `task/<task ID>`.
2. **Tests first, when the task has code.** Start the test writer (Apex tests) with the task ID, the story, the criteria the task covers and the names from the plan. It commits the tests to the branch.
3. **Build.** Start the builder with the task, the repo path and branch, the sandbox alias, the part of the design the task touches, the org summary and the SOW limits. It makes the change, validates it against the sandbox and commits.
4. **If the builder stopped** (a decision nobody made, a limit reached, an error it could not clear), go to "Handing a task back".
5. **Review.** Start both reviewers on the branch:
   - the story compliance reviewer, with the story's criteria and which ones this task covers;
   - the Salesforce quality reviewer, with the org summary and `docs/house-rules.md` when it exists.
6. **Findings go back to the builder.** Hand the builder the findings as written, nothing more. It fixes, validates and commits; the reviewers read the branch again from the start. **Three rounds at most.** After the third round with a criterion still not met or a must-fix still open, go to "Handing a task back".
7. **When both reviewers pass,** tell the builder so; it writes the task note at `docs/tasks/<task ID>.md`.
8. **Open the pull request** from `task/<task ID>` into the main branch (section 2), post the evidence note on the Jira story (section 3), and set the task to Built in `docs/build-plan.md`.
9. **Stop.** A person reviews the pull request and merges it. Never merge, never approve your own pull request, and never push to the main branch.

When the person says a pull request was merged, set the task to Merged in the plan, with the date.

## 2. The pull request

Title: `<task ID>: <what changed>`. Body, in this order:
- The story (ID, title, Jira link) and the criteria this task covers.
- What changed: each file, created or changed.
- The validation: the command's result against the sandbox, and the tests that ran.
- The story compliance result: each criterion as Met (with the file), or Cannot tell from the files (with what to check by hand in the sandbox). The person reviewing does those checks.
- The Salesforce quality result: Pass, and any should-fix items left, each with its reason.
- How many rounds it took, and whether the reviews ran as separate agents or in one session.
- Names the builder chose that the design did not give, for the SA to confirm.
- Suggestions: anything useful the task did not ask for. Not built.

Nothing in the pull request claims more than was checked. "It should work" is not evidence.

## 3. The evidence note on the story

A comment on the Jira story, short enough to read in a minute:

```
Built: <task ID> · <date> · pull request <link> · commit <short id>
Validation: passed against <sandbox alias> (<result line>)
AC 1: Met · <how it was checked: the file, the test, or "by hand in the sandbox, to do">
AC 2: Met · ...
Waiting on: review and merge by <the person>
```

When the story's last task is merged, add one line: "All tasks merged <date>. Ready for QA." Do not move the story's status yourself unless the person says to.

## 4. Handing a task back

A task goes back to a person when the builder stopped, when three rounds did not clear it, or when a reviewer found that a criterion cannot be checked as written. Do not keep trying.

- Leave the branch as it is, pushed, with no pull request (or a draft one marked "handed back").
- Set the task to Handed back in the plan.
- Tell the person in a few lines: the task, what was built, what is still wrong (the finding, word for word), what was tried in each round, and what decision or fix it needs. A criterion that cannot be checked goes to the SC; a design question goes to the SA; an error in the org goes to whoever owns the sandbox.
- The person builds the rest by hand, or answers and says "try again", which starts a fresh run of the task from step 3.

## 5. Deploying merged work to the sandbox

Agents validate; they do not deploy. When the person says "deploy what is merged to the sandbox", confirm the alias is a sandbox, deploy the main branch's metadata to it, run the tests, and report the result line. This is the only deploy this stage runs, it runs only on a person's word in this conversation, and it never targets production. Production deployments are run by a person, outside this stage.

## 6. UAT scripts

When a story's tasks are all merged, or when asked ("write the UAT script for E1.2"), start the test writer (UAT script) with the story and the labels of what was built for it. It saves `docs/uat/<story ID>.md`. Tell the SC the script is there; the SC reads it before any client sees it.

## 7. The build log for the client

When asked ("update the build log for [Client]"), write or update the build log in the client's folder from the merged pull requests only: the date, what was built in the client's words (from the story's title and user story sentence, never API names), the story it belongs to, and whether it is ready for them to test. Nothing that is not merged goes in it.

## 8. Report back

For one task, a few lines: the task, the result (pull request link, or handed back and why), what the person needs to check by hand in the sandbox, names to confirm, and the next task in order. For a run of several, a short table: task, result, rounds, pull request. No recap of steps.

End with one line naming what comes next: review and merge the pull request; then `/start-motion:build` for the next task.

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
- SOW limits are counted before anything is added.
- Sign-ins stay in the Salesforce CLI on the person's computer. Never in the repo, a pull request, a Jira comment or the chat.
- Three rounds, then a person.
- No em dashes.
