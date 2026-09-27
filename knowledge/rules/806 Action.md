---
title: "806. Action"
id: "rule-section:806"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "43a94f2e1e0bfd7f79c93123d733d87e521544f57592694c39e29e42fcd15eb6"
generated: true
confidence: "official"
---

# 806. Action

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**806.1.** Action is a Permissive keyword.

**806.1.a.** It is present on Cards, Rune Abilities, Legend Abilities or Permanent Abilities.

**806.1.b.** Action grants the corresponding card or effect permission to be played or activated during
Showdowns, even when it is not the Controlling player's turn.

**806.1.c.** Action is functionally short for the following:
**806.1.c.1.** On Cards: "This can be played during showdowns on any player's turn."

**806.1.c.2.** On Activated Abilities: "This can be activated during showdowns on any player's
turn."

**806.1.d.** Action is formatted as “[Action]” on spells, or “[Action][>]” on abilities.

**806.2.** The card or effect with this keyword is not restricted to showdowns. This permission is inclusive of all
other timings and options available to the ability as written or by default.

**806.3.** Action does not alter the function of any instruction of the corresponding card or effect it is on. It is
only permission.
Example: Playing a Unit with Action still has the inherent restrictions of playing Units
without Action. It can only be played to the controlling player's base or a battlefield they
control.

**806.4.** Some passive abilities may grant a card or ability Action under certain conditions. The card or ability
does not have the Action keyword unless and until those circumstances are true.

**806.4.a.** Those conditions might only be fulfilled while the card or ability is on the chain. In such a
case, it can still be played or activated at the appropriate timing as long as doing so could
fulfill the conditions.

**806.4.b.** If the chain item does not fulfill the conditions by the time step 5: check legality has been
reached, the actions taken while playing it are undone and it is returned to the zone it was
played from if it is a card.

**806.5.** Action is a referenceable characteristic.

**806.5.a.** Whether or not a Game Object has Action is a characteristic of that Game Object and may
be checked or referenced by other Game Effects.

**806.5.b.** Whether or not a Spell has Action is a characteristic of that Spell and may be checked or
referenced by other Game Effects.

**806.5.c.** Whether or not an Ability has Action is a characteristic of that Ability and may be checked
or referenced by other Game Effects.

## Mecánicas relacionadas

- [[mechanics/action|Action]]
