# User stories: what this stage is for

Turn the signed scope into epics and stories in the client's Jira project, then refine them live with the client's product owner until each sprint has what it needs. Every requirement already has a draft story from the call it was heard on; this stage finishes those drafts against the signed readout, pushes them to Jira as New, and runs refinement one sprint ahead of the build. If it is not in the acceptance criteria, it is not getting built.

## Where stories come from

- Sources: the solution readout at the version the client signed; the requirements list, for the items marked approved and the stories drafted for them in discovery; the solution design doc, so stories name objects and fields that exist
- Not yet: stories for requirements still heard or confirmed stay drafts on the sheet; items on the scope watch list wait for a change order
- Gaps are normal: discovery covers the workflow, not every value and exception. Each gap becomes an open question on the story it affects, never a vague criterion
- A refinement answer that widens a story past the signed scope goes on the scope watch list with the quote, and the PM hears about it that week

## Calls the SC makes story by story

- How fine to split? One story is one behavior a tester can sign off in one sitting. Two roles in the sentence, or two jobs, means two stories
- Fields table or its own story? Fields that exist for this behavior go in this story's AC as a table; a set the whole org uses gets its own story under the core record epic
- Approved but still vague? Write the behavior you can defend from the readout and the quotes, and put the rest in open questions
- Context or clutter? Keep the quote, the why, the supersession and the dependencies; drop anything that only restates the criteria or describes the build
- The product owner changes the design? Inside the signed scope, update the story and tell the SA. If it changes timeline or budget, it is a change order
- What goes in sprint 1? The foundation the rest depends on: the core record, its fields and the first workflow

## The bar: a story is ready for refinement when

- The sentence names a specific operational role, a capability and a business outcome, with no technology in it
- The description says what the business situation is, carries the client's words with speaker and date, and ends with source, supersedes, dependencies and priority
- The source line points at the signed readout: version, section 8 workflow and steps, section 5 row
- Every criterion is one true or false check with an explicit trigger that names existing metadata
- Anything with math or dates has a worked check with real numbers
- The empty state, the cancel path and the exclusions are covered
- None of the banned words appear in the acceptance criteria: should, might, could, may, usually, generally, appropriately, properly, quickly, seamlessly, user-friendly, intuitive, as needed, where applicable
- Every gap is an open question naming the criterion it affects; no criterion is written around an unknown
- Build details, metadata and test steps are empty

## And the backlog is ready for sprint 1 when

- Every approved requirement is under a story in Jira, or explicitly deferred with a reason
- Migration has its own epic
- The sprint 1 stories are refined with the product owner, their open questions closed
- The SA has added build details to every sprint 1 story and sized it with the SC
- The PM, SC and SA have loaded the sprint, and the internal build kickoff is on the calendar

The full method, the Kicksaw Academy deck, the real Jira examples and the story before and after are on the Start Motion page, User stories stage: https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S#stories
