# Kicksaw Project Start Motion

The Kicksaw delivery kit as a Claude plugin. The stages of a net-new project, from the SOW to the refinement sessions ahead of each sprint, run as skills, each one with the templates, logos and scripts it builds from. The method, the examples and the prompt builders stay on the Start Motion page (https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S); this plugin is where the work runs.

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
| 1.1 Kickoff | `/start-motion:kickoff` | Builds the kickoff deck from the finished slide templates, shows the plan first |
| 1.2 Discovery | `/start-motion:discovery-plan` | Plans discovery from the SOW and the sales calls before kickoff; preps each session |
| 1.2 Discovery | `/start-motion:discovery-call` | Sets up the discovery documents; processes every call into them, drafting a story for every requirement |
| 1.3 Readout | `/start-motion:readout` | Section plan, build, dry run, deck, readout call, sign-off |
| 2.1 Design | `/start-motion:design` | Starts, updates and finalizes the solution design |
| 2.2 User stories | `/start-motion:user-stories` | Epics, finishing the stories, Jira |
| 3 Refinement | `/start-motion:refinement` | Before each session: the SC picks the stories by sprint, epic or one by one, and gets the refinement deck and a briefing on the call. After it: the answers folded into Jira from the recording |

In chat the commands show as their bare names (`/kickoff`, `/new-client`); in Cowork and Claude Code they carry the prefix.

Plain requests work too: "process today's Tog call", "make the kickoff deck for Tog", "build the readout for Tog".

Scope sign-off (stage 1.4) is a meeting; the readout skill carries its record.

Build plan and build are a separate, private plugin, Start Motion Build (`kicksaw-start-motion-build`), installed only by the people Avi grants access. It runs in Claude Code against a sandbox and carries its own guardrails. With it installed, `/start-motion:design` also reads the client's org through its org reader.

## The review agents

A review agent is a separate checker with one job. A stage command starts it, hands it only what it needs, and gets back a short list of findings. It does not see the conversation that produced the work, so it reads a requirement the way someone holding only the recording will, and a story the way the architect and the tester will. Reviewers change nothing; the stage command fixes what is plainly wrong and takes the rest to the SC or SA.

| Agent | Its one job | Started by |
|---|---|---|
| `source-checker` | Checks every requirement and story quote against the call, SOW section or document it cites; reports only rows that do not say what the client said | `discovery-call`, `user-stories` |
| `story-reviewer` | Reads each story with nothing but the story in hand; tells the SC where someone would have to guess, with the question to ask. Helps improve a story, never holds one back | `discovery-call`, `user-stories` |
| `design-reviewer` | Checks the design against the requirements and workflows in scope, the org, the decisions already made and what later epics need | `design` |

Each runs twice at most per run. Claude Code and Cowork start these as separate agents. Claude chat cannot always do that, so each skill carries a copy of the agents it starts at `references/agents/` and runs them as a second pass there, and says on its report which way the check ran.

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
  agents/<agent>.md                   the three review agents
  shared/                             texts several skills carry copies of (decisions, the decision picker, where files live in Drive)
  skills/<command>/SKILL.md           the skill
  skills/<command>/references/agents/  copies of the agents that skill starts, written by scripts/sync-agents.py
  skills/<command>/references/        method.md (what the stage is for, the bar, the page link) and other reference files
  skills/<command>/templates|brand|icons|scripts
scripts/refresh-page-skills.py        writes the eight skill texts into a saved copy of the Start Motion page
scripts/patch-page-work-in-claude.py  added the Work in Claude box to each stage (applied Oct 30, 2026; kept to rebuild the page)
scripts/patch-page-start-here.py      added the Start here page and the new-client row (applied Oct 30, 2026; kept to rebuild the page)
scripts/sync-agents.py                copies each agent and shared text into the skills that use them; --check fails on a stale copy
scripts/edits_0_2_0.py                the Oct 30 reading-rule and handoff-optional edits, applied in place (the record of what changed and why)
CHANGELOG.md                          what changed in each release
```

## Standing rules every skill keeps

- The signed SOW is the only required input at every stage. Everything else in the client's folder is read when it is there and never asked for when it is not.
- Plain consultant language on everything shared; no invented terms; no em dashes.
- Nothing is invented: no figure, name, date, owner or quote that was not said or is not in the SOW.
- The SC reviews every change before the client sees it.
