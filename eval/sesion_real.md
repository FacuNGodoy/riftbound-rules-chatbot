# Log de sesión real — Riftbound Rules Chatbot

Fecha: 2026-08-27.  
Origen: corrida de `eval/run_eval.py` contra el servidor local (no datos sintéticos inventados para el PDF).  
Configuración: draft Gemini Flash (cadena 3.7 → 3.6 → 3.5 → preview → lite); verifier Flash-Lite.

Resumen del pipeline LLM: **5/7 casos OK (71,4 %)**. El caso 8 lo resuelve código determinístico (Hidden Blade + Zhonya) y no pasa por el modelo.

---

## Caso 3 — Hidden + Kennen (OK)

**Usuario:** Si juego de Hidden a Kennen, Keeper of Balance, ¿puede stunear cualquier battlefield?

**Sistema:**
- Veredicto: NO · Confianza: ALTA
- Reglas citadas: 811.1

**Respuesta (extracto):** No. Si jugás a Kennen, Keeper of Balance desde Hidden, debés elegir una unidad en el mismo battlefield donde fue jugado. Según 811.1.d.2, si el efecto de juego de un permanente oculto elige targets, estos deben elegirse entre las opciones en ese battlefield.

---

## Caso 4 — Repeat + Defy (OK)

**Usuario:** Si counterean (Defy) un spell con Repeat, ¿se puede usar el Repeat igual?

**Sistema:**
- Veredicto: NO · Confianza: ALTA
- Reglas citadas: 820.1

**Respuesta (extracto):** Repeat ejecuta las instrucciones una vez adicional durante la resolución (820.1.d). Si el hechizo es countereado, no hay resolución: no se ejecuta el Repeat.

---

## Caso 5 — Nidalee, Cat Form (OK)

**Usuario:** Si Nidalee, Cat Form muere en combate pero quedan unidades en el battlefield, ¿roba igual?

**Sistema:**
- Veredicto: NO · Confianza: ALTA

**Respuesta (extracto):** El texto dice “I win if I remain after combat”. I = esta carta (no el jugador). Si muere, no permanece: no roba.

---

## Caso 7 — Deathknell vs Combat Cleanup (OK)

**Usuario:** Windswept Hillock. Defiendo con Ruined Rex y Glasc Mixologist. El rival ataca con Master Yi, Tempered (5 Might) y Steel Paws empowered (9 Might). Disputa: ¿Deathknell se resuelve antes o después del heal?

**Sistema:**
- Veredicto: INFORMATIVO · Confianza: ALTA
- Reglas citadas: 320 (y Cleanup 466 / 323)

**Respuesta (extracto):** Deathknell **triggerea** antes del heal (pending item en Cleanup) pero **se resuelve después**. Durante Cleanup la chain no puede finalizarse (regla 320). Yi se cura y después recibe 4: sobrevive.

---

## Caso 8 — Hidden Blade + Zhonya (atajo determinístico)

**Usuario:** Si le tiro Hidden Blade a una unidad enemiga y tiene Zhonya's Hourglass, ¿roba igual?

**Sistema:** SI · ALTA. No llama a Gemini: `deterministic_ruling()` cubre el caso ya validado (reemplazo ≠ mistarget; 359.3.e.14).

---

## Casos que no cerraron del todo

- Caso 1 (Tail-Cloaked Matriarch + Rhasa): veredicto NO correcto, pero el grader pidió citar la regla 206 (coste impreso) y el modelo argumentó por 366.2.a.
- Caso 6 (Flame Chompers en showdown): el verifier se abstuvo (`NO_RESUELTO`) pidiendo 355/464; el runner igual lo marca OK porque citó esas reglas y el caso no tiene veredicto SI/NO.

El JSON completo está en `eval/results_run1_backup.json`.
