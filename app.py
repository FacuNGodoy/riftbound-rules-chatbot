"""
Backend FastAPI: recibe preguntas (con imágenes opcionales),
busca contexto en ChromaDB, genera respuestas con Qwen via Ollama.
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
import json as json_mod
from pathlib import Path
import base64
import json
import os
import re
import time
from dotenv import load_dotenv
import chromadb
from google import genai
from google.genai import types
from embeddings import make_embedding_function

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

CHROMA_DIR = BASE_DIR / "chroma_db"
STATIC_DIR = BASE_DIR / "static"
CARDS_FILE = BASE_DIR / "cards.json"
COLLECTION_NAME = "riftbound_rules"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not GEMINI_API_KEY:
    raise RuntimeError(
        "Falta GEMINI_API_KEY. Copiá .env.example a .env y pegá la clave."
    )
VISION_ENABLED = os.environ.get("RIFTBOUND_VISION", "1").strip().lower() not in (
    "0",
    "false",
    "no",
    "off",
)
if VISION_ENABLED:
    import ollama
GEMINI_MODEL = "gemini-3.7-flash"
# Cada modelo tiene su propia cuota diaria (RPD). Si se agota uno, se pasa al siguiente.
# El draft necesita el razonamiento más fuerte: Flash primero (20 RPD cada uno),
# con un Lite al final como red de seguridad (500 RPD).
DRAFT_MODELS = [
    GEMINI_MODEL,
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.5-flash-lite",
]
# El verifier contrasta el borrador contra evidencia ya provista y devuelve JSON:
# tarea más mecánica. Los Lite tienen 500 RPD, así que no compiten por la cuota escasa.
VERIFIER_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.6-flash",
]
# Correr la suite de evaluación gasta cuota de draft (1 request por caso) y los Flash
# tienen 20 RPD. Para iterar sobre prompts o retrieval sin quemarla, se puede levantar
# el server apuntando el draft a los Lite (500 RPD):
#   RIFTBOUND_DRAFT_MODELS="gemini-3.5-flash-lite,gemini-3.1-flash-lite" uvicorn app:app
# El número que va al informe se mide siempre con la cadena por defecto.
_draft_override = os.environ.get("RIFTBOUND_DRAFT_MODELS", "").strip()
if _draft_override:
    DRAFT_MODELS = [name.strip() for name in _draft_override.split(",") if name.strip()]
    print(f"DRAFT_MODELS override activo: {DRAFT_MODELS}")

VISION_MODEL = "minicpm-v"
MODEL_TIMEOUT_SECONDS = 150

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
TOP_K = 12

SYSTEM_PROMPT = """Sos un asistente experto en las reglas del juego de cartas Riftbound.
Reglas de respuesta:
- Respondé siempre en español.
- Sé breve y directo para preguntas simples (2-3 oraciones). Para preguntas complejas de timing, combate o interacciones entre múltiples cartas, respondé con todo el detalle necesario paso a paso.
- Toda conclusión debe estar respaldada por reglas o texto de cartas presentes en el contexto. No inventes números de regla.
- Si faltan datos del estado de juego, la identidad exacta de una carta o reglas relevantes, decí explícitamente que no podés resolverlo con suficiente confianza y pedí solo los datos faltantes.
- Si el usuario presenta dos interpretaciones (la suya vs un rival/amigo), evaluá ambas contra las reglas. NO le des la razón por default.
- ANTES de razonar una interacción, verificá que CADA jugada descrita sea legal según el texto de las cartas involucradas: permiso de timing, ubicación válida, coste, y restricciones propias de la carta. Que el usuario la describa no la vuelve legal.
- [Action] dice "Play on your turn or in showdowns": NO habilita jugar en respuesta a un spell o ability que ya está en la chain. [Reaction] dice "Play any time, even before spells and abilities resolve": esa SÍ habilita responder dentro de la chain (806, 813.1.c.1, 331.1.a).
- Si una de las jugadas descritas no es legal, decilo explícitamente ANTES que el resto y respondé sobre el escenario corregido. Es un error grave dar un ruling sobre una secuencia que no puede ocurrir.
- Trigger ≠ resolve. Agregar un Pending Item a la chain no es resolverlo.
- Si la pregunta es sobre una carta específica, SIEMPRE mencioná la carta por nombre y citá la parte relevante de su texto. Ejemplo: "Nidalee dice '(I win if I remain after combat)', así que si muere no permanece y no roba."
- NO des respuestas genéricas sobre "una unidad" o "una carta" cuando sabés cuál es la carta.
- Para un ruling, citá los números de regla relevantes. Las citas serán verificadas contra el contexto.
- Si no tenés la info en el contexto, decilo.

Vocabulario TCG (usá estos términos, NO los traduzcas):
- counter/countereado (no "contado" ni "contrarestado")
- buff, nerf, tap, exhaust
- draw/robar (no "rob")
- stack, chain
- play, cast
- target, targetear

Reglas de interpretación de cartas:
- "I"/"me" en el texto de una carta = esta carta específica, NO el jugador (regla 053).
  Ejemplo: si una carta dice "When I win a combat" significa cuando ESTA CARTA gana un combate, no cuando el jugador gana.
- El texto entre paréntesis en una carta define o aclara la mecánica. Es vinculante, no decorativo.
  Ejemplo: "(I win if I remain after combat.)" significa que esta carta solo gana si ELLA sigue viva después del combate. Si muere durante el combate, no ganó, y sus efectos de victoria no se activan.
- "Can't beats Can" (regla 054): lo que prohíbe supera a lo que permite.
- Hacé "lo máximo posible" ignorando instrucciones imposibles (regla 055).
- Tomáte tu tiempo para razonar paso a paso cuando la pregunta involucre interacciones complejas de combate o timing.
- En combate, las unidades reciben daño y si su vida llega a 0, mueren. Una unidad muerta ya no está en el tablero y no puede cumplir condiciones que requieran que permanezca.

Reglas de jugar unidades (regla 355):
- Para jugar una unidad, necesitás una ubicación válida: tu base o un battlefield que controles (355.2.a).
- Algunas cartas pueden expandir o restringir las ubicaciones válidas (355.2.b).

Targets y elecciones (regla 355.5 a 355.12, 337):
- PROHIBIDO argumentar que algo "no targetea porque la carta no dice target". NINGUNA carta de Riftbound imprime la palabra "target". El targeting es IMPLÍCITO y lo define el reglamento, no el wording de la carta.
- 355.7: si una carta elige uno o más Game Objects específicos para afectar, ESO ES un target, salvo las excepciones de 355.10.
- Frases como "a unit", "another friendly unit", "any number of your token units", "move X to this battlefield" son targets.
- Excepciones (NO targetean): zona no pública como la mano (355.10.a), restricciones de otra elección (355.10.b), costos/condición de trigger/efectos de reemplazo (355.10.c), selección programática sin elección posible como "all units" o "your legend" (355.10.d), elecciones que hacen otros jugadores (355.10.e), instrucciones con "must" (355.10.f).
- CUÁNDO se eligen: los targets se eligen al FINALIZAR el ítem en la chain (355.8, 337), durante el paso 2 "Make relevant choices" (355). NO se eligen al resolver.
  - 355.8: para poner un spell o ability en la chain, hay que hacer elecciones válidas para TODOS los targets.
  - 355.11.a: los grupos tipo "any number of" se eligen al finalizarse en la chain.
  - 355.12: si un efecto dice que "podés" hacer una acción sobre N objetos, esas elecciones igual son targeted y se eligen aparte de la decisión de hacer la acción.
  - 355.4: si el efecto mueve unidades, también elegís la ubicación destino en ese momento.
- Consecuencia práctica: cuando declarás una habilidad disparada (ej. "When I attack, you may move any number of your token units to this battlefield"), al finalizarla en la chain YA tenés que anunciar qué unidades movés. El rival reacciona SABIENDO esas elecciones. No podés esperar a la resolución para decidirlas.
- 355.5.b: al finalizar el ítem que CAUSA un trigger no elegís los targets de ese trigger; los elegís cuando esa habilidad disparada se finaliza en la chain (que sigue siendo antes de resolverla).
- Sí se elige al resolver únicamente en los casos de 355.10.e y 355.10.f (elecciones de otros jugadores, o instrucciones "must") y en 355.11.b (reelegir un subconjunto legal si el grupo dejó de cumplir la restricción).

¿Se puede jugar la carta si no hay objetos válidos? (355.8 vs 355.10, 055)
- Si la carta TARGETEA: necesitás hacer elecciones válidas para TODOS los targets para poder poner el spell o la ability en la chain (355.8). Si no hay ningún objeto válido, no podés jugarla.
  Ejemplo: "Kill a unit at a battlefield" targetea una unidad. Si no hay ninguna unidad legal en un battlefield, no se puede jugar.
  Caso Hidden: 811.1.d dice explícitamente que una carta no se puede jugar desde Hidden si es un spell sin targets válidos bajo esas restricciones.
- Si la carta NO TARGETEA (excepciones de 355.10.d, 355.10.e, 355.10.f): SÍ podés jugarla aunque no haya objetos para afectar. Se resuelve y se hace lo máximo posible (055, 359.3.e.11). Si nada es posible, igual se juega y se resuelve, pero no pasa nada (055.1).
  Ejemplo clave: "Each player kills one of their units" (Cull the Weak) NO targetea las unidades, porque es un conjunto elegido en parte por otros jugadores (355.10.e). Cada jugador elige su unidad AL RESOLVER. Por eso podés jugarla incluso sin tener unidades propias: vos simplemente no matás nada y el rival sí. Tampoco targetea a los jugadores, porque "each player" es selección programática sin elección posible (355.10.d).
- Regla práctica para distinguir: si el efecto lo elegís VOS y son objetos específicos → target → hace falta objetivo válido para jugarla. Si lo elige cada jugador, o dice "must", o es "all X" → no target → se elige al resolver y la carta es jugable igual.

Reglas de atacante/defensor (regla 464):
- El atacante es el jugador cuyas unidades aplicaron contested status al battlefield (se movieron ahí). El atacante NO controla ese battlefield.
- El defensor es el jugador que ya controlaba el battlefield. El defensor SÍ controla ese battlefield.
- Por lo tanto: si estás atacando, NO podés jugar unidades al battlefield en disputa (no lo controlás). Si estás defendiendo, SÍ podés.
- Esto aplica a CUALQUIER efecto que juegue una unidad (desde mano, descarte, etc): si no tenés ubicación válida, no podés jugarla ahí.

Orden de Combat Cleanup (reglas 465-466, 320, 323):
1. Se asigna y se inflige daño de combate simultáneamente (465.2). Asignar NO es infligir (465.2.c.1).
2. Se salta FEPR, se va directo al Resolution Step (465.3).
3. Se invoca Combat Special Cleanup (466.1):
   - 3a. Unidades con lethal damage que tienen Deathknell u otras triggered abilities por muerte propia: el trigger se AGREGA como Pending Item al Chain (323.4). La unidad aún no fue al trash.
   - 3b. Esas unidades con lethal damage mueren y van al trash (323.5).
   - 3c. Se CURAN TODAS las unidades sobrevivientes (466.1.a.1). Todo el daño marcado se remueve.
   - 3d. Se recallan atacantes si quedan defensores (466.1.a.2).
   - REGLA CRÍTICA (320): Mientras un Cleanup está ocurriendo, los Chain Items NO pueden finalizarse ni resolverse. Solo se pueden agregar nuevos Pending Items (320.1).
4. Recién cuando TERMINA el Cleanup, los Pending Items (como Deathknell) se finalizan y resuelven.
- CONCLUSIÓN: Deathknell TRIGGEREA antes del heal (paso 3a), pero se RESUELVE después del heal (paso 4). Las unidades sobrevivientes ya están curadas cuando el Deathknell hace su efecto.
- NUNCA digas que Deathknell se resuelve "de inmediato" o "antes del heal". Eso es INCORRECTO. Siempre seguí el orden descrito arriba.
- 143.3.b.2 solo dice CUÁNDO se cura (durante el Combat Cleanup). NO significa que Deathknell ya se resolvió. El heal es el paso 3c de ESE Cleanup; el Deathknell se resuelve recién cuando el Cleanup termina.

Ejemplo concreto de Deathknell + Combat Cleanup:
- Unidad A (con Deathknell "Deal 4 to an enemy unit") recibe lethal damage en combate.
- Unidad B sobrevive el combate con 3 de daño marcado sobre 5 Might.
- Combat Cleanup paso 3a: Deathknell de A TRIGGEREA y queda como Pending Item.
- Combat Cleanup paso 3b: A muere y va al trash.
- Combat Cleanup paso 3c: Se CURAN TODAS las unidades. B pasa de 3 daño a 0 daño.
- Termina el Cleanup. Regla 320 deja de bloquear resoluciones.
- Ahora se resuelve el Deathknell de A: B recibe 4 de daño. Como B tiene 5 Might y 0 daño previo (fue curada), B queda con 4 daño → B SOBREVIVE.
- Si dijeras que Deathknell se resuelve ANTES del heal, B tendría 3+4=7 daño sobre 5 Might y moriría. Eso es INCORRECTO."""

# Setup
app = FastAPI(title="Riftbound Chatbot")

ef = make_embedding_function()
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)


conversation_history: list[dict] = []
MAX_HISTORY = 10

# Cargar base de datos de cartas
CARDS_DB: list[dict] = []
CARDS_BY_NUMBER: dict[str, dict] = {}
CARDS_BY_NAME: dict[str, list[dict]] = {}

CARDS_BY_TAG: dict[str, list[dict]] = {}

if CARDS_FILE.exists():
    CARDS_DB = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    for card in CARDS_DB:
        if card.get("card_number"):
            CARDS_BY_NUMBER[card["card_number"]] = card
        name_lower = card.get("name", "").lower()
        CARDS_BY_NAME.setdefault(name_lower, []).append(card)
        # Indexar por tags (ej: "Draven", "Noxus")
        for tag in card.get("tags", []):
            CARDS_BY_TAG.setdefault(tag.lower(), []).append(card)
        # Indexar por primera parte del nombre (antes de la coma)
        if "," in name_lower:
            short_name = name_lower.split(",")[0].strip()
            CARDS_BY_NAME.setdefault(short_name, []).append(card)
        # Indexar por primera palabra para nombres sin coma (ej: "Rhasa the Sunderer" → "rhasa")
        words = name_lower.split()
        if len(words) > 1 and "," not in name_lower:
            first_word = words[0]
            if len(first_word) >= 3:
                CARDS_BY_NAME.setdefault(first_word, []).append(card)
    print(f"Cargadas {len(CARDS_DB)} cartas desde {CARDS_FILE}")


def find_card(card_number: str = "", name: str = "", energy: str = "", might: str = "") -> dict | None:
    """Busca una carta por número, o por nombre + stats como fallback."""
    if card_number and card_number in CARDS_BY_NUMBER:
        return CARDS_BY_NUMBER[card_number]
    name_lower = name.lower().strip()
    candidates = CARDS_BY_NAME.get(name_lower, [])
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1 and (energy or might):
        for c in candidates:
            if energy and c.get("energy") == energy:
                if might and c.get("might") == might:
                    return c
            if energy and c.get("energy") == energy:
                return c
        return candidates[0]
    return None


def format_card_info(card: dict) -> str:
    """Formatea la info de una carta para el contexto del LLM."""
    parts = [f"Carta: {card['name']}"]
    if card.get("card_number"):
        parts.append(f"Número: {card['card_number']}")
    if card.get("type"):
        parts.append(f"Tipo: {card['type']}")
    if card.get("domains"):
        parts.append(f"Dominios: {', '.join(card['domains'])}")
    if card.get("tags"):
        parts.append(f"Tags: {', '.join(card['tags'])}")
    stats = []
    if card.get("energy") and card["energy"] != "0":
        stats.append(f"Energy {card['energy']}")
    if card.get("power") and card["power"] != "0":
        stats.append(f"Power {card['power']}")
    if card.get("might") and card["might"] != "0":
        stats.append(f"Might {card['might']}")
    if stats:
        parts.append(f"Stats: {', '.join(stats)}")
    if card.get("effect_text"):
        if card.get("rules_text"):
            parts.append(f"Rules Text (activo solo mientras NO esté attacheada): {card['rules_text']}")
        parts.append(
            "Effect Text (inactive mientras no esté attacheada; al attachear se appendea al "
            "Rules Text de la carta de arriba y el Rules Text propio se vuelve inactive, 136.2.c). "
            "Ojo: en esta sección \"I\"/\"me\" refieren a la carta de arriba, no a esta carta; "
            "para referirse a esta carta se usa \"this\" o su nombre propio (136.2.d): "
            f"{card['effect_text']}"
        )
        if card.get("might_bonus"):
            parts.append(f"Might Bonus (se aplica a la carta de arriba): {card['might_bonus']}")
    elif card.get("description"):
        parts.append(f"Texto: {card['description']}")
    return "\n".join(parts)


def identify_card_from_image(image_bytes: bytes) -> str:
    """Usa visión para identificar la carta y busca datos precisos en la DB."""
    if not VISION_ENABLED:
        return (
            "En esta versión publicada no hay reconocimiento por foto. "
            "Escribí el nombre o el número de la carta (ej. Defy, OGN-045)."
        )
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    try:
        response = ollama.chat(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": """Look at this Riftbound card and tell me ONLY these 3 things, nothing else:
1. Card number (bottom left corner, format like OGN-006, SFD-115, VEN-088, etc.)
2. Card FULL name: read BOTH the main name AND the subtitle below it. Cards have a big name (e.g. "Kennen") and a smaller subtitle below (e.g. "Keeper of Balance"). Combine them as "Name, Subtitle" (e.g. "Kennen, Keeper of Balance"). If there is no subtitle, just write the main name.
3. Energy cost (number in the top left circle)

Reply in this exact format:
NUMBER: xxx
NAME: xxx
ENERGY: xxx""",
                "images": [b64],
            }],
        )
    except Exception as exc:
        print(f"VISION ERROR: {type(exc).__name__}: {exc}")
        return (
            "No pude leer la imagen: el modelo de visión local (Ollama / minicpm-v) "
            "no está disponible. Escribí el nombre o el número de la carta (ej. OGN-195)."
        )
    vision_text = response["message"]["content"]

    # Parsear respuesta del vision model
    card_number = ""
    card_name = ""
    energy = ""
    m = re.search(r'NUMBER:\s*([A-Z]+-\d+)', vision_text)
    if m:
        card_number = m.group(1)
    m = re.search(r'NAME:\s*(.+)', vision_text)
    if m:
        card_name = m.group(1).strip()
    m = re.search(r'ENERGY:\s*(\d+)', vision_text)
    if m:
        energy = m.group(1)

    # Buscar en la DB
    card = find_card(card_number=card_number, name=card_name, energy=energy)
    if card:
        return format_card_info(card)

    # Fallback: devolver lo que leyó el vision model
    return f"Carta identificada por visión (no encontrada en DB):\n{vision_text}"


NAME_STOPWORDS = {"the", "of", "and", "de", "del", "la", "el", "los", "las"}


def disambiguate_by_subtitle(name: str, candidates: list[dict], text_lower: str) -> list[dict]:
    """Resuelve 'Azir Sovereign' aunque el nombre real sea 'Azir, Sovereign'.

    Compara las palabras del nombre completo que no están en el nombre corto matcheado.
    """
    matched = []
    for card in candidates:
        extra = card.get("name", "").lower().replace(name, " ")
        tokens = [
            t for t in re.split(r"\W+", extra)
            if len(t) >= 3 and t not in NAME_STOPWORDS
        ]
        if tokens and all(
            re.search(rf"(?<!\w){re.escape(t)}(?!\w)", text_lower) for t in tokens
        ):
            matched.append(card)
    return matched if len(matched) == 1 else candidates


def find_cards_in_text(text: str) -> tuple[list[dict], list[str]]:
    """Busca nombres o números de cartas mencionadas en el texto. Retorna (cartas, notas de ambigüedad)."""
    found = []
    seen_numbers = set()
    ambiguities = []

    # 1. Buscar por número de carta (ej: SFD-185, OGN-006)
    for m in re.finditer(r'(OGS|OGN|SFD|UNL|VEN)-(\d{1,3})', text, re.IGNORECASE):
        card_id = f"{m.group(1).upper()}-{int(m.group(2)):03d}"
        if card_id in CARDS_BY_NUMBER and card_id not in seen_numbers:
            found.append(CARDS_BY_NUMBER[card_id])
            seen_numbers.add(card_id)

    # 2. Buscar por nombre
    text_lower = text.lower()
    # Detectar si el usuario especifica un tipo para filtrar
    type_filter = ""
    for t in ["legend", "leyenda", "champion", "signature spell", "unit", "unidad", "spell", "hechizo", "gear", "rune", "battlefield"]:
        if t in text_lower:
            type_filter = {
                "legend": "Legend", "leyenda": "Legend",
                "champion": "Champion Unit",
                "signature spell": "Signature Spell",
                "unit": "Unit", "unidad": "Unit",
                "spell": "Spell", "hechizo": "Spell",
                "gear": "Gear", "rune": "Rune", "battlefield": "Battlefield",
            }.get(t, "")
            break

    sorted_names = sorted(CARDS_BY_NAME.keys(), key=len, reverse=True)
    for name in sorted_names:
        name_pattern = re.compile(rf"(?<!\w){re.escape(name)}(?!\w)")
        if name_pattern.search(text_lower):
            candidates = CARDS_BY_NAME[name]
            # Si hay filtro de tipo y hay múltiples candidatos, filtrar
            if type_filter and len(candidates) > 1:
                filtered = [c for c in candidates if c.get("type", "").lower() == type_filter.lower()]
                if filtered:
                    candidates = filtered
            if len(candidates) > 1:
                candidates = disambiguate_by_subtitle(name, candidates, text_lower)
            new_candidates = [c for c in candidates if c["card_number"] not in seen_numbers]
            # Detectar ambigüedad
            if len(new_candidates) > 1:
                options = []
                for c in new_candidates:
                    domains = ", ".join(c.get("domains", []))
                    options.append(f"{c['name']} ({domains}, {c.get('type', '')})")
                ambiguities.append(
                    f"Se encontraron {len(new_candidates)} cartas para '{name}': {'; '.join(options)}. "
                    f"Preguntale al usuario a cuál se refiere, mencionando el dominio/color de cada una."
                )
            for card in new_candidates:
                found.append(card)
                seen_numbers.add(card["card_number"])
            text_lower = name_pattern.sub("", text_lower)
    return found, ambiguities


def detect_category(query: str) -> list[str]:
    """Detecta la categoría de la pregunta para filtrar chunks."""
    q = query.lower()
    if any(w in q for w in ["ban", "legal", "prohibid", "permitid", "baneada", "baneado"]):
        return ["legality", "rules"]
    if any(w in q for w in ["torneo", "tournament", "judge", "juez", "penalty", "penalidad", "sancion"]):
        return ["tournament"]
    return ["rules"]


HIDDEN_BLADE_CARD_NAME = "hidden blade"

TARGETING_TRIGGERS = [
    "target", "targetea", "targetear", "elegir", "eleccion", "elijo",
    "anunciar", "enunciar", "declarar", "choose", "cuando ataco",
    "when i attack", "trigger", "prioridad", "reaccion",
    "each player", "cada jugador", "cull the weak",
    "no tengo unidades", "sin unidades", "no hay unidades",
]

# Los triggers de arriba sirven para retrieval: traer reglas de más es barato.
# El pinned de targeting es otra cosa: inyecta 2.4k caracteres de "RULING OBLIGATORIO"
# en el prompt del draft. Con la lista completa alcanzaba con que la pregunta dijera
# "trigger" o "reacciona" para dispararlo, y le imponía un marco de targeting a
# preguntas de permisos o timing que no tienen nada que ver con elecciones.
# Para el pinned exigimos vocabulario de targeting propiamente dicho.
TARGETING_PINNED_EXCLUDED = {"trigger", "prioridad", "reaccion"}
TARGETING_PINNED_TRIGGERS = [
    token for token in TARGETING_TRIGGERS if token not in TARGETING_PINNED_EXCLUDED
]

ATTACHMENT_TRIGGERS = [
    "equip", "equipment", "gear", "attach", "atach",
    "quick-draw", "quickdraw", "weaponmaster", "might bonus", "effect text",
]

KEYWORD_ENRICHMENT = {
    "jugar|play|jugarlo|jugarla|invocar": "play unit valid location battlefield base",
    "atacar|attack|atacando|attacker": "attacker contested status control battlefield",
    "defender|defend|defendiendo|defensor": "defender control battlefield",
    "descart|discard": "discard play unit valid location",
    "hide|hidden|esconder|facedown": "hide hidden facedown battlefield keyword 421 811",
    "stun|stunear|stunned": "stun stunned combat damage unit",
    "exhaust|tap|exhausted": "exhaust exhausted ready tap",
    "equip|equipment|gear|attach|atach": "equip equipment gear attach attached top-most card inactive rules text effect text appended might bonus 135.4 136.2 137.3",
    "reaction|reaccion": "reaction play respond chain",
    "combat|combate|pelea": "combat damage showdown attacker defender cleanup resolution heal 465 466",
    "deathknell|deathkneel|knell": "deathknell when I die pending item cleanup 323.4 808 320 cannot be finalized resolved heal all units",
    "cleanup|curan|curacion|se curan": "combat cleanup heal all units 466.1 320 323 lethal damage",
    "move|mover|movimiento": "move unit battlefield base location",
    "kill|matar|morir|muere|muerte": "kill die destroy unit combat damage lethal",
    "buff|bonus|might": "might bonus buff increase unit",
    "counter|countere|contrarrest": "counter spell ability negate",
    "conquer|conquist": "conquer control battlefield contested",
    "recall|recycle": "recall recycle base hand unit",
    "shield|escudo": "shield damage prevent combat",
    "deflect": "deflect passive ability keyword additional cost power target choose opponent spells abilities deflect value granted summed 809 349",
    "tank|backline": "tank backline damage assignment combat",
    "repeat": "repeat spell additional cost effect",
    "target|targetear|targetea|elegir|elijo|eleccion|anunciar|enunciar|declarar|choose": "targeting choose targets valid choices finalize chain make relevant choices 355.7 355.8 355.10 355.11 355.12 337",
    "chain|prioridad|priority|responder|reaccionar": "chain pending item finalize priority FEPR make relevant choices 337 338",
    "when i attack|cuando ataco|trigger|triggered|dispara": "triggered ability pending item finalize chain choices 355.5.b 382 337",
    "zhonya|zhonyas|hourglass": "replacement effect would die instead linked instruction Hidden Blade draws 2 359.3.e.14",
    HIDDEN_BLADE_CARD_NAME: "Kill a unit Its controller draws 2 linked instruction replacement Zhonya mistarget",
}

# Búsquedas extra que fuerzan las reglas clave cuando el retrieval semántico se desvía.
MECHANIC_QUERIES = [
    {
        "match": ["deathknell", "deathkneel", "knell"],
        "queries": [
            "Deathknell When I die Pending Item before the card is moved to the trash 808",
            "323.4 Units with Lethal Damage Deathknell trigger add Pending Item",
            "While a Cleanup is occurring Chain Items cannot be Finalized or Resolved 320",
            "Combat Special Cleanup insert Heal all Units 466.1 Skip the FEPR process 465.3",
        ],
    },
    {
        "match": ["cleanup", "se curan", "curacion", "curan las", "heal all"],
        "queries": [
            "Combat Special Cleanup Heal all Units 466.1",
            "While a Cleanup is occurring Chain Items cannot be Finalized or Resolved 320",
        ],
    },
    {
        "match": TARGETING_TRIGGERS,
        "queries": [
            "When a card Chooses one or more specific Game Objects to affect it is Targeted 355.7",
            "In order to put a spell or ability on the chain valid choices must be made for all targets 355.8",
            "As they are finalized on the chain such cards can choose any group of valid targets 355.11",
            "If a spell specifies that a player may perform a Game Action on some number of Game Objects all choices are considered targeted 355.12",
            "Make relevant choices step 2 process of play choose valid location move destination 355.4",
            "Step 1 Finalize the controller of the oldest Pending Chain Item must finalize 337.1",
            "This does not include making choices for Triggered Abilities the target will be chosen when the ability triggers 355.5.b",
            "Each player kills a unit they control does not target chooses as the spell resolves 355.10.e",
            "When executing card text do as much as you can ignoring impossible instructions 055",
        ],
    },
    {
        "match": ["zhonya", "zhonyas", "hourglass", HIDDEN_BLADE_CARD_NAME],
        "queries": [
            "Hidden Blade Kill a unit Its controller draws 2 linked instruction replacement 359.3.e.14",
            "If the Game Action performed in an earlier linked instruction is replaced later linked instruction",
            "Zhonya's Hourglass If a friendly unit would die kill this instead replacement",
        ],
    },
    {
        "match": ATTACHMENT_TRIGGERS,
        "queries": [
            "A card's printed Rules Text is Inactive while that card is Attached to another card 135.4",
            "Effect Text is inactive unless the card with the Effect Text is Attached to another card 136.2.b",
            "The abilities in the Effect Text section are appended to the Rules Text of the card it is Attached to 136.2.c",
            "Effect Text may refer to this or to the name of the Attached game object 136.2.d",
            "A card's Might Bonus modulates the Might of the card to which it is Attached 137.3",
            "Equip keyword pay the Equip cost choose a unit you control attach the Equipment",
            "Deflect Opponents must pay to choose me with a spell or ability 809",
        ],
    },
]

# Marcadores de reglas que el embedding suele perder. Se inyectan por texto exacto.
CRITICAL_RULE_MARKERS = {
    "**320.**": ["deathknell", "deathkneel", "knell", "cleanup", "curan", "curacion"],
    "**323.4.**": ["deathknell", "deathkneel", "knell", "cleanup", "lethal", "muere", "muerte", "curan"],
    "**465.3.**": ["deathknell", "deathkneel", "knell", "combat", "combate", "cleanup", "curan"],
    "**466.1.a.1.**": ["deathknell", "deathkneel", "knell", "curan", "cleanup", "heal", "curacion"],
    "**808.1.**": ["deathknell", "deathkneel", "knell"],
    "**359.3.e.14.**": ["zhonya", "zhonyas", "hourglass", HIDDEN_BLADE_CARD_NAME, "linked"],
    "**055.**": TARGETING_TRIGGERS,
    "**355.5.**": TARGETING_TRIGGERS,
    "**355.7.**": TARGETING_TRIGGERS,
    "**355.8.**": TARGETING_TRIGGERS,
    "**355.10.**": TARGETING_TRIGGERS,
    "**355.11.**": TARGETING_TRIGGERS,
    "**355.12.**": TARGETING_TRIGGERS,
    "**337.1.**": TARGETING_TRIGGERS,
    "**135.4.**": ATTACHMENT_TRIGGERS,
    "**136.2.b.**": ATTACHMENT_TRIGGERS,
    "**136.2.c.**": ATTACHMENT_TRIGGERS,
    "**136.2.d.**": ATTACHMENT_TRIGGERS,
    "**137.3.**": ATTACHMENT_TRIGGERS,
    "**809.1.**": [*ATTACHMENT_TRIGGERS, "deflect"],
}


def build_critical_index() -> dict[str, list[tuple[str, dict]]]:
    index: dict[str, list[tuple[str, dict]]] = {marker: [] for marker in CRITICAL_RULE_MARKERS}
    got = collection.get(include=["documents", "metadatas"])
    for doc, meta in zip(got["documents"], got["metadatas"]):
        if meta.get("source") != "core_rules":
            continue
        for marker in index:
            if marker in doc:
                index[marker].append((doc, meta))
    return index


CRITICAL_INDEX = build_critical_index()

PINNED_RULINGS = [
    {
        "match": ["deathknell", "deathkneel", "knell"],
        "text": """RULING OBLIGATORIO (no lo contradigas, no le des la razón al usuario si choca con esto):

Las dos lecturas comunes son incorrectas en un punto:
- "Primero se curan y DESPUÉS triggerean los Deathknell" → FALSO.
- "Los Deathknell triggerean, se RESUELVEN, y después se curan" → FALSO.

Correcto: los Deathknell TRIGGEREAN antes del heal y se RESUELVEN después del heal.
Durante el Combat Cleanup la chain NO se puede resolver (regla 320). El heal de 143.3.b.2 es el paso 3c de ese Cleanup, no un momento posterior a resolver Deathknell.

En el caso típico (Rex Deathknell Deal 4 vs una unidad que sobrevivió combate con daño marcado, p.ej. Master Yi 5 Might con 3 de daño):
1. Daño de combate. Rex lethal. Yi sobrevive dañado.
2. Cleanup 3a: Deathknell de Rex queda Pending. No se resuelve.
3. Cleanup 3b: Rex muere.
4. Cleanup 3c: Yi se CURA a 0 daño.
5. Termina el Cleanup.
6. Se resuelve Deathknell: 4 daño a Yi ya curado → 4/5 → SOBREVIVE.

NUNCA respondas "vos tenés la razón" si el usuario dice que Deathknell se resuelve antes de curar.
NUNCA digas que Yi muere por el Deathknell de Rex en ese escenario.""",
    },
    {
        "match_groups": [
            [HIDDEN_BLADE_CARD_NAME],
            ["zhonya", "zhonyas", "hourglass"],
        ],
        "text": """RULING OBLIGATORIO — Kill linked vs reemplazo vs mistarget (regla 359.3.e.14):

Hidden Blade: "Kill a unit at a battlefield. Its controller draws 2."
Son instrucciones linked. El draw NO dice "If you do".

Dos situaciones distintas:
1) REEMPLAZO (Zhonya's Hourglass): la unidad SÍ sería killed; Zhonya reemplaza el die con heal + exhaust + recall. El kill se considera ejecutado. El draw SÍ ocurre (359.3.e.14.b). El rival ROBÁ 2.
2) MISTARGET (Flash, Retreat, mover la unidad a base/mano ANTES de que Hidden Blade resuelva): la primera instrucción se ignora. El draw NO ocurre (359.3.e.14.a).

NUNCA trates Zhonya como si Hidden Blade perdiera el target. Zhonya no saca la unidad de target: reemplaza el evento de muerte.
Deathgrip es distinto: dice "If you do", así que si Zhonya reemplaza el kill, el "If you do" falla.""",
    },
    {
        "match": TARGETING_PINNED_TRIGGERS,
        "text": """RULING OBLIGATORIO — targeting y momento de las elecciones:

1. NINGUNA carta de Riftbound imprime la palabra "target". El targeting es implícito y lo define el reglamento (355.7), no el wording de la carta. Está PROHIBIDO usar "la carta no dice target" como argumento. Si escribís eso, la respuesta es inválida.
2. Elegir Game Objects específicos = targetear (355.7). "A unit", "another friendly unit", "any number of your token units" son targets. Solo NO targetean las excepciones de 355.10 (zona no pública como la mano, restricciones, costos, condición de trigger, efectos de reemplazo, "all X", elecciones de otros jugadores, instrucciones "must").
3. Las elecciones se hacen al FINALIZAR el ítem en la chain, en el paso "Make relevant choices" (355, 355.8, 337). NO al resolver.
4. "Any number of" también se elige al finalizar (355.11.a). Un "you may" no posterga la elección: sigue siendo targeted y se elige ahí (355.12).
5. Si el efecto mueve unidades, la ubicación destino también se elige en ese momento (355.4).
6. Por lo tanto, en una habilidad disparada tipo "When I attack, you may move any number of your token units to this battlefield": al finalizar el trigger en la chain YA declarás cuáles y cuántas unidades movés. El rival responde conociendo esas elecciones. NO se decide en la resolución.
7. 355.5.b aclara solamente que al finalizar el ítem que CAUSA el trigger no elegís por el trigger; esas elecciones se hacen cuando la habilidad disparada se finaliza, que igual es ANTES de resolverla.
8. Se elige al resolver únicamente en 355.10.e (elige otro jugador), 355.10.f (instrucción "must") y 355.11.b (reelegir subconjunto legal si el grupo dejó de cumplir la restricción).
9. LEGALIDAD DE JUGAR: si la carta targetea, necesitás al menos una elección válida para ponerla en la chain (355.8); sin objeto válido NO se puede jugar. Si la carta NO targetea (355.10.d/e/f), se puede jugar igual aunque no haya nada que afectar: se resuelve haciendo lo máximo posible (055, 359.3.e.11) y si nada es posible no pasa nada (055.1).
10. Ejemplo obligatorio: "Each player kills one of their units" (Cull the Weak) NO targetea unidades (355.10.e: conjunto elegido en parte por otros jugadores) y cada jugador elige al resolver. Se puede jugar SIN tener unidades propias. Tampoco targetea a los jugadores (355.10.d, selección programática). En cambio "Kill a unit at a battlefield" SÍ targetea una unidad y sin unidad legal no se puede jugar.""",
    },
]


def query_is_combat_heal_timing(query: str) -> bool:
    """Detecta preguntas de Deathknell vs heal, incluso con typos."""
    q = query.lower()
    if any(token in q for token in ["deathknell", "deathkneel", "death knell", "knell"]):
        return True
    heal = any(token in q for token in ["curan", "cura", "heal", "curacion"])
    combat = any(token in q for token in ["combate", "combat", "daño", "danio"])
    trigger = any(token in q for token in ["trigere", "trigger", "se resuelven", "surviving"])
    return heal and combat and trigger


def get_pinned_ruling(query: str) -> str:
    q = query.lower()
    parts = []
    if query_is_combat_heal_timing(query):
        parts.append(PINNED_RULINGS[0]["text"])
    for item in PINNED_RULINGS:
        if item["text"] in parts:
            continue
        groups = item.get("match_groups")
        matches = (
            all(any(token in q for token in group) for group in groups)
            if groups
            else any(token in q for token in item.get("match", []))
        )
        if matches:
            parts.append(item["text"])
    return "\n\n".join(parts)


def enrich_search_query(query: str) -> str:
    """Agrega términos de búsqueda extra para mejorar el retrieval."""
    q = query.lower()
    extra = []
    for keywords, enrichment in KEYWORD_ENRICHMENT.items():
        if any(w in q for w in keywords.split("|")):
            extra.append(enrichment)
    if extra:
        return query + " " + " ".join(extra)
    return query


def retrieve_chunks(
    query: str, search_query: str, categories: list[str], cards: list[dict]
) -> tuple[list[str], list[dict]]:
    """Recupera chunks: primero reglas clave de la mecánica, después búsqueda semántica."""
    seen: set[str] = set()
    chunks: list[str] = []
    metadatas: list[dict] = []

    def add_results(docs: list[str], metas: list[dict]) -> None:
        for doc, meta in zip(docs, metas):
            key = doc[:240]
            if key in seen:
                continue
            seen.add(key)
            chunks.append(doc)
            metadatas.append(meta)

    # Las reglas de attachment casi nunca se nombran en la pregunta ("¿pago Deflect?"),
    # pero están implícitas en las cartas involucradas: un Gear con tag Equipment arrastra
    # 135.4/136.2/137.3 aunque el usuario no escriba "equipment".
    card_tokens = [t for c in cards for t in [c.get("type", ""), *c.get("tags", [])]]
    q = " ".join([query.lower(), *(t.lower() for t in card_tokens if t)])

    for marker, triggers in CRITICAL_RULE_MARKERS.items():
        if any(token in q for token in triggers):
            for doc, meta in CRITICAL_INDEX.get(marker, []):
                add_results([doc], [meta])

    extra_queries: list[str] = []
    for bundle in MECHANIC_QUERIES:
        if any(token in q for token in bundle["match"]):
            extra_queries.extend(bundle["queries"])

    if extra_queries:
        forced = collection.query(
            query_texts=extra_queries,
            n_results=2,
            where={"category": {"$in": categories}},
        )
        for docs, metas in zip(forced["documents"], forced["metadatas"]):
            add_results(docs, metas)

    results = collection.query(
        query_texts=[search_query],
        n_results=TOP_K,
        where={"category": {"$in": categories}},
    )
    paired = sorted(
        zip(results["documents"][0], results["metadatas"][0]),
        key=lambda item: 0 if item[1].get("source") == "core_rules" else 1,
    )
    add_results([doc for doc, _ in paired], [meta for _, meta in paired])

    return chunks[: TOP_K + 6], metadatas[: TOP_K + 6]


def merge_chunks(
    base: list[str],
    base_metas: list[dict],
    extra: list[str],
    extra_metas: list[dict],
) -> tuple[list[str], list[dict]]:
    """Une los chunks de una segunda búsqueda sin repetir los que ya estaban."""
    seen = {doc[:240] for doc in base}
    chunks, metadatas = list(base), list(base_metas)
    for doc, meta in zip(extra, extra_metas):
        key = doc[:240]
        if key in seen:
            continue
        seen.add(key)
        chunks.append(doc)
        metadatas.append(meta)
    return chunks, metadatas


RULE_ID_PATTERN = re.compile(
    r"(?:\*\*)?(\d{3}(?:\.(?:\d+|[a-z]))*)(?:\.\*\*|\.)"
)


def extract_rule_evidence(chunks: list[str], metadatas: list[dict]) -> dict[str, dict]:
    """Construye un catálogo de reglas que realmente están en el contexto."""
    evidence: dict[str, dict] = {}
    for chunk, meta in zip(chunks, metadatas):
        matches = list(RULE_ID_PATTERN.finditer(chunk))
        for index, match in enumerate(matches):
            rule_id = match.group(1)
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(chunk)
            rule_text = re.sub(r"\s+", " ", chunk[start:end]).strip()
            if not rule_text:
                continue
            current = evidence.get(rule_id)
            if current and len(current["text"]) >= len(rule_text):
                continue
            evidence[rule_id] = {
                "id": rule_id,
                "kind": "rule",
                "title": f"Regla {rule_id}",
                "source": meta.get("source", "core_rules"),
                "text": rule_text[:600],
            }
    return evidence


def build_evidence_catalog(
    chunks: list[str],
    metadatas: list[dict],
    cards: list[dict],
) -> dict[str, dict]:
    """Une reglas recuperadas y textos exactos de cartas."""
    evidence = extract_rule_evidence(chunks, metadatas)
    for card in cards:
        card_number = card.get("card_number", "")
        if not card_number:
            continue
        evidence[card_number] = {
            "id": card_number,
            "kind": "card",
            "title": card.get("name", card_number),
            "source": "cards.json",
            "text": card.get("description", "")[:600],
        }
    return evidence


def format_evidence_for_verifier(evidence: dict[str, dict]) -> str:
    lines = []
    for item in evidence.values():
        lines.append(
            f"[{item['id']}] {item['title']} | {item['source']}\n{item['text']}"
        )
    return "\n\n".join(lines)


def parse_json_response(text: str) -> dict | None:
    """Acepta JSON puro o envuelto en un bloque Markdown."""
    cleaned = text.strip()
    if cleaned.lower().startswith("```json"):
        cleaned = cleaned[7:].lstrip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:].lstrip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].rstrip()
    try:
        value = json.loads(cleaned)
        return value if isinstance(value, dict) else None
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end <= start:
            return None
        try:
            value = json.loads(cleaned[start:end + 1])
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            return None


def is_quota_error(exc: Exception) -> bool:
    text = str(exc).lower()
    if getattr(exc, "code", None) == 429:
        return True
    return (
        type(exc).__name__ == "ResourceExhausted"
        or "429" in text
        or "quota" in text
        or "resource_exhausted" in text
    )


def is_timeout_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return "timeout" in text or "deadline" in text


def is_retryable_error(exc: Exception) -> bool:
    """Cuota, timeout o error de servidor: vale la pena probar el siguiente modelo."""
    text = str(exc).lower()
    return is_quota_error(exc) or any(
        marker in text
        for marker in ("timeout", "deadline", "unavailable", "503", "504", "500")
    )


def is_model_unavailable_error(exc: Exception) -> bool:
    """404 del modelo: ese nombre ya no existe. No dice nada del resto de la cadena."""
    text = str(exc).lower()
    return getattr(exc, "code", None) == 404 or "404" in text or "not_found" in text


# Memoria de cuota: un 429 marca al modelo como agotado por un rato, así las
# siguientes preguntas no vuelven a gastar un intento en él. El cooldown es
# temporal (y no hasta medianoche) porque un 429 también puede venir del límite
# por minuto, que se recupera solo.
QUOTA_COOLDOWN_SECONDS = 900
quota_cooldown: dict[str, float] = {}


def model_available(model_name: str) -> bool:
    until = quota_cooldown.get(model_name)
    if until is None:
        return True
    if time.monotonic() >= until:
        del quota_cooldown[model_name]
        return True
    return False


def describe_model_failure(exc: Exception) -> str:
    """Traduce la falla del modelo para no confundir cuota con timeout."""
    name = type(exc).__name__
    text = str(exc).lower()
    if is_quota_error(exc):
        return (
            "Se agotó la cuota diaria de todos los modelos de Gemini configurados. "
            "La cuota se reinicia a medianoche del Pacífico (unas 4 AM en Argentina)."
        )
    if "timeout" in text or "deadline" in text:
        return f"El modelo no respondió dentro del tiempo límite ({MODEL_TIMEOUT_SECONDS}s)."
    return f"El modelo falló al responder ({name})."


def generate_with_fallback(
    prompt: str,
    system_instruction: str,
    history: list[dict] | None = None,
    models: list[str] | None = None,
) -> str:
    """Pide una respuesta probando cada modelo hasta que uno tenga cuota disponible."""
    chain = models or DRAFT_MODELS
    available = [name for name in chain if model_available(name)]
    if not available:
        print("Todos los modelos en cooldown por cuota, se reintenta la cadena igual")
        available = chain
    contents = [*(history or []), {"role": "user", "parts": [{"text": prompt}]}]
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        # El SDK nuevo pide el timeout en milisegundos.
        http_options=types.HttpOptions(timeout=MODEL_TIMEOUT_SECONDS * 1000),
    )
    last_exc: Exception | None = None
    for model_name in available:
        max_attempts = 2  # 1 intento + 1 retry ante timeout
        for attempt in range(max_attempts):
            try:
                response = gemini_client.models.generate_content(
                    model=model_name, contents=contents, config=config
                )
                # Ante un bloqueo por filtro de seguridad el SDK devuelve text=None en vez
                # de tirar excepción. Sin esto el None llegaría hasta el parser de JSON.
                if response.text is None:
                    raise RuntimeError(f"{model_name} no devolvió texto")
                if model_name != chain[0]:
                    print(f"MODELO ALTERNATIVO: respondió {model_name}")
                return response.text
            except Exception as exc:
                last_exc = exc
                if is_quota_error(exc):
                    quota_cooldown[model_name] = time.monotonic() + QUOTA_COOLDOWN_SECONDS
                    break  # no reintentar cuota, pasar al siguiente modelo
                if is_timeout_error(exc) and attempt < max_attempts - 1:
                    print(f"TIMEOUT en {model_name}, reintentando (intento {attempt + 2})")
                    continue  # retry en el mismo modelo
                # Un error del MODELO (no existe, sin cuota, timeout) no dice nada del
                # siguiente de la cadena: se sigue. Uno de la REQUEST (prompt inválido,
                # API key mala) va a fallar igual en todos, así que aborta.
                if is_retryable_error(exc) or is_model_unavailable_error(exc):
                    motivo = type(exc).__name__
                    detalle = str(exc).replace("\n", " ")[:160]
                    print(f"FALLO en {model_name} ({motivo}: {detalle}), probando el siguiente")
                    break  # pasar al siguiente modelo
                raise
    raise last_exc


def verify_ruling(
    query: str,
    draft: str,
    evidence: dict[str, dict],
) -> dict:
    """Segunda pasada: corrige el borrador y exige evidencia identificable."""
    verifier_prompt = f"""Actuá como revisor estricto de rulings de Riftbound.
Tu trabajo NO es defender el borrador: corregilo si contradice la evidencia.
Usá exclusivamente la evidencia enumerada. Trigger no significa resolve.

Procedimiento obligatorio, en este orden:
1. Construí el argumento MÁS FUERTE EN CONTRA de la conclusión del borrador,
   apoyándolo en la evidencia. Hacelo aunque el borrador te parezca correcto.
2. Verificá cada afirmación del borrador contra la evidencia: si una afirmación
   no se puede sostener con la evidencia listada, no vale, aunque suene razonable.
3. Evaluá si el contraargumento prevalece.
4. Recién entonces decidí. Si prevalece, cambiá el veredicto.

Pregunta:
{query}

Borrador:
{draft}

Evidencia permitida:
{format_evidence_for_verifier(evidence)}

Respondé SOLO JSON válido con esta forma:
{{
  "verdict": "SI|NO|RESUELTO|DEPENDE|INFORMATIVO|NO_RESUELTO",
  "supported": true,
  "confidence": "ALTA|MEDIA|BAJA",
  "challenge": "el argumento más fuerte en contra de la conclusión, y por qué prevalece o no",
  "explanation": "respuesta final en español, directa y luego paso a paso si hace falta",
  "citations": ["id exacto de regla o carta de la evidencia"],
  "missing_info": "",
  "missing_rules_query": ""
}}

Reglas:
- challenge nunca puede quedar vacío: si de verdad no hay contraargumento, explicá por qué.
- Si el contraargumento se sostiene pero no es concluyente, usá DEPENDE o bajá confidence.
- supported=true solo si la evidencia alcanza para justificar el resultado.
- citations debe usar únicamente IDs exactos que aparecen entre corchetes.
- Si faltan datos materiales, usá NO_RESUELTO, BAJA, supported=false y explicá missing_info.
- NO_RESUELTO significa "no puedo responder". Si respondiste la pregunta, NUNCA uses
  NO_RESUELTO, por más que no encaje en SI/NO.
- Si la pregunta ofrece opciones ("¿A o B?", "¿cuál de las dos secuencias vale?") y
  pudiste determinar cuál corresponde, usá RESUELTO y decí en explanation cuál es y
  por qué. RESUELTO también sirve para preguntas de "cuántas veces" o "en qué orden".
- missing_rules_query: completalo SOLO si verdict es NO_RESUELTO. Escribí en una frase
  qué reglas o mecánicas de Riftbound habría que buscar para poder resolverlo
  (ej: "orden en que se finalizan y resuelven las triggered abilities en la chain, Deathknell").
  Dejalo VACÍO si lo que falta son datos del estado de juego que solo puede dar el
  usuario (quién ataca, qué cartas hay en mesa, en qué fase están).
- Para preguntas de reglas, incluí al menos una regla. Para texto de carta, incluí su número.
- No incluyas Markdown fuera de los strings JSON."""

    verifier_role = (
        "Sos un verificador conservador. Es preferible abstenerse antes que inventar un ruling."
    )
    try:
        raw = generate_with_fallback(
            verifier_prompt, verifier_role, models=VERIFIER_MODELS
        )
        parsed = parse_json_response(raw)
        if parsed is None:
            retry = generate_with_fallback(
                verifier_prompt
                + "\nTu respuesta anterior no fue JSON válido. Reintentá con JSON puro, sin backticks.",
                verifier_role,
                models=VERIFIER_MODELS,
            )
            parsed = parse_json_response(retry)
            if parsed is None:
                print(f"VERIFIER: respuesta no parseable: {retry[:400]!r}")
        failure = ""
    except Exception as exc:
        print(f"VERIFIER ERROR: {type(exc).__name__}: {exc}")
        parsed = None
        failure = describe_model_failure(exc)

    if parsed is None:
        return {
            "verdict": "NO_RESUELTO",
            "supported": False,
            "confidence": "BAJA",
            "explanation": "No pude verificar la respuesta con un formato confiable.",
            "citations": [],
            "missing_info": failure or "La revisión automática no devolvió un formato válido.",
        }
    return parsed


def select_fallback_evidence(
    query: str,
    evidence: dict[str, dict],
    limit: int = 4,
) -> list[dict]:
    """Elige evidencia relevante sin afirmar que alcanza para un ruling."""
    q = query.lower()
    selected_ids: list[str] = []
    for marker, triggers in CRITICAL_RULE_MARKERS.items():
        rule_id = marker.replace("**", "").rstrip(".")
        if rule_id in evidence and any(token in q for token in triggers):
            selected_ids.append(rule_id)

    for item_id, item in evidence.items():
        if item["kind"] == "card" and item_id not in selected_ids:
            selected_ids.append(item_id)

    if not selected_ids:
        selected_ids.extend(
            item_id
            for item_id, item in evidence.items()
            if item["kind"] == "rule"
        )
    return [evidence[item_id] for item_id in selected_ids[:limit]]


def deterministic_ruling(query: str) -> dict | None:
    """Formaliza interacciones críticas ya validadas por casos de juez."""
    q = query.lower()
    has_hidden_blade = HIDDEN_BLADE_CARD_NAME in q
    has_zhonya = any(token in q for token in ["zhonya", "zhonyas", "hourglass"])
    if has_hidden_blade and has_zhonya:
        return {
            "verdict": "SI",
            "supported": True,
            "confidence": "ALTA",
            "explanation": (
                "Sí, el controlador de la unidad roba 2. Hidden Blade primero intenta matar "
                "la unidad; Zhonya's Hourglass reemplaza esa muerte por heal, exhaust y recall. "
                "Como el draw es una instrucción vinculada que no dice “If you do”, el reemplazo "
                "del kill no impide que se ejecute. Esto es distinto de Flash o Retreat: si la "
                "unidad deja de ser un target válido antes de resolver, Hidden Blade mistargetea "
                "y no se roba."
            ),
            "citations": ["359.3.e.14", "OGN-213", "OGN-077"],
            "missing_info": "",
        }

    has_deathknell = any(
        token in q for token in ["deathknell", "deathkneel", "death knell"]
    )
    has_cleanup_context = any(
        token in q
        for token in ["combat", "combate", "cleanup", "heal", "curan", "daño", "danio"]
    )
    if has_deathknell and has_cleanup_context:
        return {
            "verdict": "INFORMATIVO",
            "supported": True,
            "confidence": "ALTA",
            "explanation": (
                "En Combat Cleanup, Deathknell triggerea antes del heal pero se resuelve "
                "después. En 3a queda como Pending Item; en 3b mueren las unidades con lethal; "
                "en 3c se curan las sobrevivientes. Durante el Cleanup la chain no puede "
                "finalizarse ni resolverse, así que el efecto de Deathknell espera hasta que "
                "termine el Cleanup.\n\n"
                "Consecuencia práctica: la unidad que sobrevivió el combate ya está curada a 0 "
                "de daño cuando el Deathknell la golpea. Por eso solo muere si el daño del "
                "Deathknell por sí solo alcanza o supera su Might. El daño que había recibido "
                "en el combate NO se suma."
            ),
            "citations": ["320", "323.4", "466.1.a.1", "808.1"],
            "missing_info": "",
        }
    return None


def finalize_ruling(
    review: dict,
    evidence: dict[str, dict],
    query: str,
) -> dict:
    """Valida citas de forma determinística y aplica la política de abstención."""
    allowed_verdicts = {"SI", "NO", "RESUELTO", "DEPENDE", "INFORMATIVO", "NO_RESUELTO"}
    allowed_confidence = {"ALTA", "MEDIA", "BAJA"}
    verdict = str(review.get("verdict", "NO_RESUELTO")).upper()
    confidence = str(review.get("confidence", "BAJA")).upper()
    supported = review.get("supported") is True
    if verdict not in allowed_verdicts:
        verdict = "NO_RESUELTO"
    if confidence not in allowed_confidence:
        confidence = "BAJA"

    requested_ids = review.get("citations", [])
    if not isinstance(requested_ids, list):
        requested_ids = []
    valid_ids = []
    for item_id in requested_ids:
        normalized = str(item_id).strip().replace("Regla ", "")
        if normalized in evidence and normalized not in valid_ids:
            valid_ids.append(normalized)
    citations = [evidence[item_id] for item_id in valid_ids]

    # Un NO_RESUELTO con supported=true, citas válidas y confianza no BAJA es una
    # contradicción: el modelo resolvió la pregunta y solo falló al etiquetarla.
    # Pasa cuando la pregunta es de opción múltiple ("¿A o B?") y ni SI ni NO encajan.
    if verdict == "NO_RESUELTO" and supported and citations and confidence != "BAJA":
        print("VEREDICTO incoherente: NO_RESUELTO con evidencia y confianza -> RESUELTO")
        verdict = "RESUELTO"

    explanation = str(review.get("explanation", "")).strip()
    missing_info = str(review.get("missing_info", "")).strip()
    if not supported or not citations:
        verdict = "NO_RESUELTO"
        confidence = "BAJA"
        citations = select_fallback_evidence(query, evidence)
        reason = missing_info or "No encontré evidencia verificable suficiente para cerrar el ruling."
        explanation = (
            "No puedo resolver esta interacción con suficiente confianza. "
            f"{reason} Estas son las reglas o cartas relevantes que sí pude recuperar."
        )

    return {
        "verdict": verdict,
        "confidence": confidence,
        "answer": explanation,
        "citations": citations,
        "missing_info": missing_info,
        "challenge": str(review.get("challenge", "")).strip(),
    }


def ambiguity_ruling(ambiguities: list[str]) -> dict:
    return {
        "verdict": "NO_RESUELTO",
        "confidence": "BAJA",
        "answer": (
            "Necesito identificar la carta exacta antes de dar un ruling. "
            + " ".join(ambiguities)
        ),
        "citations": [],
        "missing_info": "Carta ambigua.",
    }


def build_user_message(
    chunks: list[str],
    card_texts: list[str],
    ambiguities: list[str],
    pinned: str,
    query: str,
) -> str:
    """Arma el prompt del draft. Se reusa en la segunda pasada con más contexto."""
    parts = []
    if pinned:
        parts.append(pinned)
    parts.append("Contexto de las reglas de Riftbound:\n\n" + "\n\n---\n\n".join(chunks))
    if card_texts:
        cards_block = "Cartas adjuntas (datos de la base de datos):\n\n"
        for i, ct in enumerate(card_texts, 1):
            cards_block += f"Carta {i}:\n{ct}\n\n"
        parts.append(cards_block.rstrip())
    if ambiguities:
        parts.append(
            "IMPORTANTE - AMBIGÜEDAD DETECTADA:\n"
            + "\n".join(f"- {amb}" for amb in ambiguities)
        )
    parts.append(f"Pregunta: {query}")
    return "\n\n---\n\n".join(parts)


@app.post("/ask")
async def ask(
    query: str = Form(...),
    images: list[UploadFile] = File(default=[]),
):
    # 1. Procesar imágenes adjuntas (identificar carta → buscar en DB)
    card_texts = []
    image_cards = []
    for img_file in images:
        if img_file.filename:
            img_bytes = await img_file.read()
            card_text = identify_card_from_image(img_bytes)
            if card_text:
                card_texts.append(card_text)
                number_match = re.search(r"Número:\s*([A-Z]+-\d+)", card_text)
                if number_match and number_match.group(1) in CARDS_BY_NUMBER:
                    image_cards.append(CARDS_BY_NUMBER[number_match.group(1)])

    # 2. Buscar cartas mencionadas por nombre en la query
    mentioned_cards, ambiguities = find_cards_in_text(query)
    for card in mentioned_cards:
        card_texts.append(format_card_info(card))

    # 3. Armar query enriquecida para búsqueda
    search_query = enrich_search_query(query)
    if card_texts:
        search_query += " " + " ".join(card_texts)

    # 3. Detectar categoría y buscar chunks relevantes
    categories = detect_category(query)
    chunks, metadatas = retrieve_chunks(
        query, search_query, categories, [*mentioned_cards, *image_cards]
    )
    evidence_cards = {
        card["card_number"]: card
        for card in [*mentioned_cards, *image_cards]
        if card.get("card_number")
    }
    evidence = build_evidence_catalog(
        chunks,
        metadatas,
        list(evidence_cards.values()),
    )

    # 4. Armar contexto
    pinned = get_pinned_ruling(query)
    if pinned:
        print("PINNED RULING aplicado")

    # 5. Armar mensaje del usuario
    user_message = build_user_message(chunks, card_texts, ambiguities, pinned, query)

    # 6. Generar respuesta con Gemini (con historial)
    # Un ruling pineado no debe heredar una respuesta previa incorrecta.
    gemini_history = []
    if not pinned:
        for msg in conversation_history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    followup_used = ""
    if ambiguities:
        ruling = ambiguity_ruling(ambiguities)
    else:
        review = deterministic_ruling(query)
        if review is None:
            try:
                draft = generate_with_fallback(
                    user_message, SYSTEM_PROMPT, gemini_history
                )
                review = verify_ruling(query, draft, evidence)

                # Retrieval iterativo. Una sola búsqueda no siempre acierta: si el
                # verificador se abstuvo porque le faltan REGLAS, nos dice cuáles y
                # volvemos a buscar con esa query. La reformulación además dispara
                # CRITICAL_RULE_MARKERS que la pregunta original no tocaba.
                # Una sola vez: cuesta 2 llamadas extra.
                followup = (review.get("missing_rules_query") or "").strip()
                if review.get("verdict") == "NO_RESUELTO" and followup:
                    extra_chunks, extra_metas = retrieve_chunks(
                        followup,
                        enrich_search_query(followup),
                        categories,
                        [*mentioned_cards, *image_cards],
                    )
                    merged, merged_metas = merge_chunks(
                        chunks, metadatas, extra_chunks, extra_metas
                    )
                    # Si no trajo nada nuevo, reintentar es gastar dos llamadas para
                    # llegar a la misma abstención.
                    if len(merged) > len(chunks):
                        print(
                            f"RETRIEVAL 2da pasada: {followup!r} "
                            f"(+{len(merged) - len(chunks)} chunks)"
                        )
                        followup_used = followup
                        chunks, metadatas = merged, merged_metas
                        evidence = build_evidence_catalog(
                            chunks, metadatas, list(evidence_cards.values())
                        )
                        retry_message = build_user_message(
                            chunks, card_texts, ambiguities, pinned, query
                        )
                        retry_draft = generate_with_fallback(
                            retry_message, SYSTEM_PROMPT, gemini_history
                        )
                        retry_review = verify_ruling(query, retry_draft, evidence)
                        # Nos quedamos con la segunda solo si dejó de abstenerse.
                        if retry_review.get("verdict") != "NO_RESUELTO":
                            review = retry_review
            except Exception as exc:
                print(f"DRAFT ERROR: {type(exc).__name__}: {exc}")
                review = {
                    "verdict": "NO_RESUELTO",
                    "supported": False,
                    "confidence": "BAJA",
                    "explanation": "",
                    "citations": [],
                    "missing_info": describe_model_failure(exc),
                }
        ruling = finalize_ruling(review, evidence, query)

    answer_text = ruling["answer"]
    sources = sorted({citation["source"] for citation in ruling["citations"]})

    # 7. Guardar en historial (solo query, no el contexto completo)
    conversation_history.append({"role": "user", "content": query})
    conversation_history.append({"role": "assistant", "content": answer_text})
    while len(conversation_history) > MAX_HISTORY * 2:
        conversation_history.pop(0)

    return {
        "answer": answer_text,
        "verdict": ruling["verdict"],
        "confidence": ruling["confidence"],
        "citations": ruling["citations"],
        "sources": sources,
        "missing_info": ruling["missing_info"],
        "challenge": ruling.get("challenge", ""),
        "followup_query": followup_used,
    }


@app.post("/ask-stream")
async def ask_stream(
    query: str = Form(...),
    images: list[UploadFile] = File(default=[]),
):
    """Igual que /ask pero envía eventos SSE de progreso al frontend."""

    # Leer imágenes ANTES del generator (el body de la request ya no está disponible después)
    raw_images: list[tuple[str, bytes]] = []
    for img_file in images:
        if img_file.filename:
            raw_images.append((img_file.filename, await img_file.read()))

    async def event_stream():
        def sse(event: str, data: str = "") -> str:
            return f"event: {event}\ndata: {data}\n\n"

        yield sse("status", "searching")

        # 1. Procesar imágenes
        card_texts = []
        image_cards = []
        for filename, img_bytes in raw_images:
            card_text = identify_card_from_image(img_bytes)
            if card_text:
                card_texts.append(card_text)
                number_match = re.search(r"Número:\s*([A-Z]+-\d+)", card_text)
                if number_match and number_match.group(1) in CARDS_BY_NUMBER:
                    image_cards.append(CARDS_BY_NUMBER[number_match.group(1)])

        # 2. Buscar cartas mencionadas
        mentioned_cards, ambiguities = find_cards_in_text(query)
        for card in mentioned_cards:
            card_texts.append(format_card_info(card))

        # 3. Query enriquecida + chunks
        search_query = enrich_search_query(query)
        if card_texts:
            search_query += " " + " ".join(card_texts)
        categories = detect_category(query)
        chunks, metadatas = retrieve_chunks(
            query, search_query, categories, [*mentioned_cards, *image_cards]
        )
        evidence_cards = {
            card["card_number"]: card
            for card in [*mentioned_cards, *image_cards]
            if card.get("card_number")
        }
        evidence = build_evidence_catalog(
            chunks, metadatas, list(evidence_cards.values()),
        )

        # 4-5. Contexto y mensaje
        pinned = get_pinned_ruling(query)
        if pinned:
            print("PINNED RULING aplicado")
        user_message = build_user_message(chunks, card_texts, ambiguities, pinned, query)
        gemini_history = []
        if not pinned:
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

        # 6. Generar
        followup_used = ""
        if ambiguities:
            ruling = ambiguity_ruling(ambiguities)
        else:
            review = deterministic_ruling(query)
            if review is None:
                try:
                    yield sse("status", "draft")
                    draft = generate_with_fallback(
                        user_message, SYSTEM_PROMPT, gemini_history
                    )
                    yield sse("status", "verify")
                    review = verify_ruling(query, draft, evidence)

                    followup = (review.get("missing_rules_query") or "").strip()
                    if review.get("verdict") == "NO_RESUELTO" and followup:
                        extra_chunks, extra_metas = retrieve_chunks(
                            followup,
                            enrich_search_query(followup),
                            categories,
                            [*mentioned_cards, *image_cards],
                        )
                        merged, merged_metas = merge_chunks(
                            chunks, metadatas, extra_chunks, extra_metas
                        )
                        if len(merged) > len(chunks):
                            print(
                                f"RETRIEVAL 2da pasada: {followup!r} "
                                f"(+{len(merged) - len(chunks)} chunks)"
                            )
                            followup_used = followup
                            evidence = build_evidence_catalog(
                                merged, merged_metas, list(evidence_cards.values())
                            )
                            retry_message = build_user_message(
                                merged, card_texts, ambiguities, pinned, query
                            )
                            yield sse("status", "draft_retry")
                            retry_draft = generate_with_fallback(
                                retry_message, SYSTEM_PROMPT, gemini_history
                            )
                            yield sse("status", "verify")
                            retry_review = verify_ruling(query, retry_draft, evidence)
                            if retry_review.get("verdict") != "NO_RESUELTO":
                                review = retry_review
                except Exception as exc:
                    print(f"DRAFT ERROR: {type(exc).__name__}: {exc}")
                    review = {
                        "verdict": "NO_RESUELTO",
                        "supported": False,
                        "confidence": "BAJA",
                        "explanation": "",
                        "citations": [],
                        "missing_info": describe_model_failure(exc),
                    }
            ruling = finalize_ruling(review, evidence, query)

        answer_text = ruling["answer"]
        sources = sorted({citation["source"] for citation in ruling["citations"]})
        conversation_history.append({"role": "user", "content": query})
        conversation_history.append({"role": "assistant", "content": answer_text})
        while len(conversation_history) > MAX_HISTORY * 2:
            conversation_history.pop(0)

        result = json_mod.dumps({
            "answer": answer_text,
            "verdict": ruling["verdict"],
            "confidence": ruling["confidence"],
            "citations": ruling["citations"],
            "sources": sources,
            "missing_info": ruling["missing_info"],
            "challenge": ruling.get("challenge", ""),
            "followup_query": followup_used,
        }, ensure_ascii=False)
        yield sse("result", result)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# Servir frontend
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.post("/reset")
def reset():
    conversation_history.clear()
    return {"ok": True}


@app.get("/health")
def health():
    """Para el túnel público y para chequear que el proceso está vivo."""
    return {"ok": True, "name": "riftbound-rules-chatbot"}


@app.get("/config")
def config():
    """Configuración activa, para que cada corrida del eval quede autoidentificada."""
    return {
        "draft_models": DRAFT_MODELS,
        "verifier_models": VERIFIER_MODELS,
        "top_k": TOP_K,
        "draft_override": bool(_draft_override),
        "vision_enabled": VISION_ENABLED,
    }


@app.get("/")
def root():
    conversation_history.clear()
    return FileResponse(str(STATIC_DIR / "index.html"))
