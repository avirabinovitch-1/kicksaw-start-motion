"""Copies each agent's instructions into the skills that start it, and the shared texts (plugins/start-motion/shared/) into the skills that use them.

Why: the agents live in plugins/start-motion/agents/, which Claude Code, Cowork and Codex load as separate agents.
Claude chat cannot always start a separate agent, and a skill can only count on reading its own folder. So every
skill that starts an agent carries a copy of that agent's instructions at references/agents/<agent>.md, and runs
it as a second pass when no separate agent is available. The agents folder is the home of the text; the copies are
written by this script and never edited by hand.

Run:    python3 -I scripts/sync-agents.py          writes the copies
Check:  python3 -I scripts/sync-agents.py --check  exits 1 if a copy is missing or out of date
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, 'plugins', 'start-motion')
AGENTS = os.path.join(PLUGIN, 'agents')
SKILLS = os.path.join(PLUGIN, 'skills')

# which skill starts which agent
STARTS = {
    'discovery-call': ['source-checker', 'story-reviewer'],
    'user-stories': ['source-checker', 'story-reviewer'],
    'design': ['org-reader', 'design-reviewer'],
    'build-plan': ['org-reader', 'story-reviewer'],
    'build': ['builder', 'story-compliance-reviewer', 'salesforce-quality-reviewer', 'test-writer'],
}

# shared texts every skill in the list carries a copy of, at references/<file>
SHARED_DIR = os.path.join(PLUGIN, 'shared')
SHARED = {  # file -> [(skill, folder inside the skill)]
    'decisions.md': [('design', 'references'), ('build-plan', 'references'), ('build', 'references')],
    'decision-picker.html': [('design', 'references'), ('build-plan', 'references'), ('build', 'references')],
    'mode-picker.html': [('build-plan', 'references'), ('build', 'references')],
    'working-mode.md': [('build-plan', 'references'), ('build', 'references')],
    'build-review.md': [('design', 'references'), ('build-plan', 'references'), ('build', 'references')],
    'build-review.py': [('build-plan', 'scripts'), ('build', 'scripts')],
    'drive-copies.md': [('design', 'references'), ('build-plan', 'references'), ('build', 'references'),
                        ('readout', 'references'), ('user-stories', 'references')],
}
SHARED_NOTE = {
    '.md': '<!-- Copy of plugins/start-motion/shared/%s, written by scripts/sync-agents.py. Do not edit here. -->\n\n',
    '.py': '# Copy of plugins/start-motion/shared/%s, written by scripts/sync-agents.py. Do not edit here.\n',
}

NOTE = ('<!-- Copy of plugins/start-motion/agents/%s.md, written by scripts/sync-agents.py. Do not edit here. '
        'This copy is for sessions that cannot start a separate agent: read it and run it as a second pass. -->\n\n')


def body(agent):
    path = os.path.join(AGENTS, agent + '.md')
    if not os.path.exists(path):
        return None
    text = open(path, encoding='utf-8').read()
    if not text.startswith('---\n'):
        sys.exit('%s: no frontmatter' % path)
    end = text.index('\n---\n', 4)
    return NOTE % agent + text[end + 5:].lstrip('\n')


def main():
    check = '--check' in sys.argv
    stale, written, skipped = [], [], []
    for skill, agents in sorted(STARTS.items()):
        if not os.path.isdir(os.path.join(SKILLS, skill)):
            skipped.append(skill)
            continue
        for agent in agents:
            want = body(agent)
            if want is None:
                skipped.append('%s (agent %s not written yet)' % (skill, agent))
                continue
            dest = os.path.join(SKILLS, skill, 'references', 'agents', agent + '.md')
            have = open(dest, encoding='utf-8').read() if os.path.exists(dest) else None
            if have == want:
                continue
            if check:
                stale.append(os.path.relpath(dest, ROOT))
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                open(dest, 'w', encoding='utf-8').write(want)
                written.append(os.path.relpath(dest, ROOT))
    for name, skills in sorted(SHARED.items()):
        src = os.path.join(SHARED_DIR, name)
        if not os.path.exists(src):
            skipped.append('shared %s (not written yet)' % name)
            continue
        text = open(src, encoding='utf-8').read()
        head = SHARED_NOTE.get(os.path.splitext(name)[1])
        want = (head % name if head else '') + text
        for skill, folder in skills:
            if not os.path.isdir(os.path.join(SKILLS, skill)):
                skipped.append(skill)
                continue
            dest = os.path.join(SKILLS, skill, folder, name)
            have = open(dest, encoding='utf-8').read() if os.path.exists(dest) else None
            if have == want:
                continue
            if check:
                stale.append(os.path.relpath(dest, ROOT))
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                open(dest, 'w', encoding='utf-8').write(want)
                written.append(os.path.relpath(dest, ROOT))
    for s in skipped:
        print('skipped: ' + s)
    for w in written:
        print('wrote: ' + w)
    if stale:
        print('out of date:\n  ' + '\n  '.join(stale))
        sys.exit(1)
    print('copies in step' if check else 'done')


if __name__ == '__main__':
    main()
