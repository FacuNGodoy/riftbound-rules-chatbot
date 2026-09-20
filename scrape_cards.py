"""
Scraper de cartas de Riftbound desde piltoverarchive.com
Usa Playwright para navegar la página y extraer datos de cada carta.
Guarda progreso en cards.json después de cada página.
"""

import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

OUTPUT_FILE = Path(__file__).resolve().parent / "cards.json"
BASE_URL = "https://piltoverarchive.com/cards?variants=standard&sortBy=color%3Aasc"
TOTAL_PAGES = 21

DOMAIN_NAMES = {"Body", "Calm", "Fury", "Mind", "Chaos", "Order"}
TYPE_NAMES = {"Champion Unit", "Signature Spell", "Legend", "Unit", "Spell", "Gear", "Rune", "Battlefield"}
RARITY_NAMES = {"Legend", "Epic", "Rare", "Uncommon", "Common", "Token"}

SETS = {"OGS": 24, "OGN": 298, "SFD": 221, "UNL": 219, "VEN": 166}

SECTION_LABELS = {"description", "effect", "might"}


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

        # Card Number
        card_number = ""
        m = re.search(r'Card Number:\s*([A-Z]+-\d+)', full_text)
        if m:
            card_number = m.group(1)

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
        }
    except Exception as e:
        print(f"  Error extrayendo datos: {e}")
        return None


def main():
    # Cargar progreso previo si existe
    cards = []
    scraped_numbers = set()
    if OUTPUT_FILE.exists():
        cards = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        scraped_numbers = {c["card_number"] for c in cards if c.get("card_number")}
        print(f"Cargadas {len(cards)} cartas previas")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        # Navegar primero para cerrar cookie banner
        page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Cerrar cookie banner si aparece
        try:
            cookie_btn = page.locator('button:has-text("Accept"), button:has-text("Reject"), [data-cky-tag="accept-button"]').first
            if cookie_btn.count():
                cookie_btn.click(timeout=3000)
                time.sleep(1)
        except Exception:
            pass

        for pg in range(1, TOTAL_PAGES + 1):
            url = f"{BASE_URL}&page={pg}"
            print(f"\n=== Página {pg}/{TOTAL_PAGES} ===")
            for attempt in range(3):
                try:
                    page.goto(url, wait_until="networkidle", timeout=45000)
                    break
                except PWTimeout:
                    print(f"  Timeout cargando página (intento {attempt+1}/3)")
                    if attempt == 2:
                        print("  Saltando página")
                        continue
            time.sleep(2)

            # Buscar imágenes de cartas del CDN
            card_imgs = page.locator('img[src*="cdn.piltoverarchive.com/cards/"]').all()
            print(f"  {len(card_imgs)} cartas en la página")

            for i, card_img in enumerate(card_imgs):
                try:
                    # Scroll al elemento para que sea visible
                    card_img.scroll_into_view_if_needed(timeout=3000)
                    time.sleep(0.3)
                    card_img.click(timeout=3000)
                    time.sleep(0.8)

                    data = extract_card_data(page)
                    if data and data.get("name"):
                        if data["card_number"] and data["card_number"] not in scraped_numbers:
                            cards.append(data)
                            scraped_numbers.add(data["card_number"])
                            print(f"  [{i+1}/{len(card_imgs)}] {data['name']} ({data['card_number']})")
                        elif not data["card_number"]:
                            cards.append(data)
                            print(f"  [{i+1}/{len(card_imgs)}] {data['name']} (sin número)")
                        else:
                            print(f"  [{i+1}/{len(card_imgs)}] {data['name']} (ya existe)")
                    else:
                        print(f"  [{i+1}/{len(card_imgs)}] No se pudo extraer datos")

                    # Cerrar modal
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

            # Guardar progreso después de cada página
            OUTPUT_FILE.write_text(
                json.dumps(cards, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"  Progreso guardado: {len(cards)} cartas totales")

        browser.close()

    # Reporte de cartas faltantes
    scraped_nums = {c["card_number"] for c in cards if c.get("card_number")}
    print(f"\nScraping completo: {len(cards)} cartas en {OUTPUT_FILE}")
    print("\n=== Cartas faltantes por set ===")
    total_missing = 0
    for set_code, count in SETS.items():
        missing = []
        for i in range(1, count + 1):
            card_id = f"{set_code}-{i:03d}"
            if card_id not in scraped_nums:
                missing.append(card_id)
        if missing:
            print(f"  {set_code}: {len(missing)} faltantes → {', '.join(missing)}")
            total_missing += len(missing)
        else:
            print(f"  {set_code}: completo ({count}/{count})")
    if total_missing == 0:
        print("\n¡Todas las cartas scrapeadas!")
    else:
        print(f"\nTotal faltantes: {total_missing}")


if __name__ == "__main__":
    main()
