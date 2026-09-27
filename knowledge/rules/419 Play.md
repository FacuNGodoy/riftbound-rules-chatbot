---
title: "419. Play"
id: "rule-section:419"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "1a0b0fbc0764a06a7ea0823474316c9bce77b08a9b7798623d2d1b0aea27f7e3"
generated: true
confidence: "official"
---

# 419. Play

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**419.1.** A player Plays cards by placing them on the chain and queuing them to be finalized.
See rule 349. Playing Cards for more information on playing cards.
See rule 337. Finalize for more information on finalizing cards.

**419.1.a.** By default, a player can only Play cards from their hand or their Chosen Champion zone.

**419.2.** This is a Discretionary Action.

**419.2.a.** As long as a player has the resources to pay the costs associated with the card and legal
choices to make for their cards, they may Play cards.

**419.3.** Game effects may result in cards being played as part of their resolution.

**419.3.a.** This treats Play as a Limited Action.

**419.3.b.** Treat all steps of Play as normal, except as noted by the game effect creating this Limited
Play Effect.

**419.3.c.** If there are no eligible cards to Play when instructed to Play in this manner, then nothing
happens and resolution continues.

**419.4.** Some Abilities trigger when cards are played or otherwise check whether cards have been played.

**419.4.a.** Any such triggered abilities trigger when the act of playing the card has been completed by
the resolution of the card.

**419.4.a.1.** If a game effect prevents the resolution of the card—for example, because the card
was countered—abilities that trigger on playing cards will not trigger.
See rule 425. Counter for more information.

**419.4.b.** Non-triggered abilities that check cards being played do so by means of referencing
whether said cards have been Finalized.
Example: A player plays a spell, which is countered by Defy. Any Legion abilities of
game objects controlled by that same player will be active.

Example: A player plays a spell, which is countered by Defy. If that player plays
Battering Ram and has played no other cards that turn, it will cost [4] Energy.

## Mecánicas relacionadas

- [[mechanics/play|Play]]
- [[mechanics/play-trigger|Triggers al jugar]]
- [[mechanics/counter|Counter]]
