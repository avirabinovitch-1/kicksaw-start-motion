"""Nov 10, 2026: the design stage starts from the org and has its design checked (org reader, design reviewer).

Applied in place to the design skill; this script is the record of what changed and why, and re-running it is a
no-op once applied. The agents are in plugins/start-motion/agents/. The build-plan and build skills are new files.

Run:  python3 -I scripts/edits_agents_phase2.py
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'plugins', 'start-motion', 'skills')


def rep(text, old, new, where=''):
    """Replace exactly one occurrence. Already applied (new present) is fine; anything else stops."""
    if new in text:
        return text
    n = text.count(old)
    if n == 1:
        return text.replace(old, new)
    sys.exit('%s: anchor found %d times, expected 1:\n%s' % (where, n, old[:140]))


def design(t):
    w = 'design'
    t = rep(t, "- The current org, if the client already runs Salesforce: objects and fields already in use.\n",
            "- The current org, when the client has one (an existing org, or a sandbox the team has started building in): the org summary at `docs/org-summary.md` in the client's repo, with a copy in the client's Drive folder. It lists the objects, fields, automation, access and pages that already exist, by their real names. When there is no summary, or the org has changed since it was written, get one first (\"Start from the org\" below).\n", w)
    t = rep(t, "## 1. Propose the sections\n",
            "### Start from the org\n\n"
            "A design written from the requirements alone can name a new field where one already exists, or miss automation the new build will collide with. So when the client has an org, the design starts from what is in it.\n\n"
            "- Where the session has a terminal with the Salesforce CLI signed in to the org and the client's repo on this computer (Claude Code, Cowork with the repo folder connected, Codex), start the org reader: `start-motion:org-reader`. Hand it the client's name, the org's alias, the repo path, the SOW's countable limits (custom fields per object and the like) and the date of the last summary. It pulls the org's configuration into the repo on its own branch and writes `docs/org-summary.md`. It reads configuration only, never records, and changes nothing in the org.\n"
            "- Save a copy of the summary to the client's Drive folder so the SC and PM can read it.\n"
            "- In Claude chat with no terminal, the org cannot be read from here. Use the summary in the client's folder if there is one and say its date; if there is none, say the design is being drafted without a read of the org, and mark every object and field it names as \"to check against the org\".\n"
            "- Name existing objects, fields and picklist values exactly as the summary has them, and say plainly what is new. Where the design adds automation to an object that already has some, say how the two will work together.\n\n"
            "## 1. Propose the sections\n", w)
    t = rep(t, "## 5. Keep it current\n",
            "## 4b. Have the design checked\n\n"
            "After a first draft, after an update that changes more than a TBD, and always before getting it ready to share, start the design reviewer: `start-motion:design-reviewer`. It did not see the design being drafted. Hand it the design as it stands; the requirements in scope (ID, statement, status, Scope), saying whether the scope is signed yet; the user stories when they exist; and the org summary when there is one. Never hand it the transcripts or your notes.\n\n"
            "Where the session cannot start a separate agent (Claude chat often cannot), read `references/reviewers/design-reviewer.md` in this skill's folder and run it yourself as a second pass, working from the requirements list and the org summary, not from memory of drafting. Say in the report which way it ran; a second pass in the same conversation is weaker than a separate reader.\n\n"
            "What to do with the findings:\n"
            "- An uncovered requirement: add it to the section it belongs in when the discovery documents say how it is met; otherwise add it as a TBD with what it waits on. Never design around a gap with an assumption.\n"
            "- A conflict with the org where the summary settles it (a field that already exists, a name spelled differently): correct the design to the org's name. A conflict that needs a decision (two automations on one object, an access model that changes) goes to the SA as an Open callout in that section.\n"
            "- Something designed beyond the confirmed scope: mark it in the design and list it for the SA. The SA takes it out or raises it with the PM. Do not remove it on your own.\n"
            "- An unconfirmed detail: mark it TBD with what it waits on.\n"
            "- Run the reviewer once, fix, and run it once more. Two passes at most. Whatever is still flagged goes to the SA as it is.\n\n"
            "## 5. Keep it current\n", w)
    t = rep(t, "Three short paragraphs: what the design covers and how it is organized, what is still TBD and who answers each one, and what the SA should check. No recap of steps.",
            "Three short paragraphs: what the design covers and how it is organized, what is still TBD and who answers each one, and what the SA should check. Then the design reviewer's findings that are still open, each in one line (uncovered requirements by ID, conflicts with the org, anything beyond scope), the date of the org summary the design was written against (or that there was none), and one line on how the reviewer ran. No recap of steps.", w)
    t = rep(t, "once it is shared, `/start-motion:user-stories` writes the stories with the design in hand.",
            "once it is shared, `/start-motion:user-stories` writes the stories with the design in hand; once the stories are refined and the SA has approved the design, `/start-motion:build-plan` turns them into build tasks.", w)
    return t


def main():
    path = os.path.join(SKILLS, 'design', 'SKILL.md')
    old = open(path, encoding='utf-8').read()
    new = design(old)
    if new != old:
        open(path, 'w', encoding='utf-8').write(new)
        print('edited: design')
    else:
        print('already applied: design')


if __name__ == '__main__':
    main()
