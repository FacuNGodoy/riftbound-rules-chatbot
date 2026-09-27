---
title: "393. Linked Abilities"
id: "rule-section:393"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "794ffb015363d2214e4adf1e3051c6e85dd07b2b57b4847185b7fa89d6981327"
generated: true
confidence: "official"
---

# 393. Linked Abilities

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**394.** Linked Abilities are a set of Abilities with one or more of the component Abilities referencing the other
Abilities in the set.

**394.1.** Component Abilities can reference other Abilities in the set by means of referencing those Abilities
directly or by referencing Game Objects affected by or mentioned in another Ability in the set.

**395.** In order for a set of Abilities to be Linked, they must be present in the printed Effect or Rules Text of the same
Game Object, or be granted by the same source to another Game Object.
Example: The Zero Drive is an Equipment gear whose rules text reads in part “[3][B], Banish this: Play
all units banished with this, ignoring their costs.” The Zero Drive’s effect text reads “[Deathnkell][>]
Banish me.” The granted deathknell ability is linked with the Zero Drive’s activated ability.

**396.** Linked Abilities can contain component Abilities of any type.

**397.** A component Linked Ability that references a Game Object affected by another Ability in the set may only
interact with Game Objects affected by the Abilities it is Linked with.
Example: The Zero Drive is an Equipment gear whose rules text reads in part “[3][B], Banish this: Play
all units banished with this, ignoring their costs.” Any units banished by effects other than component
Linked Abilities in the same set as the activated ability cannot be played when resolving the activated
ability.

## Mecánicas relacionadas

- [[mechanics/linked-instruction|Instrucciones vinculadas]]
