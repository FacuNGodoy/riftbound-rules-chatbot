---
title: "420. Move"
id: "rule-section:420"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "370bf4233bc5d919ef77b756947c967664d6a605f03992f86b208f09c8f1bbf7"
generated: true
confidence: "official"
---

# 420. Move

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**420.** Play

**420.1.** A player Plays cards by placing them on the chain and queuing them to be finalized.
See rule 349. Playing Cards for more information on playing cards.
See rule 337. Finalize for more information on finalizing cards.

**420.1.a.** By default, a player can only Play cards from their hand or their Chosen Champion zone.

**420.2.** This is a Discretionary Action.

**420.2.a.** As long as a player has the resources to pay the costs associated with the card and legal
choices to make for their cards, they may Play cards.

**420.3.** Game effects may result in cards being Played as part of their resolution.

**420.3.a.** This treats Play as a Limited Action.

**420.3.b.** Treat all steps of Play as normal, except as noted by the game effect instructing this Limited
Play Effect.

**420.3.b.1.** Such game effects may specify choices or effects such as alternate costs, ignored
costs, play locations, targets, or other choices or effects normally made or
processed during Finalization.

**420.3.b.2.** Such game effects may specify those choices or effects based on the condition of
the board. If they do so, that information is checked on finalization of the resulting
Game Object, unless it is specified as being checked earlier.
Example: Bone Skewer is a spell that reads in part “Choose a battlefield.
An opponent reveals their hand. You may choose a unit from it. They play
that unit to that battlefield, ignoring any and all costs.” The chosen
battlefield isn’t checked on finalization of the resulting game object but
when the spell itself is resolving.

Example: A spell reads in part “Play a unit from your trash to an enemy
occupied battlefield, ignoring its Energy cost.” On finalization, they can
choose any enemy occupied battlefield to play the unit to. If no such
battlefield exists as the unit is being finalized, it will fail to finalize.

Example: Rek’Sai, Swarm Queen is a unit that reads “When I attack, you
may reveal the top 2 cards of your Main Deck. You may banish one, then
play it. If it is a unit, you may play it here. Recycle the rest.” The attack
trigger adds a permission to the normal valid locations for the played unit,
that being “here.” The “here” in Rek’Sai’s ability is a referent, whose
information is checked when the ability resolves. As such, it will not check
on finalization of the unit being played.

**420.3.c.** If there are no eligible cards to Play when instructed to Play in this manner, then nothing
happens and resolution continues.

**420.4.** Some Abilities trigger when cards are played or otherwise check whether cards have been played.

**420.4.a.** Any such triggered abilities trigger when the act of playing the card has been completed by
the resolution of the card.

**420.4.a.1.** If a game effect prevents the resolution of the card—for example, because the card
was countered—abilities that trigger on playing cards will not trigger.
See rule 426. Counter for more information.

**420.4.b.** Non-triggered abilities and conditional clauses that check cards being played do so by
means of referencing whether said cards have been Finalized.
Example: A player plays a spell, which is countered by Defy. Any Legion abilities of
game objects controlled by that same player will be active.

Example: A player plays a spell, which is countered by Defy. If that player plays
Battering Ram and has played no other cards that turn, it will cost [4] Energy.

**420.5.** If an effect refers to a card being played and doesn’t do so by means of checking whether cards were
played, it refers to the card being added to the chain and queued for Finalization, that is, the Play
Game Action.
Example: Astral Heron is a unit that reads “When you play your first card each turn, if I'm at a
battlefield, the next card you play this turn costs [2][A][A] less.” This effect applies a discount
to the next card the play game action, discretionary or limited, is performed on.

## Mecánicas relacionadas

- [[mechanics/move|Move]]
