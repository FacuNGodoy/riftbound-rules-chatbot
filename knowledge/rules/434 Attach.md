---
title: "434. Attach"
id: "rule-section:434"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "992fbfdb716cc8c14003a388f79ecd4259faee6356eea58b86fe7cd9c389916d"
generated: true
confidence: "official"
---

# 434. Attach

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**434.** Swap

**434.1.** Swapping is the act of increasing one numeric value and decreasing another numeric value on
some number of Game Objects such that their values are reversed.

**434.1.a.** Swapping creates two different effects that apply to each attribute. One that Increases one
value and one that Decreases the other. These effects last for the duration specified by the
effect that instructed the Swap.

**434.1.b.** To accomplish this, determine the difference between these values and then apply an
Increase for that amount to the lower value of the two attributes, and a Decrease of that
amount to the higher value of the two attributes.

**434.1.c.** If both attributes are the same numeric value, Swapping has no effect.

**434.1.d.** If the attributes being swapped are Units’ Mights, this effect is the equivalent to giving
those units a Might increasing effect and a Might decreasing effect respectively.

**434.2.** Swapping is a Limited Action.

**434.2.a.** Players may only swap when Game Effects direct them to do so.

## Mecánicas relacionadas

- [[mechanics/attach|Attach y Equipment]]
