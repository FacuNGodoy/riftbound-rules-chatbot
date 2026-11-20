---
title: "418. Heal"
id: "rule-section:418"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "58c2368a29dfa7647ad6ec54390d52a9015f07291f72363049f40976d59b4745"
generated: true
confidence: "official"
---

# 418. Heal

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**418.** Deal

**418.1.** Spells, Units, Abilities, and other game effects may Deal Damage to units.

**418.1.a.** Assigning Damage during the Combat Damage Step is not Dealing Damage, but will cause
Damage to be Dealt when assignment is complete.

**418.1.b.** To Deal Damage to Units, mark the specified amount of Damage on the Unit.

**418.1.c.** Damage is marked on each unit separately.

**418.1.d.** Damage can be Dealt to more than one Unit at the same time.

**418.1.e.** Valid Damage is a positive integer amount, greater than or equal to 1 Damage.

**418.1.e.1.** Only Valid Damage is Dealt.
Example: A unit reads “when I take damage, give me +2 [M] this turn.” A
spell is played that Prevents the next 3 damage the unit would take. If a
player plays Hextech Ray targeting the unit, it will take no damage and its
triggered ability will not trigger. If that player had played Void Seeker
instead, it would be Dealt 1 and trigger its ability.

**418.2.** Only Damage can be Dealt.

**418.3.** Dealing Damage is a Limited Action.

**418.3.a.** Assigning Damage causes Damage to be dealt outside of being directed to Deal Damage.
See rule 461. Combat for more information.

**418.4.** Dealing can have the intrinsic property of Bonus Damage.

**418.5.** Bonus Damage is a property granted to the action of Dealing and alters the amount of Damage
distributed by this action.
See rule 712. Bonus Damage for more information.
**418.6.** Deal actions can originate from one or more sources.

**418.6.a.** If a game effect does not specify a source, the game effect describing the Deal action is the
source.
Example: Void Seeker is a spell that reads “Deal 4 to a unit at a battlefield. Draw 1.”
The damage that Void Seeker instructs you to deal is dealt by Void Seeker.

**418.6.b.** If a game effect does specify a source, then that source is what is considered the origin of
the Damage for this Deal action.

**418.6.b.1.** Units and Spells can be the source of Damage for Deal actions.

**418.6.b.2.** Abilities can be the source of Damage for Deal actions.

418.6.b.2.a.                                    When an Ability is the source of Damage for a Deal action, it is in addition
to the Spell or Unit that created that Ability.
Example: Iron Ballista is a gear that says “[E]: Deal 2 to a unit at a
battlefield.” This damage is dealt both by a gear and by an ability.

**418.6.b.3.** When a spell or ability specifies a Unit as the source of the Damage for the Deal
action, it is not in addition to the spell or ability that instructed it.
Example: Challenge is a spell that reads “Choose a friendly unit and an
enemy unit. They deal damage equal to their Mights to each other.” The
damage that Challenge causes to be dealt is dealt by the chosen units,
not by Challenge.

**418.6.b.4.** The controller of the source of a Deal action is responsible for that Deal action
unless the player performing the Deal action is otherwise specified.
Example: If a player plays Challenge targeting a friendly unit and an
enemy unit, the controller of the enemy unit is responsible for the
damage dealt by their unit. Any effects that trigger “when you deal
damage” that that player controls will trigger.

**418.6.c.** Damage Dealt as a result of being assigned during Combat has the Units as its source.

**418.6.c.1.** The Damage assigned, and subsequently Dealt, to attackers has the defenders as
the source and vice versa.

**418.7.** Deal actions can distribute Damage as part of combat actions or non-combat actions.

**418.8.** Some Deal actions may be written as “Deal X … for each …” Such actions Deal one instance of
Damage.
Example: Riven, Shattered reads in part “When I attack, choose an enemy unit here. Deal 2
to it for each Equipment attached to me.” If Riven has three Equipment attached to her, she
will deal one instance of 6 damage, not three instances of 2 damage.

## Mecánicas relacionadas

- [[mechanics/deal|Deal damage]]
