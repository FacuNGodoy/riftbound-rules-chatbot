---
title: "439. Create"
id: "rule-section:439"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "20c79b350ba7ffae52960552f01298cbc6ad887b41ac92372c7821c8f981fad9"
generated: true
confidence: "official"
---

# 439. Create

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**439.** Replace

**439.1.** Replacing is the act of Creating a token in the place of another card or token without playing it
while inheriting all effects or statuses of the game object it replaced.

**439.1.a.** The replacing token is treated as the same Game Object as the card or token it replaced for
the purposes of Game Effects that target or reference that game object.
Example: A player with Green Father as their legend conquers Navori Fighting Pit.
They choose to place the Green Father conquer effect on the chain after the Navori
Fighting Pit conquer effect. When the Green Father trigger resolves, Navori
Fighting Pit is replaced with Brush. Although the Navori Fighting Pit has been
replaced, the “here” in its triggered ability still can have its information referenced,
because the Brush inherited all statuses and conditions. The unit Navori Fighting
Pit’s triggered ability has targeted will still be a legal target on resolution.

**439.2.** Replacing is a Limited Action.

**439.2.a.** The player may Replace cards and tokens when instructed to do so by other game effects.

**439.3.** This action, when instructed, is formatted as "Replace [X] with [Y]."

**439.3.a.** The [X] is the target to be Replaced.

**439.3.b.** The [Y] is the object that will Replace the target.
**439.3.b.1.** This will always specify a Token to create.

**439.4.** Replacing is not a subset of Banishing.

**439.5.** The card or token that is Replaced is placed in Banishment.

**439.5.a.** While it resides in Banishment, it is considered to have been Replaced and not Banished.

**439.6.** If a token is Replaced it will stop existing once it begins its occupancy in Banishment.

**439.6.a.** This does not invalidate the token created, or the act of Replacement.

**439.7.** Tokens that have been Created through a Replace action can be instructed to be “Swapped back.”
This may also appear as “replace [the token] with the [Game Object] it replaced.”

**439.7.a.** Swapping Back is an extension of the Replace action.

**439.7.b.** To Swap Back, the token stops existing and the original card is returned to the space that
the token just occupied, inheriting all current effects and statuses.

**439.7.b.1.** Any card that has been Replaced by that token or any tokens it Replaced is
eligible to swap back in this way.

**439.7.c.** If there is nothing in Banishment to swap back to then this object can never swap back.

## Mecánicas relacionadas

- [[mechanics/replacement|Replacement effects]]
