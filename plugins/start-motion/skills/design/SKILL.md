---
name: design
description: Start Motion stage 5 (/start-motion:design). Drafts, updates and finalizes a Kicksaw solution design document: the data and object model, one section per capability or integration, security and access, reporting, and the diagrams needed. Written for the SA from the SOW and the discovery documents, finalized once the client has confirmed scope. Use whenever someone says "start the solution design for [client]", "update the design", or "get the design ready to share".
---

# Kicksaw solution design

The design shows how we will build the solution in Salesforce, capability by capability. It is written for the delivery team and shareable with the client. It is not a scope recap: the readout covers what and why; the design covers how. The SA owns it; Claude drafts and keeps it current.

Reference examples, by Steph McAllister: the Crossroads Treatment Centers Solution Design (https://claude.ai/artifact/E45dBFHcyYyk8R3Pxnw1pw), organized by integration, and the Healthcare Legal Solutions Client Portal Solution Design (https://claude.ai/artifact/Gdit1JR6FzURLvhq67jqAm), organized by capability. Match their structure, depth and look, not their content.

## Start: where the design stands

Read `references/method.md` in this skill's folder at the start of every run: what the stage is for, the calls the stage asks you to make, the bar, and the link to the full method on the Start Motion page.

This skill covers three moves that are three separate prompts on the page: starting the draft, keeping it current from calls and decisions, and getting it ready to share once scope is signed. Work out which one is next from what exists, and propose it.

Look before you ask. The client's name comes from the request; if it is missing, that is the one thing to ask before looking anywhere. Then report what you found against the stage's readiness list, in a few lines, before doing anything else: the signed SOW; the discovery documents (current to which call; the Integrations and Open items tabs; the data list if there is one); the readout (none, draft at which version, or signed on which date); the current org (access or not, when the client already runs Salesforce); third-party contacts and any access worksheet or data dictionary; and whether a design already exists (then its status, Draft or Final, and the TBDs still open). For example: "Tog. SOW found. Discovery documents current to S-09. Readout v1.1, not yet signed. Org: client runs Salesforce, access not granted. Design: draft started Nov 18, 14 TBDs open, 3 answered on calls since. Next: fold in the calls since Nov 18."

## What to ask: one message

Ask once, in one message, and only for what the Start did not find. Starting the draft needs nothing beyond the client; organized by capability or by integration is proposed in the section plan (section 1), not asked. Updating needs nothing; the calls since the last update are read. Getting it ready to share needs the readout version that was signed, if readout/sign-off.md does not say.

Then read back what you heard in one line and run.

## 0. Load what you need

From the client's Claude Project and the places it links:
- The signed SOW: confirmed architecture decisions and the section numbers to cite.
- The discovery documents: the requirements list (with its Integrations and Open items tabs), the workflows, the session notes and their build notes, and the data and migration list when the project has one.
- The readout as it stands: recommended build, scope in and set aside, open decisions.
- The current org, if the client already runs Salesforce: objects and fields already in use.
- Any access worksheet or data dictionary.

If the SOW, the requirements list or the workflows are missing, say which and stop. A missing data list is not a reason to stop; say the design has no data section to draw on. Never design from memory or from raw transcripts.

## 1. Propose the sections

Before writing, reply with a one-screen plan and wait for the SA:
- Organized by capability or by integration, and why.
- The capability or integration sections, in order, each with the SOW section it comes from.
- The optional sections in or out, with the reason: building on an existing build, users and licensing, prototype screens.
- The diagrams each section needs.
- What is still TBD and what each one waits on.

## 2. The sections

Always in:
1. How to read this document. One paragraph on what the document is and is not; a current state to target state strip of three to five rows; a "what this covers" list with a link to each section.
2. Data and object model. A short lede, then a table: Object, API name, Relationship, Populated by (or Portal access and How access is granted for external users), Notes. Then the ERD.
3. One section per capability or integration (see step 3).
4. Security and access model. Who sees what, drawn for each kind of user when there are external users, then a table by layer: Layer, Salesforce feature, What it does for [client]. Cover org-wide defaults, record access, hierarchy, and object and field access.
5. Reporting and dashboards. Table: Component, Audience, Details, naming the objects and field API names behind each metric and any formula still to confirm. Then what is out of scope for reporting.
6. Diagrams needed. Each diagram, the section it belongs to, and where it lives.

Add when it fits:
- Building on an existing build: when this phase extends a foundation build. What it reads from that build and what can start before it is live.
- Users and licensing: when licence type or user counts shape the design.
- Prototype screens: when there is UI the client will react to.

## 3. Write each capability section

Four parts, in this order:
1. Lede: two or three lines on what it does, citing the SOW section that puts it in scope.
2. Flow: numbered steps, each with its actor (client, agent, system, or the integrated system) and what the step produces. Dashed for steps not decided yet.
3. Spec: an Element and Spec table. For an integration: trigger, direction and pattern, fields exchanged, fallback. For a new object: label and API name, record name format, record types, statuses, relationships, ownership.
4. Terms and callouts: a "What it means for [client]" table for every Salesforce term in the section, then callouts as needed: Recommendation (with the reason and what would change it), Dependency, Open, Note.

## 4. Render

- One HTML artifact on the Kicksaw design system (list Design System artifacts; colors from the Kicksaw Brand Playbook V2). Header: "Solution design · [platform]", the client, a one-line subtitle, prepared by the SA, the date, and a status: "Draft" until scope is confirmed, then "Final".
- Contents on the side with every section linked; numbered sections; tables over prose.
- Real API names in code style. TBD as a small chip wherever a detail waits on something, with what it waits on.
- Diagrams: draw flows in the document as numbered steps. When the SA draws a diagram by hand in Lucid, embed or link it and caption it. A diagram that also appears in the readout is identical in both.

## 5. Keep it current

When asked ("update the [Client] solution design from today's call"): read the call, fold in what was decided, close the TBDs it answered with the date and source, and add new TBDs. Keep the document's tone, structure and look; add to it, never restyle it. List what changed.

## 6. Get it ready to share

When asked ("get the [Client] design ready to share"), once the client has confirmed scope:
- Check every section against the confirmed scope. Anything set aside comes out; anything added is in.
- Close every TBD the readout review answered. List the ones still open, each with an owner.
- Check the bar: every capability in scope has a section; the data model is complete; security is layer by layer; every recommendation has its reason; every term the client may not know is explained; nothing confidential about the relationship is in it.
- Set the status to "Final" and list what the SC, PM and build lead should review before it goes to the client.

## 7. Report back

Three short paragraphs: what the design covers and how it is organized, what is still TBD and who answers each one, and what the SA should check. No recap of steps.

End with one line naming what comes next: after the first draft, keep it current with `/start-motion:design` after each systems session, third-party call or decision; after scope sign-off, `/start-motion:design` gets it ready to share and the SC, PM and build lead review it; once it is shared, `/start-motion:user-stories` writes the stories with the design in hand.

## Log the run

After the report, write out one short run-log row for the delivery kit and say in one line that pasting it into #discovery-skill-feedback is optional (it helps the kit improve; it is never required). Write it quietly: no questionnaire, no asking the person to rate anything. The row, as plain text:

```
Run log · start-motion:design (v0.1.3) · design · <client> · <date>
Ran by: <the name of the person running it, if the session says; otherwise leave it for them>
Corrected: <what the person corrected during the run, in one to three plain sentences: an output they rewrote, a proposal they rejected and why, an assumption that was wrong. "Nothing" if nothing.>
Had to ask for: <anything you had to ask for that you should have found on your own (a folder, a link, a name already in a note). "Nothing" if nothing.>
Restarted: <No, or Yes and why>
Output: <the link to this run's main output, if there is one>
Notes: <anything else worth a sentence about how the run went, or nothing>
```

Nothing about the run depends on this; a run is never blocked by its log.

## Rules

- Never invent an object, field, API name, number, date or quote. If it is not confirmed, it is TBD.
- Follow the confirmed scope. The design never widens it.
- No requirement IDs or traceability tables; the requirements list holds that.
- No em dashes.
- The SA reviews every draft; the team reviews it before the client sees it.
