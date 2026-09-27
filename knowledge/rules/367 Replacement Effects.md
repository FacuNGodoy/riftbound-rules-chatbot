---
title: "367. Replacement Effects"
id: "rule-section:367"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "aa7eb9d99897d5b61cc474e64751a8a0460ed8919ef201c67f23f2faf20fe622"
generated: true
confidence: "official"
---

# 367. Replacement Effects

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**368.** An ability that alters the application of another game effect or game rule.

**368.1.** Passive Abilities can be Replacement Effects.

**369.** Replacement Effects intercede during the execution of a Game Effect and alter its execution.

**369.1.** A Replacement Effect can usually be identified by the presence of the terms “as,” “would,” or
"instead."
Example: Zhonya's Hourglass reads "The next time a friendly unit would die, kill this instead.
Heal that unit, exhaust it, and recall it." This is a replacement effect that alters the execution
of any Game Effect that would kill a friendly unit.

Example: Undertitan is a unit that reads in part “As I’m revealed from your deck, [Add] [2].”
This is a replacement effect that alters the execution of any Game Effect that reveals
Undertitan from your deck.

**369.2.** Some Game Actions are themselves Replacement Effects.
Example: Burning Out is a replacement effect.​
Example: Preventing Damage is a replacement effect.

**369.3.** Replacement Effects that apply to a unit as it enters the Board can be identified by describing how
the unit enters, or by describing a game action that occurs “as” a unit enters.
Example: Master Yi, Honed reads “I enter ready.” This applies a replacement effect to the way
that units normally enter. The event of him entering exhausted is replaced by one where he
enters ready.

Example: Baron Nashor reads “As you play me, add the Baron Pit battlefield token to the
board if it's not there already. If you do, I enter there.” The last sentence of his ability is a
replacement effect that replaces the event of him entering at his original play location with
him entering at the Baron Pit if it was created.

**370.** A Replacement Effect can alter the typical flow of play, including other cards' executions.

**370.1.** Replacement Effects apply to any event or instruction that qualifies for their application. A
Replacement Effect will specify the circumstances by which an event or instruction will qualify to be
replaced.

**370.1.a.** An event is the singular moment that results from a Game Action being performed or from
a Game Object changing state.
Example: The moment that results from a unit being killed is an event that can be
referenced by game effects, or even skipped entirely.

Example: The moment that results from a unit becoming Mighty is an event that
can be referenced by game effects, or even skipped entirely.

**370.1.a.1.** Modifying or replacing an event is the same as modifying or replacing that Game
Action or change in state that generated that event.
Example: Zhonya’s Hourglass reads in part “If a friendly unit would die, kill
this instead. Heal that unit, exhaust it, and recall it.” A unit’s death being
replaced by Zhonya’s Hourglass is the same as the kill action that caused
that death not occurring.

Example: A card reads in part “The next time an enemy unit would
become Mighty this turn, banish it instead. Its controller plays a 3 [M] Mech
unit token to its location.” A unit becoming Mighty being replaced by this
effect means the unit never became Mighty—no effects that trigger on
units becoming Mighty will trigger.

**370.1.a.2.** An event can occur simultaneously with other events only when those events are all
the result of the same Game Action or change in state occurring.
Example: A spell reads in part “Kill up to two units at battlefields.” When
that spell resolves, the units targeted are killed simultaneously because
their deaths result from the same game action.

Example: A spell reads in part “Kill a friendly unit. If you do, kill an enemy
unit with no more Might than it.” When that spell resolves, the units are
not killed simultaneously. There are two kill game actions being
performed in the instructions of the spell. The friendly unit is killed first,
followed by the enemy unit.

**370.1.b.** When a Replacement Effect applies, it replaces the qualifying event with one or more
Game Actions or events, or the qualifying instruction with another instruction.

**370.1.b.1.** In the case of Replacement Effects that describe a game action to occur “as” an
event occurs, the described event is replaced by that same event plus the game
action being performed.
Example: Undertitan is a unit that reads in part “As I’m revealed from your
deck, [Add] [2].” The event of Undertitan being revealed from your deck is
replaced by Undertitan being revealed from your deck and adding [2]
Energy to your Rune Pool.

**370.1.c.** Replacement Effects are applied before any qualifying event has actually occurred.
**370.2.** A Replacement Effect can only be applied once to an event, or to any Game Actions or events that
replace that event.
Example: A player plays a spell that reads “gear you control become 1 [M] gear units this
turn.” They control two copies of Zhonya’s Hourglass when the spell resolves. If one of those
copies is killed, both of their Replacement Effects will be applied. Whichever is applied first,
that Replacement Effect can’t be applied again. When it is applied, it kills its source, which
creates an event the other can apply its Replacement Effect to. Once they’ve both applied
their Replacement Effect to the original death event and the event that replaced it, they
cannot go any further. At that point, whichever Zhonya’s Hourglass applied its Replacement
Effect last will die.

**370.3.** If a Game Object has a Replacement Effect that is active in a specific zone, it is evaluated and
subsequently applied if it enters that zone before an event occurs that it could replace.
Example: A unit that reads “if a unit you control would die, you may banish me from your
trash instead. If you do, heal that unit, exhaust it and recall it.” The first unit dies
simultaneously with a 1 [M] Recruit token. It does not enter the trash before the Recruit dies,
so it will not be able to replace its death.

**370.4.** A Game Object can apply its Replacement Effects to any qualifying events that occur
simultaneously with it leaving the zone that its Replacement Effect is active in.
Example: Soraka, Wanderer has a Replacement Effect that reads, “If another unit you control
here would die, if it has less Might than me, instead heal it, exhaust it, and recall it.” Soraka’s
replacement can be applied to any qualifying event that occurs simultaneously with her
leaving the board, including to units that die simultaneously with her.

**371.** Some Replacement Effects will begin with “once each turn,” or “N times each turn.”

**371.1.** These Replacement Effects may only be applied to the specified number of events each turn. Once
they have been applied to that many events, they cannot be applied to a later event in the same turn.

**371.2.** If the Replacement Effect says a player “may” apply the Replacement Effect, the player has the
choice of whether or not to apply it.

**371.2.a.** When an event the Replacement Effect could apply to occurs, the player who controls the
Replacement Effect may choose to apply it to the event.

**371.2.b.** If they do not, it has not been applied this turn.
Example: Zilean, Time mage reads “Once each turn, if you would play a token unit
while I'm at a battlefield, you may play that token and an additional copy of it
instead.” When his controller plays a token, they can choose not to apply the
replacement effect to that event. If they do, they can choose to apply it to a later
event of a token being played.

**372.** If more than one Replacement Effect applies to the same event being executed, then the controller of the
object being acted on determines the order the Replacement Effects will apply.

**372.1.** If it is a player being acted on, that player decides the order the Replacement Effects will apply.

**372.2.** If the affected object is an Uncontrolled Battlefield then the Current Turn Player decides the order
the Replacement Effects will apply.

**373.** If more than one event occurs simultaneously that Replacement Effects could apply to, each event is treated
separately and individually for the purposes of Replacement Effects, and Replacement Effects with the same
controller are applied in the order of their controller’s choosing.
Example: Two units controlled by the same player die in the same cleanup. That player also controls
Zhonya’s Hourglass. They must decide which event to apply Zhonya’s Hourglass to first.

**373.1.** Although these events are simultaneous, the applied Replacement Effects are ordered. If multiple
applied Replacement Effects with different controllers would execute simultaneously, they execute
in turn order.
**373.1.a.** When executing Replacement Effects, the Game Actions that comprise their instructions
are performed before any simultaneous unmodified events.
Example: Two units die simultaneously. One of those units has their death replaced
by being healed, exhausted, and recalled. The healing, exhausting, and recalling of
that unit will be performed before the other dies.

**373.2.** When applying Replacement Effects to events that occur simultaneously, each Replacement Effect
may only be applied in one sequence, to any number of events that are qualified to be replaced.
Example: Soraka, Wanderer reads “If another unit you control here would die, if it has less
Might than me, instead heal it, exhaust it, and recall it.” Soraka dies simultaneously with two 1
[M] Recruit tokens at the same battlefield and two 1 [M] Recruit tokens in base. Soraka has a
Guardian Angel attached to her when she dies, which appends “If I would die, kill Guardian
Angel instead. Heal me, exhaust me, and recall me” to Soraka’s rules text. There are several
possible ways to order the Replacement Effects being applied to the various events: If
Soraka’s Replacement Effect is applied first, it saves the Recruits at the same battlefield as
her but not the Recruits in base. If the Replacement Effect appended by Guardian Angel
then saves Soraka, she cannot apply her Replacement Effect to the Recruits in base as her
Replacement Effect has already been applied to an event simultaneous with it dying. If the
Replacement Effect appended by Guardian Angel is applied first, it saves Soraka and recalls
her - then when Soraka’s Replacement Effect is applied, it can only save the Recruits in base.

**373.2.a.** A sequence of Replacement Effects is an uninterrupted series of applications to a set of
simultaneous events.

**373.2.a.1.** A Replacement Effect that replaces an event or Game Action that is part of another
Replacement Effect will not interrupt the sequence of the replaced Replacement
Effect’s application.

**374.** A Replacement Effect’s controller is the player that controls the source of the Replacement Effect.

**375.** If an event that a Replacement Effect applies to would be modified by the Game Effect that generated that
event, or the results of that event would be modified by a Game Action from a linked ability that references
the replaced event, the Replacement Effect will inherit those modifications.
Example: Treasure Hunter reads “When I move, play a Gold gear token exhausted.” A Replacement
Effect that says “if you would play a token gear, play that token and an additional copy instead” is
applied to the event of the Gold gear token being played. The additional copy will also be exhausted,
as it inherits the “exhausted” modification.

Example: Another Replacement Effect says “if you would play a token, draw 1 instead.” The
modification from Treasure Hunter’s ability cannot apply, so we ignore it.

Example: A spell reads “play a ready 3 [M] Mech token. Then do this: Give it Temporary.” A
Replacement Effect that says “if you would play a unit token, play that token and a 1 [M] Recruit token
instead” is applied to the event of the Mech token being made. The Recruit token enters ready and is
given Temporary.

## Mecánicas relacionadas

- [[mechanics/replacement|Replacement effects]]
