---
title: "337. Step 1: Finalize"
id: "rule-section:337"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "4e4e0e5a769d032311a84de98f2c59651a84d71931f8279f6d2f5f2d3da7c00b"
generated: true
confidence: "official"
---

# 337. Step 1: Finalize

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**337.1.** If there is at least one Chain Item Pending, the controller of the oldest Pending Chain Item must
complete the steps of Playing that Pending Item until it is a Finalized Item or leaves the Chain.
See rule 349. Playing Cards for more information on finalizing chain items.

**337.1.a.** Finalizing an item to the chain does not pass Priority.

**337.1.b.** Chain Items are Finalized in the order they were appended to the Chain.

**337.2.** If, after finalizing the Chain Item, that item is a Unit, Gear, or an ability that Adds resources, it resolves
immediately—Move to Step 4: Resolve.
See rule 349. Playing Cards for more information.

**337.3.** If, after finalizing the Chain Item, there are still Pending Chain Items, return to step 1. Finalize.

**337.4.** If, after finalizing the Chain Item, there are no more items on the chain to be Finalized, the controller
of the next item on the chain gains Priority. Move to step 2: Execute.

## Mecánicas relacionadas

- [[mechanics/triggered-ability|Triggered abilities]]
- [[mechanics/chain|Chain y resolución]]
