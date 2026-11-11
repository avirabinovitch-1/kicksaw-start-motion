"""Nov 10, 2026: the two review agents (source checker, story reviewer) wired into the stages that start them.

Applied in place to the skills; this script is the record of what changed and why, and re-running it is a no-op
once applied. The agents themselves are in plugins/start-motion/agents/.

Run:  python3 -I scripts/edits_agents_phase1.py
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


START = ("**Starting a reviewer.** Where the session can start a separate agent (Claude Code, Cowork, Codex), start it by name "
         "(`start-motion:source-checker`, `start-motion:story-reviewer`) and hand it only what its file says it is handed: "
         "never this conversation, your notes or your reasoning. Where the session cannot start one (Claude chat often cannot), "
         "read its instructions at `references/reviewers/<name>.md` in this skill's folder and run them yourself as a second pass, "
         "working from the sources and the story text, not from memory of drafting. Say on the report which way each reviewer ran; "
         "a second pass in the same conversation is weaker than a separate reader, and the SC should know which one they got.")


def user_stories(t):
    w = 'user-stories'
    t = rep(t,
            " Before showing the SC anything for an epic, have that epic's stories read cold against the transcripts and the readout for defects only (a separate reviewer agent where one is available, otherwise a second pass of your own from the transcripts, not from memory); reconcile first.",
            " Before showing the SC anything for an epic, run the two reviewers on that epic's stories (\"The two reviewers\" below) and act on what they find.",
            w)
    t = rep(t, "### The title\n",
            "### The two reviewers\n\n"
            "Two reviewers read every story before the SC does. Each has one job and reads the story without having seen it written.\n\n"
            "- **The source checker** opens every quote's call at its timestamp and checks that the quote is there, that the speaker is right, and that the acceptance criteria say what the client said: not more, not less. Hand it the epic's stories (ID, acceptance criteria, each quote with its citation), the tl;dv link for every S-ID the stories cite, the signed readout, and the calls held after each story was drafted.\n"
            "- **The story reviewer** reads each story as the architect and the tester will, with only the story in hand, and reports the criteria that cannot be built or tested as written. Hand it the stories only, plus the list of objects and fields that already exist when the solution design or an org summary has one. Never hand it the requirements list or the transcripts.\n\n"
            + START + "\n\n"
            "What to do with the findings:\n"
            "- Fix what is plainly wrong and what the sources settle: a quote that differs from the transcript is replaced with the transcript's words; a wrong timestamp or speaker is corrected; a criterion with no trigger gets the trigger the client stated; a quote inside the criteria moves to the Description; Given/When/Then is rewritten as plain behavior.\n"
            "- Never settle a finding by guessing. A criterion that is not exact because the client never gave the value becomes an open question on the story and on the Open items tab.\n"
            "- A story the source checker found narrower or broader than what the client said, or contradicted by a later call, is not reworded on your own. Show the SC the row and the source lines side by side; they fix the wording, ask the client, or mark the point as Kicksaw's recommendation so nobody reads it as something the client asked for.\n"
            "- A finding that a story should be split or merged is the SC's call; list it.\n"
            "- Run each reviewer once, fix, and run it once more on the stories that changed. Two passes at most. Whatever is still flagged goes to the SC as it is.\n"
            "- When you show the SC a story, show its open findings under it, each in one line. A story with none says \"Both reviewers passed\".\n\n"
            "### The title\n", w)
    t = rep(t, "Read the issue back to confirm the custom fields landed.",
            "A story the SC edited after the reviewers ran goes through the story reviewer once more before it is created; a finding goes back to the SC, not into Jira. Read the issue back to confirm the custom fields landed.", w)
    t = rep(t, "Then a short list of every story waiting for review. After a refinement,",
            "Then a short list of every story waiting for review, each with the reviewers' findings still open on it, and one line on how the reviewers ran (as separate agents, or as a second pass in this conversation). After a refinement,", w)
    return t


def discovery_call(t):
    w = 'discovery-call'
    t = rep(t, "## 5. Prep the next session\n",
            "## 4b. Check what was written\n\n"
            "After the documents are written and before the report, two reviewers read what this call added or changed. Each has one job and reads the work without having seen it written.\n\n"
            "- **The source checker** opens each cited call at its timestamp and checks that the quote is there, that the speaker is right, and that the requirement says what the client said: not more, not less. Hand it the requirement rows this run added or changed (ID, statement, each quote with its citation) and the stories drafted or changed from them (ID, acceptance criteria, quotes), the tl;dv link for each S-ID those rows cite, and any client email or document they cite. When a row changed because of this call, hand it the earlier call too.\n"
            "- **The story reviewer** reads each story this run drafted or changed as the architect and the tester will, with only the story in hand. Hand it the stories only. Never hand it the requirements list or the transcript.\n\n"
            + START + "\n\n"
            "What to do with the findings:\n"
            "- Fix what is plainly wrong and what the transcript settles, in the rows and stories this run wrote: a quote that differs from the transcript is replaced with the transcript's words; a wrong timestamp or speaker is corrected; a criterion with no trigger gets the trigger the client stated; a quote inside the criteria moves to the Description.\n"
            "- Never settle a finding by guessing. A criterion that is not exact because the client did not give the value becomes an open question on the story and on the Open items tab.\n"
            "- A requirement the source checker found narrower or broader than what the client said is not reworded on your own. It goes on the report for the SC with the row and the source lines side by side. The SC fixes the wording, asks the client, or marks the point as Kicksaw's recommendation.\n"
            "- A row the source checker found contradicted by another call is a conflict: handle it as step 3 says (Status to Conflict, both quotes, a blocking open item).\n"
            "- A row or story the SC has already edited or reviewed is never changed on a reviewer's finding. List the finding for the SC.\n"
            "- Run each reviewer once, fix, and run it once more on what changed. Two passes at most. Whatever is still flagged goes on the report as it is.\n"
            "- A call with nothing new to check (no rows added or changed) skips this step; say so in one clause on the report.\n\n"
            "## 5. Prep the next session\n", w)
    t = rep(t, "every session suggestion, any column or value step 0 added or renamed on the sheet, and the sign-off check if anything is at risk.",
            "every session suggestion, every reviewer finding from step 4b that needs the SC (the row or story ID, the verdict, and the source line in the `detail`), any column or value step 0 added or renamed on the sheet, and the sign-off check if anything is at risk.", w)
    t = rep(t, "Then the rows in Conflict, the Beyond SOW rows whose Scope decision is still empty, the session suggestions, and any column or value step 0 added or renamed on the sheet.",
            "Then the rows in Conflict, the Beyond SOW rows whose Scope decision is still empty, the session suggestions, the reviewer findings from step 4b that need the SC (each with the row or story ID, the verdict and the source lines), one line on how the reviewers ran (as separate agents, or as a second pass in this conversation), and any column or value step 0 added or renamed on the sheet.", w)
    return t


def main():
    for skill, fn in (('user-stories', user_stories), ('discovery-call', discovery_call)):
        path = os.path.join(SKILLS, skill, 'SKILL.md')
        old = open(path, encoding='utf-8').read()
        new = fn(old)
        if new != old:
            open(path, 'w', encoding='utf-8').write(new)
            print('edited: ' + skill)
        else:
            print('already applied: ' + skill)


if __name__ == '__main__':
    main()
