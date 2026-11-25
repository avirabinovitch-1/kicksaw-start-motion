# How the SC wants to work on the stories

`/start-motion:user-stories` asks the SC one thing once the epic plan is confirmed: Work together or Run with it. It is asked once per backlog, before any story is finished. The answer holds for this backlog unless the person saves it as their default or switches later.

Proposing the epics does not ask; the SC always confirms the epic plan first, in both modes. A run that picks up a backlog already under way carries on in the mode it was started in (the epic plan records it).

## 1. A saved default comes first

Before showing the picker, look for the person's default:

- in the client's repo, when the session has one: `.start-motion/my-defaults.json`, under `"stories"`: `{"stories": {"mode": "together", "saved": "2026-11-25"}}`. The file is the person's own, listed in `.gitignore` and never committed.
- otherwise a line in the client's Claude Project instructions: `Stories mode: Work together` or `Stories mode: Run with it`.

When there is one, do not show the picker. Say what you are using in one line and start: "Using your default for Harborlight: Run with it. Say "pick again" to change it."

The person can also name the mode in the request ("/user-stories Harborlight, run with it"), which wins over the default for this backlog only. "Pick again" shows the picker.

## 2. The picker

Wherever the session can show an interactive visual (Claude chat and Cowork both can), show `references/stories-mode-picker.html` as one. Change only the `CFG` line at the top of its script; send the rest as it is:

- `client`: the client's name.
- `mode`: `T` (Work together, the default) or `R`, the option to show selected.
- `epics` and `n`: how many epics and stories the confirmed epic plan holds.
- `canSave`: true when there is somewhere to keep a default (section 1), otherwise false, which hides the checkbox.

One line above it: "The epic plan is confirmed: seven epics, 42 stories. How do you want to work on them?"

The picker returns one message: the mode and whether to save it as the default. When it says save: with a repo, write `.start-motion/my-defaults.json` (and add it to `.gitignore` if it is not there); without one, give the person the one line to add to the client's Claude Project instructions. Then say in one line what was saved and how to change it. Write the mode on the first line of stories/epic-plan.md ("Mode: Run with it, chosen Nov 25 2026") so a later run knows.

Only where no visual can be shown (Claude Code in a terminal, Codex), ask the same with the session's pick tool or in plain text: "Work together (one story at a time: you read and approve each before it goes to Jira) or Run with it (I finish every story, create them all in Jira as New, and give you a list of the ones that need you)?"

When nobody answers (an unattended run), use the saved default if there is one. With no default, finish the stories on the User stories tab, create nothing in Jira, and say so at the top of the report: creating a whole backlog in a client's Jira project is the SC's choice to make.

## 3. What the mode changes, and what it never changes

The mode changes when the SC reads a story and where they change it. It never changes how a story is written, the standard it is held to, the two reviewers, the first estimate, the fields it fills in Jira, or who sends it to the client. Both modes end with the same backlog.

| | Work together | Run with it |
|---|---|---|
| The epic plan | The SC confirms it first | The SC confirms it first |
| Finishing the stories | One at a time; the SC sees each with its estimate and the reviewers' findings | All of them in one run, on Claude's best calls |
| A finding only the SC can settle (a source mismatch, a split or merge, beyond the SOW) | Shown under the story; the SC decides before it is created | Claude makes its best call, creates the story, and puts it on the review list under Needs a decision with the problem and what it would do |
| When a story is created in Jira | When the SC approves it | In the same run, as New |
| Where the SC changes a story | In the chat, before it is created | On the review list, editing the story in place, or in Jira |
| What says a story is reviewed | The SC's approval in the chat | The SC ticks it on the review list and it moves to Pending Client Approval |

The person can switch at any point by saying so ("slow down, one at a time", "just run with the rest"). Switch from the next story on and say so in one line. Stories already in Jira stay there. Switching does not change a saved default.

## 4. The review list (Run with it)

Once the backlog is in Jira, show `references/review-list.html` wherever an interactive visual can be shown. Change only the `CFG` block at the top of its script; send the rest as it is.

- `client`, `total` (stories created), `points` (the sum of the first estimates), `next` (the status a reviewed story moves to in this project's workflow, usually Pending Client Approval) and `jira` (the project's browse address ending in `/browse/`, so each story links to Jira; leave it empty to hide the link).
- `stories`: every story that is flagged, and the clean ones up to about thirty rows in all; the list says how many more clean stories there are. Each story: `k` (Jira key), `t` (title), `e` (epic), `g` (group), `f` (the flag in two or three words), `p` (points), `us`, `ds`, `ac` (the criteria, in order), `oq` (open questions), `rf` (the References lines), `hot` (the number of the criterion the flag is about, or 0), and for a flagged story `prob` and `rec`. Add `fix: {ac: 3, text: "..."}` when the recommendation is a new wording for one criterion, so the SC can apply it with one click.

The three groups:

- **Needs a decision** (`g: 'd'`): only the SC can settle it. The source checker found the story narrower or broader than what the client said, or a later call contradicts it; a split or merge that could reasonably go either way; a story beyond the SOW.
- **Worth a look** (`g: 'l'`): Claude made the call and the SC should see it. A large estimate left whole, three or more open questions, two drafts merged, a story changed after the SC had already reviewed it.
- **Clean** (`g: 'c'`): both reviewers passed and nothing was a judgment call.

Write `prob` and `rec` the way a colleague would say it across the desk, in one to three sentences each. `prob` says what is wrong and where, naming the criterion and the call. `rec` says what you would do and why. Never a label, a code or a finding ID in either.

Say one line above the list: "All 42 are in Jira as New. Three need a decision from you and three are worth a look. Open any story to read or edit it."

Save what the list was built from as stories/review-list.json in the client's Claude Project (each flagged key with its group, flag, problem and recommendation), so a later run can show the list again. The stories themselves always come fresh from Jira, and a story that is no longer New drops off the list.

**What comes back.** The list sends one message with up to two parts:

- `Changes:` per story, the lines the SC rewrote (user story, description, a criterion by number), criteria removed or added, a recommendation accepted, and a note. Read each story fresh from Jira, change only what the message names, and keep every other word. An accepted recommendation is carried out as it was written on the list (a split creates the new story with its own key and links the two; a Beyond SOW story stays marked and the PM is told that week). A note is an instruction for that story; if it is not clear, ask once. Keep the References block and the Open Questions field in step with what changed. Run the story reviewer once on the changed stories and add anything new as an open question; never hold a story back for it.
- `Reviewed, move to ...:` move each listed story to that status, and set its row on the User stories tab to Reviewed by SC.

Then report in one line per story what changed, with the key, and show the list again with what is still New. When nothing is left on it, say so and name what comes next.

Where no visual can be shown, give the same list as text: the three groups, each flagged story with its problem and recommendation, and ask what to change and which stories are reviewed.
