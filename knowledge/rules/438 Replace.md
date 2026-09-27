---
title: "438. Replace"
id: "rule-section:438"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "61b06ec51217cf1c13e4db3d766dad60c4122eac2bec7c205383df105f20480d"
generated: true
confidence: "official"
---

# 438. Replace

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**438.1.** Replacing is the act of Creating a token in the place of another card or token without playing it while
inheriting all effects or statuses of the game object it replaced.

**438.1.a.** The replacing token is treated as the same Game Object as the card or token it replaced for
the purposes of Game Effects that target or reference that game object.
Example: A player with Green Father as their legend conquers Navori Fighting Pit.
They choose to place the Green Father conquer effect on the chain after the Navori
Fighting Pit conquer effect. When the Green Father trigger resolves, Navori
Fighting Pit is replaced with Brush. Although the Navori Fighting Pit has been
replaced, the “here” in its triggered ability still can have its information referenced,
because the Brush inherited all statuses and conditions. The unit Navori Fighting
Pit’s triggered ability has targeted will still be a legal target on resolution.

**438.2.** Replacing is a Limited Action.

**438.2.a.** The player may Replace cards and tokens when instructed to do so by other game effects.

**438.3.** This action, when instructed, is formatted as "Replace [X] with [Y]."

**438.3.a.** The [X] is the target to be Replaced.

**438.3.b.** The [Y] is the object that will Replace the target.

**438.3.b.1.** This will always specify a Token to create.

**438.4.** Replacing is not a subset of Banishing.

**438.5.** The card or token that is Replaced is placed in Banishment.

**438.5.a.** While it resides in Banishment, it is considered to have been Replaced and not Banished.

**438.6.** If a token is Replaced it will stop existing once it begins its occupancy in Banishment.

**438.6.a.** This does not invalidate the token created, or the act of Replacement.

**438.7.** Tokens that have been Created through a Replace action can be instructed to be “Swapped back.”
This may also appear as “replace [the token] with the [Game Object] it replaced.”

**438.7.a.** Swapping Back is an extension of the Replace action.

**438.7.b.** To Swap Back, the token stops existing and the original card is returned to the space that
the token just occupied, inheriting all current effects and statuses.

**438.7.b.1.** Any card that has been Replaced by that token or any tokens it Replaced is eligible
to swap back in this way.

**438.7.c.** If there is nothing in Banishment to swap back to then this object can never swap back.

## Mecánicas relacionadas

- [[mechanics/replacement|Replacement effects]]
