# The design content file

The design is kept as one JSON file, `design-content.json`, and the page is built from it by `scripts/build-design.py` with `templates/Kicksaw Solution Design.template.html`. You write and change the content file. You never write the page's HTML by hand, and an update changes only the sections it touches.

`references/design-content-example.json` is a complete example (Harborlight, a made-up client). Read it before writing your first one.

Where it lives: next to the design in the client's Drive folder, `Design` subfolder, as `[Client] Design content v0.3.json`, saved with every version the same way as the page (`references/drive-copies.md`). Each run downloads the current one, changes it, builds the page and saves both.

## Top level

| Field | What goes in it |
|---|---|
| `client` | The client's name |
| `title` | What is being built, as the page's heading: "Harborlight Access Center" |
| `platform` | "Salesforce Health Cloud and Experience Cloud" |
| `subtitle` | Optional, one line |
| `architect` | The SA's name |
| `date`, `version`, `status` | "Nov 11, 2026", "v0.1", and "Draft" or "Final" |
| `approved` | Empty until the SA approves the draft; then "Steph McAllister, Nov 12, 2026" |
| `review_link` | The design and build review page, once a build plan exists; otherwise empty |
| `changed` | What this version changed because of the SA's answers, one plain line each. Empty on a first draft. The page shows it at the top |
| `sections` | The sections, in order (below) |
| `decisions` | The decisions, copied from the Decisions tab (below) |
| `log` | The change log: `["v0.2", "Nov 12, 2026", "what changed"]`, one per version |

## Sections

Each section: `id` (lower-case letters, digits and hyphens: `data-model`, `intake`), `num` ("1", "2.1"), `title`, and `html`, the section's content.

`html` is plain content only: `<p>`, `<ol>`, `<ul>`, `<table>` inside `<div class="tw">`, `<h3>`, `<code>` for API names, `<span class="who">` for the actor at the start of a flow step, `<span class="tbd">TBD · what it waits on</span>`, `<div class="callout"><b>Dependency</b> ...</div>`, and a diagram as inline SVG inside `<div class="erd">` (the data model) or `<div class="fig">`. No styles, no scripts, no layout.

Mark where a decision shaped the text with `{{D-04}}`, right after the sentence or row it shaped. The page turns it into the right label: "Written on Claude's pick · D-04" while it is open, "Decided · D-04" once it is. Write the sentence itself on the option in force: the SA's choice when decided, your pick when not.

Set `"rewritten": true` on a section this version rewrote because of the SA's answers, and clear it on the next version.

Three sections are written by the page from the data and have no `html`. Give each an `id`, `num`, `title` and `auto`:

- `"auto": "key-decisions"`: every decided choice in a line the client can read, then what is still open and with whom.
- `"auto": "claude-calls"`: the calls Claude made on its own, each with Reopen. Left out of a Final design.
- `"auto": "change-log"`.

## Decisions

One entry per row of the Decisions tab that this design raised or depends on. The tab is the record; this is its copy for the page. Keep the two in step in the same run.

| Field | What goes in it |
|---|---|
| `id` | The D-ID from the tab |
| `kind` | `sa` (SA call), `recommended`, `client` (client call) or `clear` (a call Claude made) |
| `status` | `open`, `decided`, `parked` (the SA asked for more first) or `dropped` (no longer applies after another decision) |
| `structural` | true for a choice most of the design is built on: how a person or an account is modeled, what the main record is, the access model, an integration pattern several capabilities share. These sit in the data model section and are answered first; every other decision is locked until they are |
| `section` | The `id` of the section the decision sits in. Its card is shown at the end of that section. Not needed for `clear` |
| `depends_on` | Another decision's ID, when this one only makes sense once that one is decided. It stays locked until then |
| `q`, `ask`, `why` | A short title; the question in one plain sentence, as you would ask it across a table; what it holds up |
| `said`, `today`, `reqs` | The client's own words with speaker, call and timestamp; what the org has now; the requirement IDs and statements. Leave out what you cannot point to |
| `shapes` | The titles of the sections that change if the answer changes |
| `opts` | For `sa`: two or three options, each `k` (A, B, C), `name`, `sum`, `gain`, `cost`, `risk`, `builds` (a list), `undo`, `effort`. Fill the same rows for every option |
| `lean`, `lean_why`, `change_if` | The option you pick and why in one sentence, and what would change it. `lean` empty means no lean; then `lean_why` says what it turns on |
| `pick`, `alt` | For `recommended`: what you went ahead on (with `why`), and the other way in a clause |
| `ref` | For `client`: the Open items number and who is asking ("Q-21, with the SC to ask Kim Tanaka") |
| `chosen`, `why_chosen`, `by` | Once decided: what was chosen, why in a line the client could read, and who decided ("Steph McAllister, Nov 12" or "Claude") |
| `parked_for` | When parked: what the SA asked for |

Every fact in a decision comes from somewhere the SA could check. Never write an option, a risk or a quote you cannot point to.

## Building the page

```
python3 -I scripts/build-design.py --template "templates/Kicksaw Solution Design.template.html" \
    --content design-content.json --out "<Client> Solution Design v0.1.html"
```

It prints a CHECK line for each problem (a marker for a decision that does not exist, a decision whose section is missing, an SA call with one option, Final with a decision still open, an em dash) and a NOTE with the counts. Fix every CHECK in the content file and build again. Then save and publish as `references/drive-copies.md` sets out.

## What the SA does in the page, and what comes back

The bar at the top counts what is answered and has one marker per decision. Next decision goes to the next one. The SA picks an option, writes their own, asks for more first, confirms or changes a recommendation, reopens a call Claude made, and can comment on any section. Send to Claude shows one message to copy into the chat:

```
Decisions for Harborlight Behavioral Health · Solution design v0.1. Write these to the Decisions tab, rewrite the sections they touch, save the next version and tell me what changed.
D-01: A (Person Accounts) · why: Health Cloud needs it
D-02: B (A Lead that converts)
D-04: need more first: ask Tom whether the fax mailbox can forward
D-05: confirm
D-07: change: show the program name as well
Reopen D-12: we may need it stored for the County export
Comment on 2.1 Referral intake: phone referrals need a quick create too
```

When that message arrives, in one run:

1. Write each answer to the Decisions tab as `references/decisions.md` sets out ("Writing the answers back").
2. In the content file: set each decision's `status`, `chosen`, `why_chosen` and `by`; a "need more first" becomes `parked` with `parked_for`; a reopened call becomes an `sa` decision with its options, `open`, in the section it belongs to; a decision that no longer applies becomes `dropped`.
3. Rewrite only the sections the answers touch (each decision's `shapes`, and any section with a comment) and set `rewritten` on them. Where the SA chose your pick, nothing is rewritten.
4. Fill `changed` with one line per answer, saying what it changed or that nothing needed rewriting, and how many decisions are open now.
5. Bump the version, add the `log` line, build, save to Drive and republish to the same link.
6. Reply in the chat with the same lines as `changed` and the link.

An approval message ("Approve the Harborlight Behavioral Health solution design v0.3. Accept the calls Claude made with it.") sets `approved`, marks each Clear row on the tab "Claude · accepted by <SA> with the design, <date>", and saves the version.
