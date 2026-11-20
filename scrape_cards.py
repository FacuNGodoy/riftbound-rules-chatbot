"""
Scraper de cartas de Riftbound desde piltoverarchive.com
Usa Playwright para navegar la página y extraer datos de cada carta.

Trae TODAS las variantes, set por set:
  - standard      : número normal dentro del set (RAD-043)
  - alt           : mismo número con sufijo a/b (RAD-043a)
  - overnumbered  : número mayor al tamaño del set (RAD-173 en un set de 167)
  - signed        : overnumbered firmada (OGN-302*)

Seguridad:
  - Hace backup de cards.json antes de empezar (cards_backup_pre_all_variants.json).
  - El progreso va a cards_all_partial.json (se puede reanudar).
  - cards.json solo se reemplaza al final y solo si no se pierde ninguna carta
    que ya estaba. Si no, el resultado queda en cards_all_variants.json.
"""

import json
import math
import re
import shutil
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / "cards.json"
BACKUP_FILE = ROOT / "cards_backup_pre_all_variants.json"
PARTIAL_FILE = ROOT / "cards_all_partial.json"
RESULT_FILE = ROOT / "cards_all_variants.json"

SITE_URL = "https://piltoverarchive.com/cards?sets={code}"
SET_CODES = ["OGS", "OGN", "SFD", "UNL", "VEN", "RAD"]
PAGE_SIZE = 48

DOMAIN_NAMES = {"Body", "Calm", "Fury", "Mind", "Chaos", "Order"}
TYPE_NAMES = {"Champion Unit", "Signature Spell", "Legend", "Unit", "Spell", "Gear", "Rune", "Battlefield"}
RARITY_NAMES = {"Legend", "Epic", "Rare", "Uncommon", "Common", "Token"}

SECTION_LABELS = {"description", "effect", "might"}

# Números: SFD-058, SFD-058a (alt), SFD-T01 (token), SFD-R01a (runa alt), OGN-302* (firmada)
NUMBER_PATTERN = r"[A-Z]+-[A-Z]?\d+[ab]?\*?"


def variant_from_label(label: str) -> str:
    """El modal dice la variante textualmente; sin etiqueta es estándar."""
    low = label.lower()
    if "signed" in low:
        return "signed"
    if "overnumbered" in low:
        return "overnumbered"
    if "alt" in low:
        return "alt"
    return "standard"


def extract_card_data(page) -> dict | None:
    """Extrae datos de la carta del modal abierto."""
    try:
        dialog = page.locator('[data-slot="dialog-content"]')
        dialog.wait_for(state="visible", timeout=5000)
        time.sleep(0.8)

        full_text = dialog.text_content()

        # Nombre
        name = ""
        name_el = dialog.locator("h2, [class*='text-2xl'], [class*='text-xl']").first
        if name_el.count():
            name = name_el.text_content().strip()

        # Badges - clasificar en tipo, rareza, dominios, tags
        all_badges = []
        badge_els = dialog.locator('[class*="flex-wrap"] > div, [class*="flex-wrap"] > span').all()
        for el in badge_els:
            text = el.text_content().strip()
            if text and len(text) < 30:
                all_badges.append(text)

        card_type = ""
        rarity = ""
        domains = []
        tags = []

        for badge in all_badges:
            if badge in TYPE_NAMES:
                card_type = badge
            elif badge in RARITY_NAMES:
                rarity = badge
            elif badge in DOMAIN_NAMES:
                domains.append(badge)
            elif badge and badge not in {"Standard"}:
                tags.append(badge)

        if not card_type:
            for t in ["Champion Unit", "Signature Spell", "Legend", "Battlefield", "Unit", "Spell", "Gear", "Rune"]:
                if t in full_text:
                    card_type = t
                    break

        # Stats
        energy = ""
        power = ""
        might = ""
        for label in ["Energy", "Power", "Might"]:
            try:
                label_el = dialog.locator(f':text-is("{label}")').first
                if label_el.count():
                    parent = label_el.locator("xpath=..")
                    parent_text = parent.text_content().strip()
                    val = parent_text.replace(label, "").strip()
                    if val.isdigit():
                        if label == "Energy":
                            energy = val
                        elif label == "Power":
                            power = val
                        elif label == "Might":
                            might = val
            except Exception:
                pass

        # Las cartas con frame de attachment (Equipment) tienen tres secciones
        # separadas en el modal: Description (Rules Text), Effect (Effect Text)
        # y Might (Might Bonus). La distinción es funcional: al attachear, el
        # Rules Text se vuelve inactive y el Effect Text se appendea a la carta
        # de arriba (136.2.c). Concatenarlos borra esa diferencia.
        def clean_html(html: str) -> str:
            text = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*/?>', r' \1 ', html)
            text = re.sub(r'<[^>]+>', ' ', text)
            return re.sub(r'\s+', ' ', text).strip()

        sections: dict[str, list[str]] = {}
        current = None
        for el in dialog.locator("p").all():
            cls = el.get_attribute("class") or ""
            text = clean_html(el.inner_html())
            if not text:
                continue
            if cls.startswith("mb-"):  # solo los encabezados de sección llevan margen
                label = text.lower()
                current = label if label in SECTION_LABELS else None
            elif current and ("whitespace-pre-line" in cls or "items-center" in cls):
                sections.setdefault(current, []).append(text)

        rules_text = " ".join(sections.get("description", []))
        effect_text = " ".join(sections.get("effect", []))
        might_bonus = " ".join(sections.get("might", []))
        description = " ".join(p for p in (rules_text, effect_text, might_bonus) if p)

        # Card Number (con sufijo a/b en las alters)
        card_number = ""
        m = re.search(rf'Card Number:\s*({NUMBER_PATTERN})', full_text)
        if m:
            card_number = m.group(1)

        # Variant: aparece como texto en el modal ("Alt Art", "Overnumbered + Signed")
        variant_label = ""
        m = re.search(r'Variant:\s*(.+?)(?:Close|Artist|$)', full_text)
        if m:
            variant_label = m.group(1).strip()

        # Set
        card_set = ""
        m = re.search(r'Set:\s*([^\n]+?)(?:Card Number|Artist|$)', full_text)
        if m:
            card_set = m.group(1).strip()

        return {
            "name": name,
            "card_number": card_number,
            "set": card_set,
            "type": card_type,
            "rarity": rarity,
            "domains": domains,
            "tags": tags,
            "energy": energy,
            "power": power,
            "might": might,
            "rules_text": rules_text,
            "effect_text": effect_text,
            "might_bonus": might_bonus,
            "description": description,
            "variant": variant_from_label(variant_label),
            "variant_label": variant_label,
        }
    except Exception as e:
        print(f"  Error extrayendo datos: {e}")
        return None


def read_site_count(page) -> int | None:
    m = re.search(r"([\d,]+)\s+cards", page.locator("body").inner_text())
    return int(m.group(1).replace(",", "")) if m else None


def clean_variant_tags(cards: list[dict]) -> None:
    """Saca de `tags` el nombre de la variante (ej. un badge de arte alternativo).

    Sin conocer cómo lo llama el sitio: en una alter/overnumbered, un tag que la
    carta base (mismo nombre, estándar) no tiene se descarta.
    """
    base_tags: dict[str, set[str]] = {}
    for c in cards:
        if c.get("variant") == "standard":
            base_tags.setdefault(c["name"], set()).update(c.get("tags", []))
    for c in cards:
        if c.get("variant") == "standard" or c["name"] not in base_tags:
            continue
        extra = [t for t in c.get("tags", []) if t not in base_tags[c["name"]]]
        if extra:
            c["tags"] = [t for t in c.get("tags", []) if t in base_tags[c["name"]]]


def save_partial(cards: list[dict]) -> None:
    PARTIAL_FILE.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    old_cards = json.loads(OUTPUT_FILE.read_text(encoding="utf-8")) if OUTPUT_FILE.exists() else []

    if old_cards and not BACKUP_FILE.exists():
        shutil.copyfile(OUTPUT_FILE, BACKUP_FILE)
        print(f"Backup creado: {BACKUP_FILE.name} ({len(old_cards)} cartas)")
    elif BACKUP_FILE.exists():
        print(f"Backup ya existente, no se pisa: {BACKUP_FILE.name}")

    cards: list[dict] = []
    if PARTIAL_FILE.exists():
        cards = json.loads(PARTIAL_FILE.read_text(encoding="utf-8"))
        print(f"Reanudando desde {PARTIAL_FILE.name}: {len(cards)} cartas")
    scraped_numbers = {c["card_number"] for c in cards if c.get("card_number")}

    site_counts: dict[str, int | None] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        first = True
        for code in SET_CODES:
            base_url = SITE_URL.format(code=code)
            page.goto(base_url, wait_until="load", timeout=45000)
            time.sleep(2)

            if first:
                try:
                    cookie_btn = page.locator('button:has-text("Accept"), button:has-text("Reject"), [data-cky-tag="accept-button"]').first
                    if cookie_btn.count():
                        cookie_btn.click(timeout=3000)
                        time.sleep(1)
                except Exception:
                    pass
                first = False

            site_count = read_site_count(page)
            site_counts[code] = site_count
            if not site_count:
                print(f"\n[{code}] No pude leer el conteo del sitio; salto este set")
                continue
            total_pages = math.ceil(site_count / PAGE_SIZE)
            print(f"\n##### {code}: el sitio muestra {site_count} cartas ({total_pages} páginas) #####")

            for pg in range(1, total_pages + 1):
                url = f"{base_url}&page={pg}"
                print(f"\n=== {code} página {pg}/{total_pages} ===")
                for attempt in range(3):
                    try:
                        page.goto(url, wait_until="networkidle", timeout=45000)
                        break
                    except PWTimeout:
                        print(f"  Timeout cargando página (intento {attempt+1}/3)")
                time.sleep(2)

                card_imgs = page.locator('img[src*="cdn.piltoverarchive.com/cards/"]').all()
                print(f"  {len(card_imgs)} cartas en la página")

                for i, card_img in enumerate(card_imgs):
                    try:
                        card_img.scroll_into_view_if_needed(timeout=3000)
                        time.sleep(0.3)
                        card_img.click(timeout=3000)
                        time.sleep(0.8)

                        data = extract_card_data(page)
                        if data and data.get("name") and data["card_number"]:
                            if data["card_number"] in scraped_numbers:
                                print(f"  [{i+1}/{len(card_imgs)}] {data['name']} ({data['card_number']}) ya existe")
                            else:
                                cards.append(data)
                                scraped_numbers.add(data["card_number"])
                                print(f"  [{i+1}/{len(card_imgs)}] {data['name']} ({data['card_number']}) [{data['variant']}]")
                        elif data and data.get("name"):
                            print(f"  [{i+1}/{len(card_imgs)}] {data['name']} sin número: se descarta")
                        else:
                            print(f"  [{i+1}/{len(card_imgs)}] No se pudo extraer datos")

                        try:
                            close = page.locator('button[data-slot="dialog-close"]').first
                            if close.count():
                                close.click(timeout=2000)
                            else:
                                page.keyboard.press("Escape")
                        except Exception:
                            page.keyboard.press("Escape")
                        time.sleep(0.5)

                    except PWTimeout:
                        print(f"  [{i+1}] Timeout, saltando")
                        page.keyboard.press("Escape")
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"  [{i+1}] Error: {e}")
                        page.keyboard.press("Escape")
                        time.sleep(0.5)

                save_partial(cards)
                print(f"  Progreso guardado: {len(cards)} cartas totales")

        browser.close()

    clean_variant_tags(cards)
    save_partial(cards)

    # Reporte por set y variante
    print("\n=== Resumen por set ===")
    for code in SET_CODES:
        in_set = [c for c in cards if c["card_number"].startswith(code + "-")]
        by_variant = {v: sum(1 for c in in_set if c.get("variant") == v) for v in ("standard", "alt", "overnumbered", "signed")}
        print(f"  {code}: {len(in_set)} scrapeadas / {site_counts.get(code)} en el sitio  {by_variant}")

    # Reemplazo seguro de cards.json: no se pierde ninguna carta que ya estaba.
    new_numbers = {c["card_number"] for c in cards}
    lost = sorted(c["card_number"] for c in old_cards if c.get("card_number") and c["card_number"] not in new_numbers)
    RESULT_FILE.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
    if lost:
        print(f"\nNO se reemplaza cards.json: faltan {len(lost)} cartas que ya estaban: {', '.join(lost[:20])}")
        print(f"Resultado guardado en {RESULT_FILE.name}; cards.json sigue intacto.")
    else:
        shutil.copyfile(RESULT_FILE, OUTPUT_FILE)
        print(f"\ncards.json actualizado: {len(old_cards)} -> {len(cards)} cartas (backup: {BACKUP_FILE.name})")


if __name__ == "__main__":
    main()
