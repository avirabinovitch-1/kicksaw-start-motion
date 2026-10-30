"""Oct 30, 2026 edits, applied in place to the skills (the repo is the home of the skill text since Oct 30; this
script is the record of what changed and why, and re-running it is a no-op once applied).

Two things, from Avi's decisions of Oct 30:
1. The reading rule. Delivery can count on the signed SOW and whatever else is in the client's Drive folder,
   nothing more. No skill names a sales calls subfolder ("01. Sales Handoff" came off a real client folder);
   the skills read the whole client folder, every subfolder included, and nothing beyond the SOW is reported
   as a gap: it is the normal case.
2. The handoff stage is optional: it runs when sales shares a packet beyond the SOW, nothing downstream
   waits for it, and a folder holding only the SOW is "nothing to hand off".

Run:  python3 -I scripts/edits_0_2_0.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'plugins', 'start-motion', 'skills')
PAGE = 'https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S'
METHOD_LINE = "Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page."


def rep(text, old, new, where=''):
    """Replace exactly one occurrence. Already applied (old absent, new present) is fine; anything else stops."""
    if new in text:
        return text
    n = text.count(old)
    if n == 1:
        return text.replace(old, new)
    sys.exit('%s: anchor found %d times, expected 1:\n%s' % (where, n, old[:140]))


# ---------------------------------------------------------------- 1 and 2: the seven skills
def handoff(t):
    w = 'handoff'
    t = rep(t, 'or shares a sales handoff folder.\n---', 'or shares a sales handoff folder. This stage is optional: it runs when sales shares a packet beyond the SOW, and nothing downstream waits for it.\n---', w)
    t = rep(t, 'This skill covers three moves that are three separate prompts on the page: building the handoff document (sales),',
            'This stage is optional. Delivery cannot count on more than the signed SOW and whatever else sales shares into the client\'s folder; `/start-motion:new-client` starts a client from the SOW without any of this, and no later stage waits for a handoff. The stage is here so the process is visible and sales can adopt it; when a packet beyond the SOW arrives, this is how it is handled.\n\nThis skill covers three moves that are three separate prompts on the page: building the handoff document (sales),', w)
    t = rep(t, 'it sets the client up and names the stage to run next.\n',
            'it sets the client up and names the stage to run next.\n\nWhen the folder holds nothing beyond the SOW (no transcripts, no contracts past the SOW itself, no IKT, no client documents), say so in one line and stop: "Tog. Only the SOW in the folder; nothing to hand off yet. `/start-motion:new-client` starts from the SOW." A handoff document that restates the SOW is not worth anyone\'s reading time, and nothing downstream is waiting for it.\n', w)
    t = rep(t, '1. The client\'s handoff folder, if sales shared one: transcripts, signed SOW, contracts.\n2. The client\'s Google Drive folder ("01. Sales Handoff" subfolder when it exists).',
            '1. The client\'s Google Drive folder and everything in it, every subfolder included: the signed SOW, and whatever sales shared (transcripts, contracts, a handoff doc). Subfolder names vary by client; read them all rather than looking for one by name.\n2. A separate handoff folder, if sales shared one outside the client\'s folder.', w)
    t = rep(t, 'No sales call transcripts is not a stop. Build the document from the SOW, the contracts, the Closed Won record and anything else in the folder.',
            'No sales call transcripts is not a stop, as long as there is something beyond the SOW to hand off (contracts, an IKT, the deal\'s Slack thread, client documents). Build the document from the SOW, the contracts, the Closed Won record and anything else in the folder.', w)
    t = rep(t, 'Save the doc as a Google Doc in the client\'s Drive folder ("01. Sales Handoff" when it exists) unless the team asks for another format.',
            'Save the doc as a Google Doc in the client\'s Drive folder, in the Discovery subfolder (or the Engagement docs subfolder when that is the one the client folder has; never at the top level), unless the team asks for another format.', w)
    t = rep(t, 'if it does not, tell the PM it needs creating.', 'if there is no project, add the call to the Discovery documents Google Doc in the client\'s Drive folder instead.', w)
    t = rep(t, 'the sales call transcripts (how many, in which folder, named by date and call or not, and any recording with no transcript)',
            'the sales call transcripts (how many, named by date and call or not, and any recording with no transcript)', w)
    t = rep(t, 'Transcripts: three Chorus exports in 02 Sales calls, one MP4 with no transcript.', 'Transcripts: three Chorus exports, one MP4 with no transcript.', w)
    t = rep(t, 'the client\'s handoff folder when none turns up under the client\'s name, the transcript', 'the client\'s Drive folder, only when none turns up under the client\'s name, the transcript', w)
    return t


def kickoff(t):
    w = 'kickoff'
    t = rep(t, 'filling them from the SOW, the handoff packet and the sales calls, with real headshots',
            'filling them from the SOW and whatever else is in the client\'s folder (sales calls, a handoff packet, client documents), with real headshots', w)
    t = rep(t, 'the signed SOW (found, and its date); the handoff packet (found or none); the Kicksaw team',
            'the signed SOW (found, and its date); what else is in the client\'s folder beyond the SOW (transcripts, a handoff doc, client documents, in one clause; nothing beyond the SOW is not a gap, it is the normal case); the Kicksaw team', w)
    t = rep(t, 'Signed SOW: found (Oct 3). Handoff packet: none. Kicksaw team:', 'Signed SOW: found (Oct 3). Beyond the SOW: three transcripts, no handoff doc. Kicksaw team:', w)
    t = rep(t, 'then the handoff packet if there is one (the client\'s Drive folder, "01. Sales Handoff" when it exists), the Notion Closed Won task, any client documents in the folder, and the client\'s Claude Project.',
            'then everything else in the client\'s Drive folder, every subfolder included (sales call transcripts, a handoff packet if sales shared one, client documents; subfolder names vary by client), the Notion Closed Won task, and the client\'s Claude Project.', w)
    t = rep(t, 'The handoff packet gives enough real understanding to play back', 'The sales calls and anything else in the folder give enough real understanding to play back', w)
    t = rep(t, '- **The handoff packet or SOW,** attached or linked.', '- **The SOW,** attached or linked, with or without anything else from the folder.', w)
    return t


def discovery_plan(t):
    w = 'discovery-plan'
    t = rep(t, 'from the SOW and every sales and pre-kickoff call, and prep the SC before each session.',
            'from the SOW and whatever else is in the client\'s folder (sales and pre-kickoff calls, a handoff doc, client documents), and prep the SC before each session.', w)
    t = rep(t, 'the sales and pre-kickoff calls (how many, which have transcripts, which do not); the handoff doc or IKT (found or none); client documents in the folder; whether',
            'everything else in the client\'s folder, every subfolder included (calls with transcripts and without, a handoff doc or IKT, client documents: what is there, in one clause; nothing beyond the SOW is not a gap, it is the normal case); whether', w)
    t = rep(t, 'Calls: four shared by sales, three with transcripts, one MP4 with no transcript. Handoff doc: none. Discovery documents:',
            'Beyond the SOW: four calls, three with transcripts, one MP4 without; no handoff doc. Discovery documents:', w)
    t = rep(t, 'build the plan from the SOW and whatever else is there, and list what was missing in `builtFrom`.',
            'build the plan from the SOW and whatever else is there, and list in `builtFrom` what was read; nothing beyond the SOW is a fact in the report, not a gap.', w)
    return t


def discovery_call(t):
    w = 'discovery-call'
    t = rep(t, 'When someone says "set up the discovery documents for [Client]" (usually with the SOW, and the handoff packet when there is one), make the client\'s copies of the templates. The SOW is the one input setup needs.',
            'When someone says "set up the discovery documents for [Client]" (usually with the SOW, and whatever else is in the client\'s folder), make the client\'s copies of the templates. This is the same routine `/start-motion:new-client` runs as the first command on a new client; when this skill finds the documents missing, offer setup here. The SOW is the one input setup needs.', w)
    t = rep(t, 'Run `/start-motion:discovery-plan` ("plan discovery for [Client]") with the SOW and the sales calls.',
            'Run `/start-motion:discovery-plan` ("plan discovery for [Client]") with the SOW and whatever else is in the folder.', w)
    t = rep(t, '(the discovery plan, the requirements list, the workflow document, What we heard, the SOW and handoff packet, the sales and pre-kickoff calls, and the session notes',
            '(the discovery plan, the requirements list, the workflow document, What we heard, the SOW and anything else shared, the sales and pre-kickoff calls, and the session notes', w)
    return t


def no_change(t):
    return t


SKILL_EDITS = {'handoff': handoff, 'kickoff': kickoff, 'discovery-plan': discovery_plan, 'discovery-call': discovery_call,
               'readout': no_change, 'design': no_change, 'user-stories': no_change}

# reference files (static, in place)
def handoff_method(t):
    return rep(t, '# SOW and handoff: what this stage is for\n\n',
               '# SOW and handoff: what this stage is for\n\nThis stage is optional. Delivery cannot count on more than the signed SOW and whatever files sales shares, so nothing downstream waits for a handoff; `/start-motion:new-client` starts a client from the SOW alone. The stage is here so the process is visible and sales can adopt it. When a packet beyond the SOW arrives, this is the standard for handling it.\n\n', 'handoff/method')

def plan_method(t):
    return rep(t, '- What do we already know? Read the SOW and the sales calls before planning anything',
               '- What do we already know? Read the SOW and whatever else was shared before planning anything', 'discovery-plan/method')

def note(t):
    t = rep(t, '| SOW and handoff packet | [Drive link] | From sales |', '| SOW, and anything else shared | [Drive link] | From sales, through the client\'s folder |', 'note')
    return t

REF_EDITS = {
    'handoff/references/method.md': handoff_method,
    'discovery-plan/references/method.md': plan_method,
    'discovery-call/references/discovery-documents-note.md': note,
}



def apply_all(write=True):
    out = {}
    for cmd, fn in SKILL_EDITS.items():
        p = os.path.join(SKILLS, cmd, 'SKILL.md')
        t = fn(open(p, encoding='utf-8').read())
        if '\u2014' in t:
            sys.exit('em dash in ' + cmd)
        out[cmd] = t
        if write:
            open(p, 'w', encoding='utf-8').write(t)
    for rel, fn in REF_EDITS.items():
        p = os.path.join(SKILLS, rel)
        t = fn(open(p, encoding='utf-8').read())
        if write:
            open(p, 'w', encoding='utf-8').write(t)
    return out


if __name__ == '__main__':
    for cmd, t in apply_all().items():
        print('%-15s %6d bytes' % (cmd, len(t)))
