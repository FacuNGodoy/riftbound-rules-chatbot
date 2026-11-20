---
title: "473. Layers"
id: "rule-section:473"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "7b011f225ffbc793e4e131c348a5c8b2b825e843e0aaed4829481217651f1322"
generated: true
confidence: "official"
---

# 473. Layers

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**473.** When a player Scores, two things occur:

**473.1.** The player Gains up to one Point, depending on their current score.

**473.1.a.** The Final Point has additional restrictions.
**473.1.a.1.** Notably, points Gained from sources that are not Conquer are not beholden to
these restrictions.

**473.1.b.** When a player tries to Gain a Point through a Conquer, and their current Point Total is 1
point from the Victory Score of the Mode of Play or higher, the following occurs:

**473.1.b.1.** If the player has Scored every Battlefield this turn, that player Gains the Final
Point. If the player has not Scored every Battlefield this turn, that player draws a
card instead.

**473.2.** Trigger Score abilities at the Battlefield that Scored.

**473.2.a.** Conquer abilities trigger at a Battlefield that was Conquered.

**473.2.b.** Hold abilities trigger at a Battlefield that was Held.

**473.2.c.** These will only trigger when the Battlefield is Scored; I.E. These cannot be triggered more
than once per turn for a player.

**474.** When a cleanup occurs and a player has accrued Points greater than or equal to the Victory Score for their
Mode of Play, and if they have more points than every opponent, they Win the Game.

**475.** Layers
**476.** Layers are the mechanism in which Game Effects alter the Traits, Intrinsic Abilities, or other properties of
Game Objects.

**477.** Layers are an organizational structure.

**477.1.** Layers only serve to structure the application and order that Game Effects apply to Game Objects to
maintain consistency.

**478.** The layers are applied repeatedly until all effects operating on an object have been applied once and no
changes have been processed.

**478.1.** Layers are applied and evaluated continuously. All Game Objects have their layers updated in the
same instant, but each Game Object is treated separately and individually when evaluating layers.

**478.1.a.** If evaluating a Game Effect’s applicability depends on information from one or more other
Game Objects, that Game Effect has an object level Dependency. Pause evaluating the
layers of the dependent Game Object and evaluate the layer effects of those Game Objects
whose information is referenced. Continue once the applicability of that Game Effect has
been established or disqualified.
Example: A 4 [M] unit reads in part “While I’m [Mighty], I’m a Yeti.” Another unit
reads in part “I have all tags of units you control.” When the 4 [M] unit is buffed, the
layers for all game objects are evaluated. While evaluating the layers for the second
unit, it requires us to pause and evaluate the layers for all other units. When we’re
evaluating the layers for the 4 [M] unit, after all is said and done, the unit has the
Yeti tag. Once we’ve evaluated all units, we go back to evaluating the second unit,
and at that time it has the Yeti tag as well.

**478.1.b.** If a Game Object has an object level dependency with a Game Object that itself has an
object level dependency with a third Game Object and so on, determine the final point of
the dependency chain and evaluate the layer effects of that Game Object first, continuing
up the dependency chain until all Game Objects have had their layer effects evaluated.

**478.1.c.** If a dependency chain loops back around on itself, identify the minimum set of Game
Objects in the loop and evaluate their layer effects simultaneously, layer by layer. If any of
them have Game Effects that reference Game Objects from outside the set, pause and
evaluate those Game Objects first before continuing with the set.
Example: A 4 [M] unit reads “If there is a [Mighty] enemy unit here, I have +5 [M].”
Both players control one of these units at a battlefield during combat. Each one is
buffed. A third player plays Siphon Power, which reads “Choose a battlefield. Give
friendly units there +1 [M] this turn, and enemy units there -1 [M] this turn, to a
minimum of 1 [M].” Both of the units there are given -1 [M]. Because they have
effects that reference each other, they have a dependency chain. After evaluating
their layers simultaneously, layer by layer, both units will be 4 [M].

**478.2.** Layers are applied in sequence. Each effect in them is applied as soon as able, and only a single time
across all sequences.

**478.3.** When a sequence of applications completes, recur the process, and evaluate each layer again
applying any effects that may now be applicable.

**478.4.** The removal or disqualification of an effect is separate from the application of the effect, but still can
only be applied once.
Example: Fiora, Victorious has printed Might 4 and says “While I'm Mighty, I have Deflect,
Ganking, and Shield.” If a player places a buff on Fiora, her Might is increased in the
Arithmetic layer, after the layer for Ability-Altering Effects. The Ability-Altering Effect layer is
then re-checked and the abilities Deflect, Ganking, and Shield applied. Since each effect has
been applied once and there are no other effects to apply, Fiora’s characteristics are
finalized as 5 Might with Deflect, Ganking, and Shield. While a buffed Fiora, Victorious is in
combat as a defender, an additional +1 Might will be applied in the Arithmetic layer, giving
her 6 Might and the 3 keywords.

Example: A buffed Fiora, Victorious is in combat as a defender when her buff is removed.
Reevaluating the layers in sequence, she no longer gains Deflect, Ganking, and Shield
during the Ability-Altering Effect layer, so when the Arithmetic layer is evaluated, neither the
buff (which is gone) nor Shield (which she no longer has) apply. She goes directly from 6
Might with three keywords to 4 Might with no keywords.

**479.** Layers are applied in the following order:

**479.1.** 1. Copy Effects

**479.1.a.** This layer deals with all copy effects.

**479.1.b.** When a Copy effect is applied to a Game Object, the traits specified by the Copy Effect
replace or are added to the Copyable Traits of the Game Object being Copied as specified
by the effect. If no traits are specified by a Copy Effect, all traits of the Game Object are
replaced with those of the Copied Game Object.
Example: A player triggers Leblanc, Deceiver’s hold effect and plays a Reflection
token, making it a copy of Honest Broker. That player then plays Mirror Image,
targeting the Reflection token. When the Mirror Image Reflection token is played,
it copies all of the copyable traits of the original Reflection token - which are
currently those of Honest Broker which it is a copy of. That player will have three
units named Honest Broker in play, two of which are token Copies with Temporary.

**479.1.b.1.** The copyable traits of a Game Object are all of the printed—or if a copy effect is
applied, copied—traits of that Game Object. In the case of a Token, they are the
traits the token had when it was Created.
Example: The copyable traits include the printed versions of the following
traits: Name, Supertype, Type, Tags, Cost, Domain, Rules Text, Effect Text,
Might, Might Bonus, Flavor Text, Art

**479.1.c.** Copyable traits of a Game Object are distinct from the actual traits of that Game Object,
which may be modified by subsequent applied Layer effects.

**479.1.d.** Effects for this layer can be identified by the phrase "copy" in the text.
Example: Svellsongur is an Equipment that reads in part “As this is attached to a
unit, copy that unit's text to this Equipment's effect text for as long as this is
attached to it.” This is a copy effect that is applied in this layer.

**479.2.** 2. Trait-Altering Effects

**479.2.a.** This layer deals with effects that grant, remove, or replace inherent traits of Game Objects.
Name
Supertype
Type
Tags
Controller
Cost
Domain
Base Might
Base Might Bonus

**479.2.b.** Effects for this layer can be identified by the phrase "become(s)", "give," "is," or "are" in the
text.
Example: A permanent has the ability "Other friendly units are Yordles." Other
friendly units gain the Yordle tag in this layer.

**479.3.** 3. Ability-Altering Effects

**479.3.a.** This layer deals with non-Copy effects that grant, remove, or replace the abilities or rules text
of Game Objects.
Keywords
Passive Abilities
Appending rules text
Removing rules text
Effect Text

**479.3.b.** Effects for this layer can be identified by the phrase "become(s)," "give," "lose(s)," "have,"
"has," "is," or "are" in the text.
Example: A permanent has the ability "Other friendly units have [Vision]." Other
friendly units gain the Vision keyword in this layer.

**479.3.c.** Abilities of Effect Text of Attached cards are appended in this layer.

**479.4.** 4. Arithmetic Effects

**479.4.a.** This layer deals with the mathematics of increasing and decreasing the numeric values of
the traits of Game Objects.
Might
Energy Cost
Power Cost

**479.4.b.** When an arithmetic effect from a source that is not a passive ability has a limitation that
applies, it is limited at the time of its application, and is “remembered” at that limited level
for the duration of its effect. This process is called “snapshotting.”
Example: If an effect gives a unit “-4 [M] to a min of 1 this turn” choosing a unit with
2 [M], then the effect will generate -1 [M] this turn.

Example: A unit reads “Units you control here have their Might increased to 5 [M].”
This is a passive ability, so it will not snapshot.

Example: A spell reads “Increase a friendly unit’s Might to 5 [M].” This effect is
applied once, with an unlimited duration. Because it isn’t from a passive ability, it
will snapshot.
**479.4.c.** Players cannot increase a numeric attribute by a negative amount. If an effect would
instruct a player to do so, they increase it by 0 instead.
Example: A player plays Last Stand, which reads “Double a friendly unit's Might this
turn. Give it Temporary.” The player declares a 2 [M] unit as the target during
finalization. In reaction to Last Stand, an opponent plays Eclipse targeting the 2 [M]
unit. When Last Stand resolves, the unit is -2 [M]. Last Stand instructs its controller
to increase the unit’s Might by its current amount, -2, when the double action is
performed. This is not possible, so the unit’s Might is increased by 0 instead.

**479.4.d.** Might Bonuses of Attached cards are applied in this layer.

**479.4.e.** This layer applies arithmetic in the following way.

**479.4.e.1.** 1. Increases

479.4.e.1.a.                                         Positive values, or increases, to Might are applied first.

479.4.e.1.b.                                         If there is a restriction or limitation to this increase and it isn’t from a
passive ability, the limitation is “snapshotted” for the duration of the effect.

**479.4.e.2.** 2. Decreases

479.4.e.2.a.                                         Negative values, or decreases, to Might are applied last.

479.4.e.2.b.                                         If there is a restriction or limitation to this decrease and it isn’t from a
passive ability, the limitation is “snapshotted” for the duration of the effect.

**479.4.f.** Effects for this layer can be identified by the phrase "give,” “swap,” "increase," "decrease,"
"cost … less," "cost … more," "-X,” or “+X,” in the text.
Example: An effect says “I cost [1] less for each card you've played this turn, to a
minimum of [1].” The cost is modified in this layer.

**480.** If more than one effect applies to the same Game Object in the Same Layer, or to each other in the same
layer, then both effects will apply but their order may be determined by Dependency.

**480.1.** A Dependency is established if:

**480.1.a.** Applying one of the effects alters the existence of the other; or

**480.1.b.** Applying one of the effects alters the number of objects the other effect can influence; or

**480.1.c.** Applying one of the effects alters the outcome when applying the other.

## Mecánicas relacionadas

- [[mechanics/might|Might actual]]
