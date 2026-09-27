---
title: "473. Layers"
id: "rule-section:473"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "232104345bbeaaf163845ccc7b9efd0d693855466c08fde6bf454b117efc6fc7"
generated: true
confidence: "official"
---

# 473. Layers

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**474.** Layers are the mechanism in which Game Effects alter the Traits, Intrinsic Abilities, or other properties of
Game Objects.

**475.** Layers are an organizational structure.

**475.1.** Layers only serve to structure the application and order that Game Effects apply to Game Objects to
maintain consistency.

**476.** The layers are applied repeatedly until all effects operating on objects have been applied once and no
changes have been processed.

**476.1.** Layers are applied in sequence. Each effect in them is applied as soon as able, and only a single time
across all sequences.

**476.2.** When a sequence of applications completes, recur the process, and evaluate each layer again
applying any effects that may now be applicable.
**476.3.** The removal or disqualification of an effect is separate from the application of the effect, but still can
only be applied once.
Example: Fiora, Victorious has printed Might 4 and says “While I'm Mighty, I have Deflect,
Ganking, and Shield.” If a player places a buff on Fiora, her Might is increased in the
Arithmetic layer, after the layer for Ability-Altering Effects. The Ability-Altering Effect layer is
then re-checked and the abilities Deflect, Ganking, and Shield applied. Since each effect has
been applied once and there are no other effects to apply, Fiora’s characteristics are finalized
as 5 Might with Deflect, Ganking, and Shield. While a buffed Fiora, Victorious is in combat as
a defender, an additional +1 Might will be applied in the Arithmetic layer, giving her 6 Might
and the 3 keywords.

Example: A buffed Fiora, Victorious is in combat as a defender when her buff is removed.
Reevaluating the layers in sequence, she no longer gains Deflect, Ganking, and Shield
during the Ability-Altering Effect layer, so when the Arithmetic layer is evaluated, neither the
buff (which is gone) nor Shield (which she no longer has) apply. She goes directly from 6
Might with three keywords to 4 Might with no keywords.

**477.** Layers are applied in the following order:

**477.1.** 1. Trait-Altering Effects

**477.1.a.** This layer deals with effects that grant, remove, or replace inherent traits of Game Objects.
Name
Super Type
Type
Tags
Controller
Cost
Domain

**477.1.a.1.** Assignment of Might is dealt with in this layer.
Example: A spell reads "A unit's Might becomes 4 this turn." The unit's
Might is set to 4 in this layer.

**477.1.b.** Copy effects are applied in this layer.

**477.1.b.1.** When one Game Object becomes a copy of another, all copyable traits replace or
are added to those of the original Game Object as specified by the Game Effect
directing the Copy. This is applied in this layer.

477.1.b.1.a.                                         Copyable traits are:
Name​
Super Type​
Type​
Tags​
Cost​
Domain​
Rules Text

477.1.b.1.b.                                         Copy effects will copy the copyable traits of a Game Object. By default,
those are the printed traits of the Game Object. When a Game Object
becomes a copy of something, its copyable traits are updated to the new
traits it has received.
Example: A player triggers Leblanc, Deceiver’s hold effect and
plays a Reflection token, making it a copy of Honest Broker. That
player then plays Mirror Image, targeting the Reflection token.
When the Mirror Image Reflection token is played, it copies all of
the copyable traits of the original Reflection token - which are
currently those of Honest Broker which it is a copy of. That player
will have three units named Honest Broker in play, two of which
are token Copies with Temporary.
**477.1.b.2.** Some Game Effects may specify copying certain traits of a card. Only the traits
specified by the Game Effect will be copied.

**477.1.c.** Effects for this layer can be identified by the phrase "become(s)", "give," "is," or "are" in the
text.
Example: A permanent has the ability "Other friendly units are Yordles." Other
friendly units gain the Yordle tag in this layer.

**477.2.** 2. Ability-Altering Effects

**477.2.a.** This layer deals with non-Copy effects that grant, remove, or replace the abilities or rules text
of Game Objects.
Keywords
Passive Abilities
Appending rules text
Removing rules text

**477.2.b.** Effects for this layer can be identified by the phrase "become(s)," "give," "lose(s)," "have," "has,"
"is," or "are" in the text.
Example: A permanent has the ability "Other friendly units have [Vision]." Other
friendly units gain the Vision keyword in this layer.

**477.2.c.** Abilities of Effect Text of Attached cards are appended in this layer.

**477.3.** 3. Arithmetic

**477.3.a.** This layer deals with the mathematics of increasing and decreasing the numeric values of
the traits of Game Objects.
Might
Energy Cost
Power Cost

**477.3.b.** When an arithmetic effect from a source that is not a passive ability has a limitation that
applies, it is limited at the time of its application, and is “remembered” at that limited level
for the duration of its effect. This process is called “snapshotting.”
Example: If an effect gives a unit “-4 [M] to a min of 1 this turn” choosing a unit with
2 [M], then the effect will generate -1 [M] this turn.

Example: A unit reads “Units you control here have their Might increased to 5 [M].”
This is a passive ability, so it will not snapshot.

Example: A spell reads “Increase a friendly unit’s Might to 5 [M].” This effect is
applied once, with an unlimited duration. Because it isn’t from a passive ability, it
will snapshot.

**477.3.c.** Players cannot increase a numeric attribute by a negative amount. If an effect would
instruct a player to do so, they increase it by 0 instead.
Example: A player plays Last Stand, which reads “Double a friendly unit's Might this
turn. Give it Temporary.” The player declares a 2 [M] unit as the target during
finalization. In reaction to Last Stand, an opponent plays Eclipse targeting the 2 [M]
unit. When Last Stand resolves, the unit is -2 [M]. Last Stand instructs its controller
to increase the unit’s Might by its current amount, -2, when the double action is
performed. This is not possible, so the unit’s Might is increased by 0 instead.

**477.3.d.** Might Bonuses of Attached cards are applied in this layer.

**477.3.e.** This layer applies arithmetic in the following way.

**477.3.e.1.** 1. Increases
477.3.e.1.a.                                         Positive values, or increases, to Might are applied first.

477.3.e.1.b.                                         If there is a restriction or limitation to this increase and it isn’t from a
passive ability, the limitation is “snapshotted” for the duration of the effect.

**477.3.e.2.** 2. Decreases

477.3.e.2.a.                                         Negative values, or decreases, to Might are applied last.

477.3.e.2.b.                                         If there is a restriction or limitation to this decrease and it isn’t from a
passive ability, the limitation is snapshotted for the duration of the effect.

**478.** If more than one effect applies to the same Game Object in the Same Layer, or to each other in the same
layer, then both effects will apply but their order may be determined by Dependency.

**478.1.** A Dependency is established if:

**478.1.a.** Applying one of the effects alters the existence of the other; or

**478.1.b.** Applying one of the effects alters the number of objects the other effect can influence; or

**478.1.c.** Applying one of the effects alters the outcome when applying the other.

**479.** To determine which effect Depends on another, determine which of the prior criteria applies, and then also
which effect’s evaluation is altered by the sequence of applications. That effect is said to Depend on the other.
Example: A unit with 4 [M] is under the effects of a passive ability that reads “Units you control here
have their Might increased to 5 [M].” Its controller plays Discipline on the unit, giving it +2 [M]. When
applying Layer alterations, both effects are applied in the same layer. If we apply the passive ability
first, the passive ability will give +1 [M] while the Discipline effect will give +2 [M]. If we apply them in
the other order, the Discipline effect will give +2 [M], and the passive ability will give +0 [M]. The
passive ability is altered by the sequence of applications, so it depends on the Discipline effect.

**479.1.** If both effects are altered by the application of the other, no Dependency can be established.
Example: A unit with 4 [M] is under the effects of a passive ability that reads “Units you
control here have their Might increased to 5 [M].” Its controller plays a spell that reads “Give a
unit +2 [M], to a maximum of 5 [M].” If we apply the passive ability first, the passive ability will
apply +1 [M] and the spell effect will apply +0 [M]. If we apply the spell effect first, it will apply
+1 [M] while the passive ability applies +0 [M]. Both effects are altered by the sequence of
applications, so we can’t establish a dependency.

**479.2.** To resolve a dependency, the effects within the same layer that created the dependency must be
applied such that:
1. Identify which effect Depends on the other within the Layer.
2. Apply the effect that is depended on first.
3. Immediately apply the effect that Depends on the first effect next.

Example: A unit with 4[M] is under the effects of a passive ability that reads “Units you
control here have their Might increased to 5 [M].” Its controller plays Discipline on the unit. As
previously established, the passive ability depends on the Discipline effect. We apply the
Discipline effect first, giving the unit +2 [M], and then immediately apply the passive ability
that depends on it. The unit’s final Might is 6 [M].

**480.** If more than one effect applies in the same layer but no dependency is established, then Timestamp order is
applied to the effects within that layer and sublayer

**480.1.** When an effect begins applying, it establishes a time for which it is compared against other Game
Effects for purposes of resolving Layered effects as its Timestamp.

**480.1.a.** Timestamps are not rote values.

**480.1.b.** Timestamps are relative comparisons between effects and when they began applying to
the game.
**480.1.c.** Timestamps are not referenced by Game Effects in any way. They are only used to finalize
layered effects.

**480.2.** When Rules Text becomes Inactive for any reason, it loses its Timestamp. When it ceases to be
Inactive, a new Timestamp is established.

**480.3.** Effects are applied such that the earliest Timestamp within each Layer and Sublayer applies first,
followed by other Effects in that Layer and Sublayer in chronological order.

## Mecánicas relacionadas

- [[mechanics/might|Might actual]]
