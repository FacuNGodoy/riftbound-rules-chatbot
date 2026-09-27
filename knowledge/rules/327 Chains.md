---
title: "327. Chains"
id: "rule-section:327"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "91f66cb9fb6cc064e79d82a204a0052f547180a9a3bbab7ee130f6b6f8a414cd"
generated: true
confidence: "official"
---

# 327. Chains

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**328.** The Chain is a Non-Board Zone that temporarily exists whenever a card is played or an ability is activated.

**328.1.** Cards, abilities, and tokens are placed here as part of the process of being played.
See rule 349. The Process of Play for more information.
See rule 360. Abilities for more information on Abilities.

**329.** Cards, tokens, and abilities added to the chain are added as Pending Chain Items that become Finalized
Chain Items.

**329.1.** Pending Items are on the Chain.

**329.2.** Chain Items are Pending until the “Check Legality” step of playing a card.
See rule 349. Playing Cards for more information.

**329.3.** When a Pending Chain Item is no longer Pending it is finalized and becomes a Finalized Chain
Item.

**330.** The Chain exists as long as a Chain Item is on it.

**330.1.** Only one Chain can exist at a time.

**330.2.** If a card or token would begin to be played while a Chain already exists, it is placed on the existing
Chain.

**331.** The State of the Turn is partially determined by whether or not the Chain currently exists.

**331.1.** The turn is said to be in a Closed State if a Chain exists.

**331.1.a.** Cards of all Categories, by default, cannot be played during a Closed State.

**331.1.b.** Card abilities, by default, cannot be played during a Closed State.

**331.2.** The turn is said to be in an Open State if no Chain exists.

**332.** Handling Tasks and Resolving Chain Items

**333.** A Task is one or more steps or processes that one or more Players must perform before continuing with any
other actions.

**333.1.** Tasks include, but are not limited to: Cleanups, the actions performed during the Start of Turn
Process, throughout Combat in its various steps, and the actions performed during the End of Turn
Process.
See rule 318. Cleanups for more information on Cleanups
See rule 315. Start of Turn for more information on the Start of Turn process
See rule 459. Combat for more information on the steps of Combat
See rule 317. Ending Phase for more information.

**334.** Whenever a Player takes one or more actions that incur Tasks they should refer to the process of HOT FEPR:
Handle Outstanding Tasks; then Finalize, Execute, Pass, Resolve.

**334.1.** In the course of Handling Outstanding Tasks, Chain Items may be added to the Chain. They will
remain there until the Tasks are complete.
**334.2.** When all Outstanding Tasks are completed, all pending Chain Items will subsequently be processed
by the FEPR process.

**334.2.a.** During the FEPR process, new Tasks may be incurred. Complete the current step of the
process and then pause and complete the necessary Tasks before continuing.

**335.** If there are no Outstanding Tasks, no pending Chain Items, no ongoing Showdown or Combat, and it is the
Main Phase, the Turn Player receives priority. If there are no Outstanding Tasks, no pending Chain Items, no
ongoing Showdown, and it is any other phase of the turn, proceed to the next substep, step, phase, or turn.

**335.1.** If there are no Outstanding Tasks, no pending Chain Items, and there is an ongoing Showdown, the
player with Focus receives priority.

**336.** When there are no outstanding Tasks and there are pending Chain Items on the Chain, players should refer
to the FEPR process to proceed.

**336.1.** In the sequence of resolving FEPR more Chain Items may become Pending Chain Items. These will
be processed by the same FEPR process that produced them.

## Mecánicas relacionadas

- [[mechanics/reaction|Reaction]]
