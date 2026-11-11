# Decisions: the log, the four kinds, and what waits

How the kit records a design or build choice, who makes it, and what keeps moving while it is open. Used by `/start-motion:design`, `/start-motion:build-plan` and `/start-motion:build`. The home of this text is `plugins/start-motion/shared/decisions.md`; the copies in each skill's `references/` are written by `scripts/sync-agents.py`.

The rule behind all of it: anything that does not need a person moves forward, and anything that does is made plain, logged and put in front of the right person in one place. A decision never stops a whole run. Only the work that depends on it waits.

## What goes in the log

A choice goes in the log when a real alternative existed and someone could later ask why we went this way: an object model, a relationship type, standard against custom, configuration against code, how a new automation joins an existing one, an access model, an integration pattern, something retired. It also goes in when the kit's own rules (simple and sound) were set aside for a reason.

Not in the log: names the design or the builder gave, formatting, order of build tasks, anything the SOW or the client already settled word for word with no other way to read it. Those live where they already live.

## Where it lives

The **Decisions** tab of the client's requirements list (the Google Sheet in the client's Drive folder, next to Requirements and Open items). One row per decision. The SC, SA and PM all have it, it is already shared, and the stories and the readout already point at that sheet.

If the tab is missing (older client sheets), add it with the header row below, freeze the header, add dropdowns for Kind and Status, and say so in the report. Where the session cannot reach the sheet (Codex, or Claude Code with no Sheets connector), write the same rows to `docs/decisions.md` in the client's repo, say so, and copy them into the sheet the next time it can be reached. Never keep two live copies on purpose.

Columns, found by header name:

| Column | What goes in it |
|---|---|
| ID | D-01, D-02 and on. Never reused. |
| Decision | The question, in one plain line: "How does a referral link to its referring provider?" |
| Kind | Clear, Recommended, SA call or Client call (below). |
| Status | Proposed, Decided, Superseded or Dropped. |
| Options and trade-offs | Each option on its own line: "A · Lookup to Contact: one record per provider, reportable; providers must be Contacts first." Two or three options. A Clear row may have one line. |
| Recommended | Claude's pick and the reason in one line, or "No lean" with what it turns on. |
| Chosen | The option chosen, or the person's own wording. Empty until decided. |
| Why | Why it was chosen, in a line the client could read. |
| What would change it | The fact that would reopen it ("if providers ever need portal access"). |
| Requirements | The requirement IDs it serves. |
| Affects | The design section, stories and build tasks that depend on it. |
| Raised in | Design (date), Build plan (date), Task E1.2-T1, or the call (S-05). |
| Decided by | A person's name, or "Claude" for a Clear row (see below). |
| Date | The date it was decided. |
| Source | Where the decision was made: "SA in chat, Nov 12", the call and timestamp, a Slack thread, the Open items number for a client call. |
| Superseded by | The ID of the decision that replaced it. |

Internal reasoning (effort, margin, the relationship) stays in this tab. What the client reads is the design's Key decisions section, written from the Chosen and Why columns.

## The four kinds

Sort every logged choice into one of these the moment it comes up. When unsure between two, take the one that involves the person more.

**Clear.** One answer is sound and the rest are not, under the SOW, the org, what the client said, or the kit's simple-and-sound rules (`/start-motion:design` 3b). Claude makes the call, writes the row with Status Decided and Decided by "Claude", and moves on. Nothing waits. The SA sees every Clear row in one short list and can reopen any of them; approving the design accepts the rest, and each is then marked "Claude · accepted by <SA> with the design, <date>".

**Recommended.** More than one answer is sound and Claude has a pick it can defend in one line. Write the row with Status Proposed, the pick in Recommended, Chosen empty. The work goes ahead on the pick: the design is written with it and the section carries a small "Recommended · D-04" marker. It only has to be confirmed before the design goes Final, or before a build task that depends on it is approved.

**SA call.** A real trade-off where a careful architect could go either way (cost against flexibility, a pattern the client will live with for years, how far to bend the org's existing build), or where Claude has no defensible lean. Write the row with Status Proposed and every option's trade-off; put a lean in Recommended if there is one, otherwise "No lean". The design shows that section as Open with the options side by side. Everything that does not depend on it keeps moving.

**Client call.** Only the client can answer (a business rule, a policy, a third party). Write the row and an Open items question for the SC or PM, and put the Open items number in Source. Claude may still write the options and a lean so the SC can ask it well. The dependent work waits exactly as for an SA call. When `/start-motion:discovery-call` or a refinement closes that Open items question, the decision row closes with it.

## What moves and what waits

| | Nothing waits | Waits |
|---|---|---|
| Clear | Everything | Nothing |
| Recommended | Drafting, stories, planning, on the pick | The design going Final; approving a build task that depends on it |
| SA call, Client call | Every section, story and task that does not depend on it | The dependent section (shown Open), stories whose criteria turn on it (open question with the D-ID), build tasks that depend on it (planned but marked "waits on D-07", never built) |

A run never stops because a decision is open. It finishes everything else and ends with the decisions waiting, in one place.

## Putting decisions in front of the person

At the end of a run that leaves rows Proposed (and at build plan approval, for the decisions its tasks depend on), show the decision picker: `references/decision-picker.html`, in Claude chat when an interactive visual can be shown. Change only the `CFG` line at the top of its script; send the rest as it is.

- `client`, `stage` ("Solution design", "Build plan", "Build").
- `calls`: SA calls and Client calls, most consequential first. Each: `id`, `q` (the Decision column), `why` (one line: what it affects and why it matters), `kind` ("SA call" or "Client call"), `opts` (each with `k` (A, B, C), `name`, `pro`, `con`, and `effort` when it differs: "Low", "Medium", "High"), `lean` (the option's `k`, or empty).
- `recs`: Recommended rows, each with `id`, `q`, `pick` (the option name) and `why`.
- `clear`: Clear rows, each with `id`, `q` and `chosen`.

One line above it, for example: "Two calls need you for Harborlight, three recommendations to confirm, and eleven I made. Everything else is drafted." The picker returns the answers as a message; write them straight into the log.

Everywhere else (Cowork, Claude Code, Codex, a chat that cannot show visuals), send this, filled in:

```
Decisions for [Client] · [stage]

Need you (pick one each):
D-07 · [question] ([what it affects])
  A · [name]: [pro]. [con].
  B · [name]: [pro]. [con].
  Lean: B, [one line why]

Confirm (I went ahead on these):
D-04 · [question]: [pick], [why]

Made (reopen any):
D-01 · [question]: [chosen]
D-02 · ...

Answer in one line, for example: "D-07 B, confirm all, reopen D-02".
```

Client calls appear in the picker so the SA can see them, marked "Client call · Q-14 with the SC"; the SA can note a lean, but the row stays Proposed until the client answers.

## Writing the answers back

- A pick, or the person's own wording: Chosen, Decided by (the person's name, from the session or as they gave it), Date, Source ("SA in chat, <date>"), Status Decided. Write Why from the option's trade-off and anything the person said; if they gave no reason, Why is the option's pro line.
- "Confirm": Chosen takes the Recommended pick.
- "Reopen" on a Clear row: it becomes an SA call; write its options and put it in the next picker, or in this run if the person is still here.
- A changed decision is never edited: write a new row, set the old one to Superseded with Superseded by. Then update everything in Affects.
- Then act on it in the same run: update the design section (remove the Open callout, fold the choice in), take the D-ID off the story's open question, mark the build tasks unblocked. Say in one line what changed because of it.

## How the agents use the log

- Agents are handed the **Decided** rows that touch their work, never the Proposed ones and never anyone's reasoning beyond the Why column.
- The builder builds to them. When the task, the design and a Decided row disagree, it stops and says so under Needs a person.
- A reviewer does not flag a choice a Decided row records (a lookup the SA chose over a formula is not "heavier than needed"). It does flag work that contradicts a Decided row, citing the ID, and a choice with a real alternative that no row records, so it gets logged. A Decided row never excuses something that breaks a hard rule: production, deletion, records, a platform or SOW limit.
- When the builder stops for a decision, the stage command writes it as a Proposed row (Raised in: the task), hands back only that task and the ones that depend on it, and carries on with the rest.
