# Changelog

## 0.1.0 (2026-10-30), first build, not yet released

Skills built from the skill texts embedded in the live Start Motion page (version 1793311819-6881, Oct 30, 2026), one skill per stage command, with these additions on every skill:

- A Start section: the skill reads `references/method.md`, looks before it asks, and reports where the client stands against the stage's readiness list (the "Before you build" checklists on the page become what the command checks on open). A command that finds the client's documents missing offers to set them up right there.
- A one-message intake that works like the page's builder: the slide list (kickoff) and the section list (readout) shown in full with the optional items marked; the person answers once; the skill reads it back in one line, then shows the plan and waits, as the page does. No preset standard set. The readout's two settings (what we heard played back or future state only; dates solid or not) come prefilled from the Discovery documents note and can be changed.
- `references/method.md` per skill: what the stage is for, the checks before you accept, the bar, the calls the skill cannot make, and the link to the stage on the Start Motion page.
- A Next line at the end of every report naming the command that follows.
- The standing lines people used to paste from the page prompts moved into the skill's rules.
- Templates, logos and scripts carried inside each skill: discovery page templates and logos (discovery-plan, discovery-call), the readout template, build script and content example (readout), the kickoff slide templates, manifest, icons, brand files and tokens (kickoff), the Discovery documents note shape (discovery-call).
- The run log row names the plugin version.

- Shared outputs (Avi, Oct 30): the skills keep working out of the SC's Claude Project, and also save three things into the client's Drive folder (the Discovery subfolder, next to the requirements list) as they are written: the Discovery documents note as a Google Doc, every session note, and the readout sign-off record. The discovery call and user stories skills read those Drive copies when the project copy is not there, so anyone on the client can find the outputs.

Commands: `/start-motion:handoff`, `kickoff`, `discovery-plan`, `discovery-call`, `readout`, `design`, `user-stories`.

Known gaps in this build: the kickoff brand folder has no topographic pattern PNGs (they live in the Kicksaw Slides design system; the skill builds without the pattern when it cannot read them). The kickoff icons were regenerated from Font Awesome Free (the same source the design system used), white on transparent, 256 px.
