---
title: "438. Replace"
id: "rule-section:438"
kind: "rule-section"
tags: ["riftbound", "knowledge/rule"]
source: "docs/core_rules.md"
source_hash: "d2ae25a142d5fb3de3e2feae910ff0d8967ba1624b9df3e49983707fd7445db7"
generated: true
confidence: "official"
---

# 438. Replace

> [!NOTE] Fuente oficial
> Sección extraída de `docs/core_rules.md`.

**438.** Prevent

**438.1.** Preventing damage is the act of reducing the Damage a set of game objects would take.

**438.1.a.** Prevent is an action that interacts with Damage.

**438.1.a.1.** Prevent includes any applied Bonus Damage when determining the total damage
being prevented.

**438.1.b.** Prevent appears in statements that define an amount of damage and the source of the
damage it will affect, as well as the timespan it will be relevant for.

**438.1.b.1.** Prevent actions are usually formatted as “Prevent the next X [source] damage
that would be dealt to a [unit] this turn.”

438.1.b.1.a.                                         The X is referred to as the Prevent Value.

438.1.b.1.b.                                         X can be “All,” which specifies an infinite amount of damage.

**438.1.b.2.** Prevent will always apply to the next damage that would be dealt to a unit
affected by the Prevent action.

**438.2.** When damage is Prevented, it is replaced with an event where the source of the damage deals that
much damage reduced by the Prevent Value tracked on the Unit specifically.

**438.2.a.** The damage being dealt as a result of Preventing can never be less than 0, but can be 0.
This is equivalent to not dealing damage.
**438.3.** When damage is dealt this way, reduce the Prevent Value being tracked on the Unit affected by the
Prevent action by the prevented amount.

**438.3.a.** If the Prevent Value is 0 or less, then Prevent is no longer being tracked on the Unit in
question, and the effect expires.

**438.3.b.** The reduced value is the newly tracked Prevent Value.

**438.3.c.** If the Prevent Value is “All” then it remains “All.”

**438.4.** Damage dealt to a Unit that has that all of that damage Prevented is not considered to have been
dealt to it at all.

**438.5.** Damage can still be assigned to Units in combat that are affected by Prevent. The damage dealt as
a result of that assignment will be affected by the Prevent action.

**438.5.a.** Damage can be assigned to a Unit up to a value that would be Lethal considering the
Prevent Value of all Prevent Actions on a Unit, following the normal rules for damage
assignment.
Example: A unit with 2 [M] is being assigned damage in the combat damage step.
The unit has “prevent the first 3 damage I would take each combat.” The unit
would need to be assigned 5 damage in order to have lethal damage assigned to
it.

**438.5.b.** No amount of damage is ever considered lethal if the Prevent Value is “All.”

**438.6.** Prevent is a Limited Action.

**438.6.a.** Players may only Prevent Damage when directed to by Game Effects.

**438.7.** Prevent is a Delayed Replacement Effect.
See rule 367. Replacement Effects for more information.
See rule 390. Delayed Abilities for more information.

## Mecánicas relacionadas

- [[mechanics/replacement|Replacement effects]]
