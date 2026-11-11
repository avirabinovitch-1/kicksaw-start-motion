# Build: what this stage is for

Take one approved build task to a pull request a person can read and merge, with the evidence attached. Agents do the first build of each task and the first two reviews, so the person's time goes to reading a change and its evidence, not to making the change and guessing whether it is complete.

## Who does what

- **The builder** makes the change for one task as metadata in a branch and validates it against the sandbox.
- **The test writer** writes Apex tests and UAT scripts from the acceptance criteria, not from how the task was built.
- **The story compliance reviewer** checks the change against each acceptance criterion, without seeing how the builder got there.
- **The Salesforce quality reviewer** checks the change against Salesforce practice and the team's house rules.
- **A person** reviews the pull request, does the checks metadata cannot show, and merges. A person runs every production deployment.

A reviewer and the builder go back and forth three times at most. After that the task stops and a person is asked.

## Rules the agents cannot break

- Metadata only. Agents read and change configuration. They do not read, query or export client records
- Sandbox only. Agents build in and validate against a sandbox
- Everything is a commit. No change is made in the org that is not also in the repo
- A person merges. Nothing reaches the main branch on an agent's say
- Only what was approved. Something useful that nobody asked for is reported as a suggestion, not built
- SOW limits are counted. Where the SOW sets a limit, the builder checks the count before adding and stops at the limit
- Sign-ins stay put. The org sign-in lives in the Salesforce CLI on the person's computer
- Nothing is deleted from an org by an agent: no records, no metadata. A removal is a named task a person carries out. The one exception is the undo of a rejected task, below
- Nothing is done in a production org. A person runs every production deployment

## Deploying and undoing

The builder validates and never deploys. Once a task has passed both reviews, the stage asks whether to deploy it to the sandbox, so the person can do the by-hand checks before merging. One yes per deploy.

If that task is then rejected, "undo <task ID>" takes it back out: what the task changed is put back to the main branch's version, and what the task created is removed. The list of what it created comes from git, built by a fixed script, and only an unmerged task in a sandbox can be undone. Nothing that was in the org before the task is touched.

## The org guard

The plugin backs these rules with an org guard (`hooks/org-guard.sh`) that checks every Salesforce CLI command before it runs:

- Blocked: changing, loading, exporting or deleting records; anonymous Apex; direct API calls; deleting metadata (other than the undo above); deleting an org; any saving deploy or removal aimed at an org that is not a sandbox
- Asks the person first: a query that returns client records; a deploy that saves to a sandbox; the undo of a rejected task
- Passes: retrieve, validate, dry runs, test runs, and queries about configuration

## What "done" means

A build task is done when all five are true:

1. The files the task names exist in the branch
2. The validation against the sandbox passed
3. The tests pass
4. The story compliance reviewer passed every criterion the task covers, and the quality reviewer passed where it applies
5. The evidence note is on the Jira story: the commit, the validation result, and each criterion with how it was checked

"It should work" is not on the list.

## Calls the person makes

- Merge or not? Read the pull request and its evidence, do the checks listed as "by hand in the sandbox", then merge
- A name the builder chose? Confirm it or change it before merging
- A task handed back? Answer the question it is waiting on, or build the rest by hand
- A suggestion? Raise it with the SC as a possible story, or drop it. It is never built on the side

## House rules

A team can add its own rules for the quality reviewer in `docs/house-rules.md` in the client's repo: naming, prefixes, which automation tool for which job, anything the team always or never does. House rules win over the reviewer's defaults.

The stage on the Start Motion page: https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S
