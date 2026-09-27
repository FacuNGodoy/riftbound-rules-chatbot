---
title: "417. Deal"
id: "rule-section:417"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "301d676ec581b7560918089e8a0d13db715bde4b2bba530ac84f0c679f979903"
generated: true
confidence: "official"
---

# 417. Deal

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**417.1.** Spells, Units, Abilities, and other game effects may Deal Damage to units.

**417.1.a.** Assigning Damage during the Combat Damage Step is not Dealing Damage, but will cause
Damage to be Dealt when assignment is complete.

**417.1.b.** To Deal Damage to Units, mark the specified amount of Damage on the Unit.

**417.1.c.** Damage is marked on each unit separately.

**417.1.d.** Damage can be Dealt to more than one Unit at the same time.

**417.1.e.** Valid Damage is a positive integer amount, greater than or equal to 1 Damage.

**417.1.e.1.** Only Valid Damage is Dealt.
Example: A unit reads “when I take damage, give me +2 [M] this turn.” A
spell is played that Prevents the next 3 damage the unit would take. If a
player plays Hextech Ray targeting the unit, it will take no damage and its
triggered ability will not trigger. If that player had played Void Seeker
instead, it would be Dealt 1 and trigger its ability.

**417.2.** Only Damage can be Dealt.

**417.3.** Dealing Damage is a Limited Action.

**417.3.a.** Assigning Damage causes Damage to be dealt outside of being directed to Deal Damage.
See rule 459. Combat for more information.

**417.4.** Dealing can have the intrinsic property of Bonus Damage.

**417.5.** Bonus Damage is a property granted to the action of Dealing and alters the amount of Damage
distributed by this action.
See rule 712. Bonus Damage for more information.

**417.6.** Deal actions can originate from one or more sources.
**417.6.a.** If a game effect does not specify a source, the game effect describing the Deal action is the
source.
Example: Void Seeker is a spell that reads “Deal 4 to a unit at a battlefield. Draw 1.”
The damage that Void Seeker instructs you to deal is dealt by Void Seeker.

**417.6.b.** If a game effect does specify a source, then that source is what is considered the origin of
the Damage for this Deal action.

**417.6.b.1.** Units and Spells can be the source of Damage for Deal actions.

**417.6.b.2.** Abilities can be the source of Damage for Deal actions.

417.6.b.2.a.                                     When an Ability is the source of Damage for a Deal action, it is in addition
to the Spell or Unit that created that Ability.
Example: Iron Ballista is a gear that says “[E]: Deal 2 to a unit at a
battlefield.” This damage is dealt both by a gear and by an ability.

**417.6.b.3.** When a spell or ability specifies a Unit as the source of the Damage for the Deal
action, it is not in addition to the spell or ability that instructed it.
Example: Challenge is a spell that reads “Choose a friendly unit and an
enemy unit. They deal damage equal to their Mights to each other.” The
damage that Challenge causes to be dealt is dealt by the chosen units, not
by Challenge.

**417.6.b.4.** The controller of the source of a Deal action is responsible for that Deal action
unless the player performing the Deal action is otherwise specified.
Example: If a player plays Challenge targeting a friendly unit and an
enemy unit, the controller of the enemy unit is responsible for the damage
dealt by their unit. Any effects that trigger “when you deal damage” that
that player controls will trigger.

**417.6.c.** Damage Dealt as a result of being assigned during Combat has the Units as its source.

**417.6.c.1.** The Damage assigned, and subsequently Dealt, to attackers has the defenders as
the source and vice versa.

**417.7.** Deal actions can distribute Damage as part of combat actions or non-combat actions.

## Mecánicas relacionadas

- [[mechanics/deal|Deal damage]]
