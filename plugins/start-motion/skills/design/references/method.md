# Solution design: what this stage is for

Show how we will build it in Salesforce, capability by capability, for the delivery team first and the client second. Scope drives the design: the SA drafts it alongside discovery and the readout, flags anything not confirmed as TBD, and finalizes and shares it once the client has signed the scope. The readout answers what we will build and why; the design answers how.

## Calls the SA makes on every design

- When do I start? During discovery, as soon as the systems sessions start. Draft freely; share nothing with the client before scope is signed
- Sections by capability or by integration? Whatever the build is made of
- Not confirmed yet? Flag it TBD and say what it waits on. Never fill a gap with an assumption
- Recommendation or open item? Recommend when you would make the call and can say why; leave it open when the client or a third party has to answer
- Who decides? Claude makes the clear calls and logs them; the SA confirms recommendations and makes the real trade-offs, from a short options brief; the client answers what only the client can. Every one is a row on the Decisions tab with its options and why, and only the work that depends on an open one waits
- How technical? API names, objects, sharing and patterns, yes. Explain every Salesforce term in a short table so the client can follow it too
- Scope changed after the readout? The design follows the signed scope. Anything set aside comes out of the design, not into it

## The bar: a design is ready to share when

- It matches the scope the client confirmed; anything set aside is out
- Every capability in scope has its own section
- The data model lists every object with its API name, relationships and how it is populated or accessed
- Security and access are spelled out layer by layer
- Every recommendation carries its reason
- Every design choice with a real alternative is on the Decisions tab, and none is still waiting on the SA
- Anything not confirmed is flagged TBD with what it waits on, never assumed
- The diagrams each section needs are listed, and drawn or linked
- Every Salesforce term the client may not know is explained
- The SC, PM and build lead have reviewed it
- Nothing confidential about the relationship is in it

The full method, Steph's two designs, the anatomy of a capability section and the house style are on the Start Motion page, Design stage: https://claude.ai/artifact/7FURp3rBMYHuqmor99zi6S#design
