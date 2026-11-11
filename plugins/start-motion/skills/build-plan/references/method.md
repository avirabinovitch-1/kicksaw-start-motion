# Build plan: what this stage is for

Settle the order, the dependencies and what "built" means for each story before anyone builds. Stories say what the system does; the build plan says which change comes first, what each change covers, and how we will know it worked. The solution architect owns it and approves it. A developer who was not in discovery should be able to pick up any task and build it without asking a question.

## Calls the SA makes on every plan

- Which stories are ready? Only stories the product owner has been through, with no open question that touches a criterion. The rest wait, with the question named
- How small is a task? Small enough to build and review in one sitting. If the change would take a reviewer more than a few minutes to read, split it
- What order? Whatever depends on nothing first: objects, then fields, then access and pages, then automation, then reports
- What proves it? Every task names its check before it is built: a validation, a test and what it asserts, or a step done by hand in the sandbox
- A name the design does not give? The SA gives it. The plan never invents one
- Something useful nobody asked for? It goes to Suggestions. It is not a task until it is a story

## The bar: a plan is ready to approve when

- Every criterion of every planned story is covered by a task, and every task has a criterion behind it
- Tasks are in an order that can be built top to bottom without going back
- Each task names what it creates or changes, by real name
- Each task names the check that proves it
- Manual steps and data work are listed as tasks done by hand, with who does them
- Stories not planned are listed with what each waits on
- SOW limits are counted, today and after the plan is built
- The plan starts from an org summary no older than the last change in the sandbox

The stage on the Start Motion page: https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S
