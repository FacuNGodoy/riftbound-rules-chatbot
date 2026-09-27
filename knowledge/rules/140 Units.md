---
title: "140. Units"
id: "rule-section:140"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "1ecd940def7e6b03ea188c21dfd36fdf482a1fa7fb22b74be6322961c1740895"
generated: true
confidence: "official"
---

# 140. Units

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**141.** Unit is:

**141.1.** A Game Object

**141.1.a.** While on the Board:

**141.1.a.1.** Units are at one of several Locations while on the Board: a Battlefield or their
Base.

**141.1.a.2.** Units and their details are Public Information while on the Board.

**141.1.a.3.** Units can be chosen, affected, or manipulated by spells, affects, or game actions
that specify Units.

**141.1.a.4.** Units can be Killed.
See rule 428. Kill for more information.

**141.1.b.** While in the Trash:

**141.1.b.1.** Units are treated as Cards, similar to when in the Hand.

**141.1.b.2.** They retain the properties of being a Unit, but are not on the Board and thus
cannot take actions or be affected by spells, abilities, or game actions that target
Units on the Board.

**141.1.b.3.** Units can be affected by spells and game effects that target Units in the Trash.

**141.2.** A Card Type

**141.2.a.** This is a unique identifier that some spells or abilities will use to restrict what they can
choose or affect.

**141.2.b.** The card type is relevant in all zones.

**142.** Damage is a marked value that is applied to Units.

**142.1.** Damage is not a Game Object.

**142.2.** Damage is a value tracked per-Unit.

**142.3.** Damage is marked on Units by players.

**142.3.a.** The player responsible for the Deal action that caused the Damage to be marked is the
player who marked that Damage.

**142.3.b.** Game Effects may refer to that player’s Damage. This means the Damage marked by that
player.
Example: A unit reads in part “Your damage can’t be prevented.” This refers to the
damage marked by that player.

**142.4.** Damage tracks how close a Unit is to being Killed.
See rule 428. Kill for more information.

**142.4.a.** Lethal Damage is the amount of marked Damage that will cause a unit to die in a cleanup.

**142.4.b.** Lethal Damage for a Unit is a non-zero amount greater than or equal to that Unit’s Might.
Example: A unit has 5 [M] and 3 damage marked on it. Frigid Touch is played
targeting that unit. When it resolves, the unit’s Might becomes 3, and it will have
lethal damage marked on it.

Example: A unit has 0 [M]. In order to have lethal damage marked on it, it must
have at least 1 damage marked on it.

**142.4.c.** Some effects may alter this amount. These effects will refer to the amount of damage
needed to kill a unit.
Example: Elder Dragon’s passive ability reads “Any amount of your damage is
enough to kill enemy units.” This alters the Lethal Damage value for enemy units
that have damage marked by you.

**142.5.** Damage can be Healed.
See rule 418. Heal for more information.

**143.** Units have multiple Intrinsic Properties unique to them:

**143.1.** Tag: A Unit has zero or more Tags representing one or more champions, regions, factions, or species
it belongs to.

**143.1.a.** These have no intrinsic rules or behaviors by themselves.

**143.1.b.** Spells, abilities, and game actions can reference these types as part of their execution.

**143.2.** Might: The combat statistic of a Unit. Used to determine a Unit's contribution to Combat, as well as
when it is Killed by damaging effects.

**143.2.a.** If a Unit ever has nonzero damage marked on it equalling or exceeding its Might, it is Killed.

**143.2.b.** If a unit's Might is ever less than 0, it is treated as 0 when referenced by spells and abilities,
and when summing Might to be assigned as damage in the Combat Damage Step.
See rule 465. The Combat Damage Step for more information.

**143.2.b.1.** Although the unit’s Might is treated as 0, it is not 0. Effects that calculate Might
increases and decreases use the actual value of the unit’s Might.

**143.3.** Units can have damage marked on them.

**143.3.a.** When spells, abilities, or other game effects deal damage, Units mark that damage on them
temporarily. This can be tracked with coins, dice, or other markers, or by memory.

**143.3.b.** Damage is Healed from Units at two specific times:

**143.3.b.1.** At the end of each player's turn.
See rule 317.2. Ending Phase for more information.

**143.3.b.2.** During a Combat Cleanup.
See rule 466.1. for more information about Combat Cleanups.

**143.4.** Units enter the Board exhausted.
**143.4.a.** This can be altered by Accelerate or similar game effects.
See rule 805. Accelerate for more information.

**144.** Units have the Inherent Ability to perform a Standard Move.

**144.1.** This action is limited in when it can be performed.

**144.1.a.** This action can be done any time during a player's Main Phase.

**144.1.b.** This action cannot be performed during a Closed State.

**144.1.c.** This action cannot be performed during a Showdown or Combat.

**144.2.** Exhausting the Unit is the Cost for this action.

**144.3.** Players may perform multiple Units' standard move simultaneously. This is treated as one game
action performed on multiple Units.

**144.3.a.** When a Move like this is declared by a player, the units' Destination must be the same.

**144.3.b.** When a Move like this is declared by a player, the Origins do not need to be the same.

**144.3.c.** The Costs of Exhausting the Units are also paid Simultaneously.

**144.4.** The Destinations where Units can Move to with their Standard Move are restricted:

**144.4.a.** Units may move from their Base to a Battlefield.

**144.4.a.1.** Units cannot Move to a Battlefield that already has units from 2 other players
present, or where a Combat is ongoing that has 2 other players as participants.
See rule 447.2. For more information on valid destinations for movement.

**144.4.b.** Units may move from a Battlefield to their Base.

**144.4.c.** Ganking is a unique ability that affects a Unit's Standard Move

**144.4.c.1.** Units with Ganking may use their Standard Move to Move from Battlefield to
Battlefield.
See rule 810. Ganking for more information.

**145.** Units may have Activated Abilities.

**145.1.** Activated Abilities are Game Effects that are written as Costs followed by a ":", and then succeeded
by an effect.
See rule 376. Activated Abilities for more information.

**145.2.** The Activated Ability of Units may be executed at any time during the controlling player's Main
Phase during an Open State, and not during a Showdown.

**145.2.a.** This follows the same process as playing a card.
See rule 349. Playing Cards for more information.

**145.2.a.1.** This behaves, once activated, like a spell without an associated card.

**146.** Units have a Location.

**146.1.** A Unit’s Location is the Base or Battlefield it currently occupies.
See rule 197. Locations for more information.

## Mecánicas relacionadas

- [[mechanics/kill|Kill]]
- [[mechanics/might|Might actual]]
- [[mechanics/deal|Deal damage]]
