---
title: "382. Triggered Abilities"
id: "rule-section:382"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "a476a21c5efe9510299afa28d776a92b7abd71ba712c096e21382d764e74925d"
generated: true
confidence: "official"
---

# 382. Triggered Abilities

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**383.** Triggered Abilities are repeatable effects that happen when a Condition is met.

**383.1.** Triggered Abilities can usually be recognized by the word "when" followed by a game action or
event; the word "at" followed by a point in time during the turn sequence; or the phrase “the [Nth]
time” followed by a game action or event.
Examples:
"When you conquer here, you may spend a buff to draw 1."

"At the end of your turn, ready 2 runes."

“The first time I move each turn, you may ready something else that's exhausted.”

**383.1.a.** The phrases that identify triggered abilities do not always appear at the beginning of
sentences or abilities.

**383.1.b.** If an ability triggers “the [Nth] time” something happens and that trigger condition is met
multiple times simultaneously, the ability’s controller picks one of those instances to serve as
the trigger condition. The ability triggers only once, due to the chosen condition.
Example: Wraith of Echoes reads “The first time another friendly unit dies each turn,
draw 1.” That ability hasn’t triggered yet this turn. Two other friendly units die
simultaneously (say, due to combat damage). The Wraith’s controller chooses one
of those deaths to trigger Wraith’s ability.

**383.2.** Triggered Abilities have a Condition and an Effect.

**383.2.a.** The Condition is the clause with When, At, or the Nth Time.

**383.2.a.1.** Any additional conditional statement immediately after the Condition must be
true in order for the Condition to be fulfilled. Such a conditional statement is part of
the Trigger Condition and not the Effect.
Example: Sona, Harmonious reads “At the end of your turn, if I'm at a
battlefield, ready up to 4 friendly runes.” Her Trigger Ability’s Condition will
be fulfilled in the Ending Step, but the Triggered Ability will only be placed
on the chain if she is located at a battlefield when the Condition is fulfilled.
If she is removed in reaction to the triggered ability, it will still resolve.

Example: Loose Cannon reads “At the start of your Beginning Phase, draw
1 if you have one or fewer cards in your hand.” The “if you have one or fewer
cards in your hand” conditional statement is not immediately after the
trigger condition, so it is part of the effect and not the condition.

**383.2.b.** The Effect is the Instructions that are not part of the Condition.

**383.2.c.** The Condition of a Trigger is evaluated after a potentially inciting event has been processed.

**383.2.c.1.** If a Game Object has a Triggered Ability that is active in a specific zone, it is
evaluated and subsequently triggered if it enters that zone at the same time that
its Trigger’s condition is met.
Example: Immortal Phoenix says “When you kill a unit with a spell, you
may pay [1][C] to play me from your trash.” This ability triggers if Immortal
Phoenix is in your trash immediately after you kill a unit with a spell, even if
the unit you killed with a spell was that Immortal Phoenix.

**383.2.c.2.** A Game Object will not be able to successfully evaluate its Trigger Condition,
however, if it leaves the zone that its Trigger is active from at the same time that its
Trigger is satisfied.
Example: Viktor, Leader says “When another non-Recruit unit you control
dies, play a 1 [M] Recruit unit token into your base.” This ability triggers if
Viktor is on the board immediately after another non-Recruit unit you
control dies. It does not trigger if Viktor and another non-Recruit unit you
control die during the same game action (for instance, if they are both
killed in the same Cleanup due to the damage dealt by Unchecked
Power).

**383.3.** When a Condition is met, a Triggered Ability behaves like an Activated Ability and is placed on the
Chain.

**383.3.a.** If a Triggered Ability says “you may”or “they may” as the first part of its Effect, the controller
of its source will choose whether or not to perform the Triggered Ability during finalization.
Example: Tideturner reads “When you play me, you may choose a unit you control
at another location. Move me to its location and it to my original location.” This “you
may” appears as the first part of its effect, so the choice represents whether or not
to perform the triggered ability.

**383.3.a.1.** The decision of “may” when it appears in this way is solely whether or not to
perform said triggered ability.

**383.3.a.2.** If the controller of the Triggered Ability chooses not to perform that Triggered
Ability during finalization, it is removed from the chain and considered to have not
triggered.

**383.3.a.3.** If “you may” or “they may” appears in any later part of the Effect of a triggered
ability, it is decided on resolution.
Example: Ornn, Blacksmith reads “When you play me or when I hold, look
at the top 4 cards of your Main Deck. You may reveal a gear from among
them and draw it. Then recycle the rest.” This “you may” does not appear
as the first part of its effect, so the choice is made on resolution. The ability
is always finalized to the chain.

**383.3.b.** If a Triggered Ability contains a cost within instructions at the beginning of the effect or
immediately following the “you may” or “they may” that appears as the first part of the
effect, that cost is treated as the base cost of the Triggered Ability.
Example: Ekko, Recurrent reads “[Deathknell][>] Recycle me to ready your runes.” In
this case, “recycle me to ready your runes” is a cost within instructions that appears
at the beginning of the effect of the ability, and thus “recycle me” is taken as the
base cost of the triggered ability.

Example: Insightful Investigator reads “When you play me, choose an opponent.
They reveal their hand. You may pay 2 XP to choose a card from their hand. If you
do, they discard that card and draw 1.” The “pay 2 XP” is a cost within instructions,
but because it does not appear in the first part of the effect, it is not taken as the
base cost of the triggered ability. Paying 2 XP is performed on resolution.

**383.3.b.1.** The cost must be paid in order to finalize the Triggered Ability to the Chain.

**383.3.c.** Triggered Abilities can be put on the Chain during Closed States or Open States on any
player's turn.

**383.3.d.** If more than one Triggered Ability is Triggered simultaneously, then the player that controls
the Abilities selects the order to place them on the Chain.

**383.3.d.1.** If multiple players separately control Triggered Abilities that are Triggered
simultaneously, then starting with the Turn Player and proceeding in Turn Order,
each player orders their Triggered Abilities on the Chain.

**383.3.e.** Some Triggered Abilities will trigger “once each turn,” or “N times each turn.”

**383.3.e.1.** Such a Triggered Ability will only be performed the specified number of times
each turn. If its trigger condition would be fulfilled and it has already been
performed that many times, it does not trigger.

**383.3.e.2.** If the Triggered Ability says “you may” or “they may” as the first part of its effect, its
controller has the choice of whether or not it is performed.

383.3.e.2.a.                             During finalization of the Triggered Ability, the player who controls the
Triggered Ability may choose to perform it.

383.3.e.2.b.                             If they do not, it is removed from the chain.
Example: A player controls a unit that reads in part “Once each
turn, when an enemy unit dies, you may banish it.” When an
enemy Recruit token dies, the triggered ability goes on the chain.
If they choose not to perform the ability on finalization, it is
removed from the chain. When a Stalwart Poro dies later in the
turn, they can choose to trigger it then.

**383.4.** Some Conditions are commonly used and structured in a way that explicitly defines their use and
other properties of the Effect that is associated with it.

**383.4.a.** Play Effects are Triggered Abilities whose Condition includes the Permanent that has the
Play Effect being played to the board.

**383.4.a.1.** These are commonly structured as “When you play me…” for Units and “When you
play this…” for Gear.

**383.4.a.2.** These Triggered Abilities are put on the Chain as Pending Items after the
Permanent these effects correspond to is finalized and enters the board.

**383.4.a.3.** These Triggered Abilities can be referred to as Play Effects.

**383.4.a.4.** Abilities that trigger when another object is played are not considered Play Effects.
**383.4.b.** Targeting Effects are Triggered Abilities whose Condition includes a Game Object
becoming targeted.

**383.4.b.1.** These are commonly structured as “When you choose me …” or “When you choose
a [Game Object] …”

**383.4.b.2.** These Triggered Abilities are put on the Chain as Pending Items after a spell or
ability that targets an appropriate Game Object is Finalized.

**383.4.b.3.** Although these abilities say “choose” in their Condition, they trigger specifically
when an appropriate Game Object is Targeted.
See rule 355.6. Targeting for more information on what counts as
Targeting.

**383.4.b.4.** These Triggered Abilities can be referred to as Targeting Effects.

**383.4.c.** Conquer Effects are Triggered Abilities whose Condition includes a Unit participating in,
and successfully Conquering a Battlefield.

**383.4.c.1.** These are commonly structured as “When I conquer…” and “When you conquer…”

**383.4.c.2.** This category of Triggered Abilities encompasses only those that are triggered
from Units that were present during the Conquer action, or Abilities that reference
the player that performed the Conquer action.

383.4.c.2.a.                    The Conquer Abilities of Units are put on the Chain as Pending Items
after the Unit(s) these effects correspond to are present at a Battlefield
when a player gains control of it and gains 1 Victory Point from
Conquering.

383.4.c.2.b.                    The Conquer Abilities of anything that references the player Conquering
is put on the Chain as a Pending Item when the Condition that the player
that controls the triggering source has performed a Conquer and gained 1
Victory Point.

383.4.c.2.c.                    If the act of gaining one point from Conquering is negated or replaced in
any way, the Conquer Effect will still trigger.

**383.4.c.3.** These Triggered Abilities can be referred to as Conquer Effects.

**383.4.d.** Hold Effects are Triggered Abilities whose Condition includes a Unit being present at a
Battlefield during the Beginning phase when a player scores Victory Points from Holding.

**383.4.d.1.** These are commonly structured as “When I hold…” or “When you hold…”

**383.4.d.2.** This category of Triggered Abilities encompasses only those that are triggered
from Units that were present during the Hold action, or Abilities that reference the
player that performed the Hold action.

383.4.d.2.a.                    The Hold Abilities of Units are put on the Chain as Pending Items after
the Unit these effects correspond to are present at a Battlefield when a
player maintains control of it and Gains 1 Victory Point during their
Beginning Phase from Holding.

383.4.d.2.b.                    The Hold Abilities of anything that references the player Holding is put on
the Chain as a Pending Item when the Condition that the player that
controls the triggering source has performed a Hold and gained 1 Victory
Point.

383.4.d.2.c.                    If the act of gaining one point from Holding is negated or replaced in any
way, the Hold Effect will still trigger.
**383.4.d.3.** These Triggered Abilities can be referred to as Hold Effects.

**383.4.e.** Attack Triggers are Triggered Abilities that trigger when a Unit or Player gains the
Attacker designation for the first time during a combat.

**383.4.e.1.** These are commonly structured as “When I attack…” or “When you attack…”

**383.4.e.2.** These Triggered Abilities are put on the Chain as Pending Items after the Unit
these effects correspond to gains the Attacker designation during Combat.

383.4.e.2.a.                                      These triggers will only have their condition checked once per combat,
despite a Unit being able to gain and lose the Attacker designation
multiple times in the same combat.

383.4.e.2.b.                                      If the trigger condition contains other requirements besides attacking and
if those requirements are not fulfilled when the unit gains the Attacker
designation, it will not trigger in that combat.

**383.4.e.3.** These Triggered Abilities can be referred to as Attack Triggers.

**383.4.f.** Defend Triggers are Triggered Abilities that trigger when a Unit or Player gains the
Defender designation for the first time during a combat.

**383.4.f.1.** These are commonly structured as “When I defend…” or “When you defend…”

**383.4.f.2.** These Triggered Abilities are put on the Chain as Pending Items after the Unit
these effects correspond to gains the Defender designation during Combat.

383.4.f.2.a.                                      These triggers will only have their condition checked once per combat,
despite a Unit being able to gain and lose the Defender designation
multiple times in the same combat.

383.4.f.2.b.                                      If the trigger condition contains other requirements besides defending
and if those requirements are not fulfilled when the unit gains the
Defender designation, it will not trigger in that combat.

**383.4.f.3.** These Triggered Abilities can be referred to as Defend Triggers.

**383.4.g.** Some effects may instruct a player to “activate” one of these named triggered abilities.

**383.4.g.1.** To do so, that player checks the condition of all of the specified effects, as if they
had fulfilled the named part of the condition.
Example: Reckoner’s Arena reads “When you hold here, activate the
conquer effects of units here.” For each unit at the battlefield, you will
check the trigger condition of their conquer effects to see if the condition
has been fulfilled, treating the conquer portion of the condition as having
been fulfilled. If all of the conditions are fulfilled for a conquer effect, it is
placed on the chain as if it had just triggered. If any of the non-conquer
parts of the condition are not fulfilled, it will not be placed on the chain.

Example: A spell reads “Activate the play effects of your gear.” For each
gear you control, you will treat it as if you had just played the gear and
check the other conditions of that gear. If all of the conditions are fulfilled
for a play effect, it is placed on the chain as if it had just triggered.

**384.** Presence on Permanents

**384.1.** Typically active while on the Board.

**384.2.** Triggered Abilities of Permanents are only able to have their Conditions evaluated while on the
Board.
**385.** Presence on Cards outside of the Board

**385.1.** Triggered Abilities on cards outside of the Board rely on the Information Level of the zone they are
in.

**385.2.** Triggered Abilities outside of the Board will self-describe their context.
Example: The triggered ability "When you conquer, you may discard 1 to return this from
your trash to your hand." triggers while the card it's on is in the trash, and not anywhere else.

## Mecánicas relacionadas

- [[mechanics/play-trigger|Triggers al jugar]]
- [[mechanics/triggered-ability|Triggered abilities]]
