# Kicksaw Project Start Motion

The Kicksaw delivery kit as a Claude plugin. The seven stages of a net-new project run as skills, each one with the templates, logos and scripts it builds from. The method, the examples and the prompt builders stay on the Start Motion page (https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S); this plugin is where the work runs.

Two ways to work, both supported:

- **Page first.** Read the stage on Start Motion, use its builder or copy its prompt, paste into Claude. The page's copy boxes and prompts stay; the same skill text the page hands out is what this plugin installs.
- **Claude first.** Open Claude and type the stage's command. The skill says where the client stands, asks for its picks in one message, runs, and names the next command.

## What delivery can count on

The signed SOW, and whatever else is in the client's Drive folder. Nothing more. Sales call transcripts, a handoff doc, contracts and client documents make every stage more specific when they are there; no stage waits for them, no skill looks for them in a folder with a particular name, and none of them missing is reported as a gap.

## The commands

| Stage | Command | What it does |
|---|---|---|
| Setup | `/start-motion:new-client` | Sets a new client up once: finds the SOW and whatever sales shared, finds or makes the client's Drive folder and its Discovery subfolder, checks the Claude Project and connectors, offers the discovery documents, names the first stage |
| 0 SOW and handoff (optional) | `/start-motion:handoff` | When sales shares a packet beyond the SOW: builds the handoff document on DJ's standard, drafts delivery's questions, folds in the handoff call. Nothing downstream waits for it |
| 1 Kickoff | `/start-motion:kickoff` | Builds the kickoff deck from the finished slide templates, shows the plan first |
| 2 Discovery | `/start-motion:discovery-plan` | Plans discovery from the SOW and the sales calls before kickoff; preps each session |
| 2 Discovery | `/start-motion:discovery-call` | Sets up the discovery documents; processes every call into them, drafting a story for every requirement |
| 3 Readout | `/start-motion:readout` | Section plan, build, dry run, deck, readout call, sign-off |
| 5 Design | `/start-motion:design` | Starts, updates and finalizes the solution design |
| 6 User stories | `/start-motion:user-stories` | Epics, finishing the stories, Jira, refinement |
| Build plan (0.2.0, not released) | `/start-motion:build-plan` | Turns approved stories and the approved design into ordered build tasks, each with the criteria it covers and the check that proves it. The SA approves it |
| Build (0.2.0, not released) | `/start-motion:build` | Builds the approved plan one task at a time in a sandbox: a builder agent makes the change, two reviewer agents check it, and a person reviews and merges the pull request |

In chat the commands show as their bare names (`/kickoff`, `/new-client`); in Cowork and Claude Code they carry the prefix.

Plain requests work too: "process today's Tog call", "make the kickoff deck for Tog", "build the readout for Tog".

Scope sign-off (stage 1.4) is a meeting; the readout skill carries its record.

## The agents (0.2.0, not released)

An agent is a separate worker with one job. A stage command starts it, hands it only what it needs, and gets back a short result. It does not see the conversation that produced the work it is checking: it reads a story the way the architect will, or a built field the way a tester will.

| Agent | Its one job | Started by |
|---|---|---|
| `source-checker` | Checks every requirement and story against the call, SOW section or document it cites; reports only rows that do not match | `discovery-call`, `user-stories` |
| `story-reviewer` | Reads each story with nothing but the story in hand; reports criteria that cannot be built or tested as written | `discovery-call`, `user-stories`, `build-plan` |
| `org-reader` | Reads an org's configuration through the Salesforce CLI, pulls it into the client repo and writes the org summary. Never reads records | `design`, `build-plan` |
| `design-reviewer` | Checks the design against the requirements in scope and against what is in the org | `design` |
| `builder` | Builds one approved task as metadata in a branch and validates it against the sandbox | `build` |
| `test-writer` | Writes Apex tests and UAT scripts from the acceptance criteria | `build` |
| `story-compliance-reviewer` | Checks what was built against each acceptance criterion | `build` |
| `salesforce-quality-reviewer` | Checks what was built against Salesforce practice and the team's house rules | `build` |

Claude Code, Cowork and Codex start these as separate agents. Claude chat cannot always do that, so each skill carries a copy of the agents it starts at `references/agents/` and runs them as a second pass there, and says on its report which way the check ran. `agents/` is the home of the text; `scripts/sync-agents.py` writes the copies and `--check` fails when one is out of date.

Rules no agent can break: configuration only, never client records; sandbox only, never production; nothing is deleted from an org, records or metadata; every change is a commit; a person merges; only what an approved task names, built the simplest sound way; SOW limits are counted; sign-ins stay in the Salesforce CLI on the person's computer.

**The org guard.** The rules above are also enforced outside the agents' instructions. `hooks/org-guard.sh` runs before every shell command in Claude Code and Cowork. It blocks Salesforce CLI commands that change, load, export or delete records, run anonymous Apex, call the org's API directly, delete metadata, delete an org or uninstall a package, and any saving deploy aimed at an org that is not a sandbox (it asks the CLI what kind of org the alias is). It stops and shows the person the command, to confirm themselves, for a query that returns client records, a deploy that saves to a sandbox, and the undo of a rejected task. Retrieves, validations, dry runs, test runs and queries about configuration (`--use-tooling-api`) pass.

**Undoing a rejected task.** `/build` asks, once a task has passed its reviews, whether to deploy it to the sandbox so the person can check it by hand before merging. If the pull request is then rejected, "undo <task ID>" takes the change back out. `skills/build/scripts/undo-task.sh` builds the list from git: only what that task's unmerged branch created is removed, what it changed is put back to the main branch's version, and the guard re-checks the list and the org before the person confirms. This is the only removal the kit runs.

## Install

The click-by-click version is the Start here page on Start Motion (https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S#start).

Personal Claude account: Customize, Plugins, Add marketplace, enter `avirabinovitch-1/kicksaw-start-motion`, then install **Kicksaw Project Start Motion**. Turn on **Sync automatically** so each weekly release reaches you without re-saving anything. One install covers chat, Cowork and Claude Code on the same account. You need read access to this repo; ask Avi.

Uploading the `.plugin` file from a release also works, but does not update itself.

## How the plugin and the page stay in step

- This repo is the home of the skill text (since Oct 30, 2026; the first build was taken from the page's embedded texts with `scripts/build-skills-from-page.py`, which is kept for the record and is no longer the source). Fixes land here during the week and go out together as one release on Mondays, with one list of what changed, so a skill does not change under anyone mid-client-week.
- Each release also refreshes the Start Motion page's embedded skill texts from this repo (`scripts/refresh-page-skills.py`), so the page's copy boxes and the plugin always hand out the same skill.
- The templates in each skill's folder are the copies Claude builds from. The Kicksaw Discovery Templates folder in Drive holds viewing copies of the page templates; the Kicksaw Slides design system holds the master copy of the kickoff slide templates. Both are refreshed from here on release.
- The requirements list stays a Google Sheet in Drive, copied per client.

## Layout

```
.claude-plugin/marketplace.json       the marketplace this repo is
plugins/start-motion/                 the plugin
  .claude-plugin/plugin.json
  agents/<agent>.md                   the eight agents (0.2.0)
  hooks/hooks.json, hooks/org-guard.sh  the org guard (0.2.0)
  skills/build/scripts/undo-task.sh   builds and checks the undo list for a rejected task (0.2.0)
  skills/<command>/SKILL.md           the skill
  skills/<command>/references/agents/  copies of the agents that skill starts, written by scripts/sync-agents.py
  skills/<command>/references/        method.md (what the stage is for, the bar, the page link) and other reference files
  skills/<command>/templates|brand|icons|scripts
scripts/refresh-page-skills.py        writes the eight skill texts into a saved copy of the Start Motion page
scripts/patch-page-work-in-claude.py  added the Work in Claude box to each stage (applied Oct 30, 2026; kept to rebuild the page)
scripts/patch-page-start-here.py      added the Start here page and the new-client row (applied Oct 30, 2026; kept to rebuild the page)
scripts/sync-agents.py                copies each agent into the skills that start it; --check fails on a stale copy
scripts/edits_0_2_0.py                the Oct 30 reading-rule and handoff-optional edits, applied in place (the record of what changed and why)
CHANGELOG.md                          what changed in each release
```

## Standing rules every skill keeps

- The signed SOW is the only required input at every stage. Everything else in the client's folder is read when it is there and never asked for when it is not.
- Plain consultant language on everything shared; no invented terms; no em dashes.
- Nothing is invented: no figure, name, date, owner or quote that was not said or is not in the SOW.
- The SC reviews every change before the client sees it.
