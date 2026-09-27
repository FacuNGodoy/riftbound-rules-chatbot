---
title: "818. Equip"
id: "rule-section:818"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "b60968f38a389b026f5502fcbd8d6bf9402abff92b2c474c642e87f8d8149cad"
generated: true
confidence: "official"
---

# 818. Equip

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**818.1.** Equip is an Activated Ability keyword.

**818.1.a.** Equip is present on Gear with the tag Equipment.

**818.1.b.** Equip has a cost to activate and Attaches the card with Equip to a chosen Unit when the
cost is paid.

**818.1.b.1.** Equip’s choice is a Target.

**818.1.b.2.** The chosen Unit will become the Top-Most Card for the Attach action.

**818.1.c.** Equip is formatted as “Equip [Cost]”

**818.1.c.1.** If paying costs or making choices for this ability causes triggered abilities to trigger,
they will be placed on the chain above this ability in a Pending state.
See rule 376. Activated Abilities for more information.

**818.1.c.2.** Equip is functionally short for “[Cost]: Attach this gear to a unit you control.”

**818.1.c.3.** Equip costs may include both resource costs and non-resource costs.

**818.1.c.4.** Equip abilities may also include text that alters the Equip cost. Such text is taken
into account when determining a card’s Equip cost when paying for the ability.

**818.1.c.5.** Equip abilities may include text that alters the timing or targeting of the Equip
ability.
**818.2.** When the Attach action completes from this keyword, the Unit that was chosen is considered to
have been Equipped by the Gear with this ability.

**818.2.a.** This is an event other Game Effects and Triggered Abilities can reference.

**818.3.** Equipped is the state of a Top-Most Card being Attached by one or more cards that are Equipment.

**818.3.a.** The state of being Equipped is synchronous with that of the Attached state of the
Equipment.

**818.3.b.** A Top-Most Card is Equipped as long as one or more of its Attached cards are Equipment.

**818.3.c.** The state of being Equipped corresponds to a Top-Most card having a card with Equip that
is Attached to it.

**818.4.** Multiple instances of Equip are equivalent to multiple Activated Abilities and can each be activated
separately by paying the corresponding costs.

**818.5.** Equip, and whether or not a Gear has Equip, is a characteristic of the Gear and may be checked or
referenced by other Game Effects.

**818.5.a.** Whether or not a Gear has Equip may be referenced even if the Rules Text of the Gear is
Inactive.
See rule 716. Attachment for more information.

## Mecánicas relacionadas

- [[mechanics/attach|Attach y Equipment]]
