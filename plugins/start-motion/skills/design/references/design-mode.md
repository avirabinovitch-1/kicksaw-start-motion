<!-- Copy of plugins/start-motion/shared/design-mode.md, written by scripts/sync-agents.py. Do not edit here. -->

# How the SA wants to work on a design

`/start-motion:design` starts a new design by asking the SA one thing: Build together or Run with it. It is asked once, right after the Start report and before anything is drafted. The answer holds for this design unless the person saves it as their default or switches later.

Updating a design that already exists, and getting one ready to share, do not ask. They carry on in whatever state the design is in.

## 1. A saved default comes first

Before showing the picker, look for the person's default:

- in the client's repo, when the session has one: `.start-motion/my-defaults.json`, under `"design"`: `{"design": {"mode": "together", "saved": "2026-11-11"}}`. The file is the person's own, listed in `.gitignore` and never committed.
- otherwise a line in the client's Claude Project instructions: `Design mode: Build together` or `Design mode: Run with it`.

When there is one, do not show the picker. Say what you are using in one line and start: "Using your default for Harborlight: Run with it. Say "pick again" to change it."

The person can also name the mode in the request ("/design Harborlight, run with it"), which wins over the default for this design only. "Pick again" shows the picker.

## 2. The picker

Wherever the session can show an interactive visual (Claude chat and Cowork both can), show `references/design-mode-picker.html` as one. Change only the `CFG` line at the top of its script; send the rest as it is:

- `client`: the client's name.
- `mode`: `T` (Build together, the default) or `R`, the option to show selected.
- `n`: how many capabilities or integrations the scope holds, counted from the SOW and the requirements list. Leave it 0 when you cannot count them yet.
- `canSave`: true when there is somewhere to keep a default (section 1), otherwise false, which hides the checkbox.

One line above it: "Harborlight has five capabilities in scope. How do you want to work on the design?"

The picker returns one message: the mode and whether to save it as the default. When it says save: with a repo, write `.start-motion/my-defaults.json` (and add it to `.gitignore` if it is not there); without one, give the person the one line to add to the client's Claude Project instructions. Then say in one line what was saved and how to change it.

Only where no visual can be shown (Claude Code in a terminal, Codex), ask the same with the session's pick tool or in plain text: "Build together (we start with the data model and the big design choices, then go one capability at a time) or Run with it (I draft the whole design and you work back through the decisions in the document)?"

When nobody answers (an unattended run), use the saved default if there is one, otherwise Run with it, and say so at the top of the report.

## 3. What the mode changes, and what it never changes

The mode changes when the SA is asked and where they answer. It never changes what is designed, the Decisions tab, the design reviewer, where the design is saved or who approves it. Both modes end with the same design document.

| | Build together | Run with it |
|---|---|---|
| The data model and the structural decisions | Shown first. The SA decides them before any capability is written | Shown first, on Claude's picks. Claude keeps going without waiting |
| Capabilities | One at a time in the chat: what it needs, what Claude would build, its decisions. The SA confirms before the next | All drafted in one sitting on Claude's picks |
| Where decisions are answered | In the chat, in the decision picker | Inside the design document, with Next decision |
| The design reviewer | Once, when the last capability is confirmed | Once, when the draft is complete, before the SA sees it |

The one time Run with it stops first: a structural decision where Claude has no pick it can defend and most of the design depends on the answer. Ask that one question, in the decision picker, and carry on when it is answered. Drafting a whole design on a coin flip wastes the SA's time.

The person can switch at any point by saying so ("slow down, one at a time", "just run with it"). Switch from the next capability on and say so in one line. Switching does not change a saved default.
