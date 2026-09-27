---
title: "716. Attachment"
id: "rule-section:716"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "e2fc96c42c9e65044e0b5e34b3badbe33f4fa24eb828c3243f184069cbf85081"
generated: true
confidence: "official"
---

# 716. Attachment

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**717.** Attaching is a limited action that causes cards to become linked to each other to combine their effects in
some way. This causes one card to become Attached and the other to become A Top-Most Card.
See rule 434. Attach for more information.
**718.** Attached is the state of a card being linked to another card in this way.

**718.1.** A card remains in this state until Detached.

**718.2.** While in this state, the card’s printed Rules Text is Inactive.
See rule 720. Inactive for more information.

**718.3.** While in this state, Abilities in the card’s Effect Text are appended to the Rules Text of the Top-Most
Card.

**718.4.** While in this state, the card’s Might Bonus modulates the Top-Most Card’s Might by the value listed.

**718.5.** Attached cards still have all properties of being a card on the board while in this state.

**718.5.a.** Attached cards still have all Types and Tags while Attached.

**718.5.b.** Attached cards still can be chosen or targeted by game effects while Attached.

**718.5.c.** Attached cards cannot be moved separately from the Top-Most Card they are Attached
to.

**718.5.d.** A card may be Attached only to a single Top-Most card at a time.

**718.5.e.** Attached cards may have different Controllers from their Top-Most card.

**718.5.f.** Changes in Control of the Top-Most card do not impact Control of Attached cards and vice
versa.

**718.5.g.** An Attached card still appends the abilities in its Effect Text to the Rules Text of the
Top-Most card and modulates the Top-Most Card’s Might by its Might Bonus.

**719.** A Top-Most Card is a card that has one or more cards linked to it through the process of Attaching.

**719.1.** The Effect Text of all cards Attached to this card are appended to the Rules Text of this card for as
long as they remain Attached.

**719.2.** This card ceases being a Top-Most Card when there are no longer any cards Attached to it.

**719.3.** A Top-Most Card and all cards Attached to it are at the same location.

**719.3.a.** When the Top-Most Card changes locations, all Attached cards change locations with it.

**719.4.** The Exhausted and Ready state of the Top-Most card does not affect nor change the status of the
Attached cards and vice versa.

**719.4.a.** This is true of all statuses aside from location, Attached, and Top-Most.
Example: If the top-most card becomes stunned, it does not affect the state of any
attached cards.

Example: If an attached card becomes empowered, it does not affect the state of
its top-most card.

**719.5.** When a Top-Most Card changes zones from a board zone to a non-board zone, all Attached cards
Detach from it, remaining in their current zones.

**719.5.a.** The player that controls the Top-Most Card that changed zones decides the order these
cards Detach in, and thus the order of any relevant effects that occur due to the Detach
occurring.

## Mecánicas relacionadas

- [[mechanics/attach|Attach y Equipment]]
