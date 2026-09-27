---
title: "340. Step 4: Resolve"
id: "rule-section:340"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "1186bdfe0c00f91c191be268f477c0c7fa5391f23000fccb046e958185bc6619"
generated: true
confidence: "official"
---

# 340. Step 4: Resolve

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**340.1.** The newest Finalized Chain Item resolves. Execute its game effects in their entirety.
See rule 349. Playing Cards for more information on resolving spells.
See rule 398. Playing or Activating Abilities for more information on resolving abilities.

**340.2.** If the Chain is empty, play proceeds in an Open State.

**340.2.a.** If this occurs during a Showdown and the chain wasn’t initiated by a triggered ability or an
ability that Adds resources, focus passes to the next player in turn order.

**340.3.** If the Chain is not empty and there are one or more Pending Items, return to Step 1: Finalize.

**340.4.** If the Chain is not empty and there are no Pending Items, the controller of the newest item on the
chain gains Priority. Return to Step 2: Execute.

## Mecánicas relacionadas

- [[mechanics/play|Play]]
- [[mechanics/play-trigger|Triggers al jugar]]
- [[mechanics/chain|Chain y resolución]]
