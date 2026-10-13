---
title: "446. Copy"
id: "rule-section:446"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "9205b79a8e986ca801905396a4cfa8ffa0ff973ee04cae0281d7693f05fea716"
generated: true
confidence: "official"
---

# 446. Copy

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**446.1.** Copying a Game Object is the act of adding or replacing some or all of the copyable traits of another
Game Object with those of the Copied Game Object.

**446.2.** Copy Effects are rendered in the Copy Effects layer.
See rule 475. Layers for more information.

**446.3.** Some Game Objects may be created as a Copy of another Game Object. This is not a Copy Effect.
The Copy in such a case is rendered with the same copyable traits as those of the Game Object it is a
Copy of. It has no printed traits of its own that are subsequently replaced.
Example: Zilean, Time Mage is a unit that reads “Once each turn, if you would play a token
unit while I'm at a battlefield, you may play that token and an additional copy of it instead.”
The additional copy played by Zilean’s replacement effect has no printed traits of its own. Its
printed traits are those of the token it is a copy of.

**446.4.** Copy is a Limited Action.

**446.4.a.** Players may only Copy Game Objects when directed to by Game Effects.

**447.** Movement
**448.** Moving is a Limited Action.

**448.1.** A Permanent changing its position from any space on the Board to another space on the Board is a
Move, unless it is caused by a corrective Recall or an Attached Permanent changing locations to or
with its Top-Most Card.
See rule 421. Move for more information.

**448.2.** A card changing game zones does not in itself constitute a Move.

**448.3.** Moving is instantaneous.

**448.3.a.** There is no state for Permanents between locations.

**448.3.b.** Permanents are either at their Origin before Moving or their Destination after Moving.

**448.3.c.** Moving does not use the Chain, nor is it able to be Reacted to.

**449.** Moving is defined by the Origin and Destination of the Permanent that is changing locations.

**449.1.** The Origin is where the Permanent is starting from.

**449.2.** The Destination is where the Permanent is going to.

**449.2.a.** In Modes of Play with more than two players, Battlefields with Staged Combats or
Combats in Progress are Invalid Destinations for Moves of all kinds (Standard Moves or
otherwise) by Units controlled by Players not involved in those Combats or who don't
already have units at that Battlefield.

**449.2.b.** In Modes of Play with teammates, Battlefields occupied by a player’s teammates are
Invalid Destinations for Moves of all kinds (Standard Moves or otherwise) by Units that
player controls.

**449.2.c.** If an action would require a Move that would cause a Unit to become present in a Location
where it cannot move for any reason, such as a Battlefield with two players that are not the
controller of the Unit performing this Move action are in a Combat or such a Combat is
Staged, it instead Recalls.
See rule 456. Recalls for more information.

**450.** Players may choose to move their Units with the Standard Move.
See rule 144. for more information on the Standard Move.

**451.** Spells, Abilities, or other effects may cause a Move to occur.

**451.1.** The source of the Move will provide details on any restrictions on legality for Destination.

**451.2.** Units cannot Move to a Battlefield that already has units from 2 other players present by any means.

## Mecánicas relacionadas

- [[mechanics/move|Move]]
