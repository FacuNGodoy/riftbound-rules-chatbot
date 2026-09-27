---
title: "428. Kill"
id: "rule-section:428"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "603fe748c105579cf208688008dc08ec4db8c1d809fdf6c19baad9ebc84c2dcb"
generated: true
confidence: "official"
---

# 428. Kill

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**428.1.** Killing is the action of a Permanent going to the trash from the board.

**428.1.a.** This can be Active or Passive.

**428.1.a.1.** Active Kill is when the action is taken when instructed by a game effect or as a cost
for a card or ability.

428.1.a.1.a.                                         This is referred to as a Kill Instruction.

428.1.a.1.b.                                         When a unit with a Deathknell or other ability that triggers on its own
death is to be put in the Trash due to a Kill Instruction, it first has any
such ability added to the chain as a Pending Item. Note the unit’s
location, attributes, and other relevant information to process those
abilities when finalized before completing this Kill Instruction.
Example: Draven, Audacious reads in part “When I die in combat,
choose an opponent. They gain 1 point.” The ability triggers when
Draven himself dies, so it will go on the chain first when a kill
instruction is performed on Draven, before he is put in the trash.

**428.1.a.2.** Passive Kill is when the action is taken as a result of Lethal Damage or as a
consequence for any other state.

**428.2.** When a permanent is killed it is placed directly in the trash from its place of origin.

**428.2.a.** It is only considered Killed if its origin was any zone on the board.

**428.2.b.** This is not a subset of Move.

**428.3.** Killing is a Limited Action.

**428.3.a.** Players may only Kill units when Game Effects direct them to do so.

**428.4.** Killing can also be the result of resolving a Cleanup.

**428.5.** Killing can be attributed to one or more Game Objects.

**428.5.a.** The Killed Unit or Gear is said to be Killed by that Game Object.

**428.5.b.** A spell or ability that contains a Kill instruction is responsible for Killing the Unit or Gear.
**428.5.c.** When one or more Units is killed due to a Cleanup, that kill action is attributed to the spell
or ability that resolved immediately prior to that Cleanup that dealt damage to the Unit or
Units.

**428.5.c.1.** The player responsible for the deal action is responsible for the kill action.

**428.5.c.2.** If the Cleanup that caused the units to be killed was the Combat Cleanup, the
sources of the Combat Damage are attributed the kill action, and their controller is
responsible for the kill action.

**428.5.d.** Abilities originating from Game Objects that are attributed Kill Actions are attributed in
addition to the Game Object that created them.
Example: There is a spell that says “Do this twice: Deal 3 to a unit.” Immortal
Phoenix is a unit that says “When you kill a unit with a spell, you may pay [1][C] to
play me from your trash.” A player plays the spell while Immortal Phoenix is in their
trash. The “do this” phrasing means that it has a reflexive triggered ability, which
places two triggered abilities on the chain. As each of those triggered abilities
resolve, it deals damage to the unit chosen for that ability. If one of these abilities
deals lethal damage to a unit, both the spell and its ability are considered sources of
the damage, and so both the spell and its ability receive attribution for killing the
unit. This means that the spell’s controller killed a unit with a spell, so Immortal
Phoenix’s ability will trigger.

**428.6.** This action is formatted as "Kill [one or more permanents]."
e.g., "Kill an enemy unit."
e.g., "Kill this, [2]: Draw 1."
e.g., "Kill all gear."

## Mecánicas relacionadas

- [[mechanics/kill|Kill]]
