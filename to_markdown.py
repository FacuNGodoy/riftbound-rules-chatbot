"""
Convierte los .txt raw a .md curados con estructura de headers.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw_text"
MD_DIR = BASE_DIR / "docs"

# === Secciones principales del Core Rules ===
CORE_SECTIONS = {
    "000": "Golden and Silver Rules",
    "100": "Game Concepts",
    "300": "Playing the Game",
    "700": "Additional Rules",
    "800": "Keywords",
}

# Subsecciones del Core Rules (nivel ###)
CORE_SUBSECTIONS = {
    "001": "Golden Rule", "050": "Silver Rule",
    "101": "Deck Construction", "104": "Setup", "105": "Spaces",
    "107": "The Board", "108": "Non-Board Zones", "110": "Setup Process",
    "119": "Game Objects", "125": "Cards", "127": "Ownership", "128": "Privacy",
    "129": "Back Side", "130": "Front Side", "131": "Cost", "132": "Name",
    "133": "Category", "134": "Domain", "135": "Rules Text", "136": "Effect Text",
    "137": "Might Bonus", "138": "Flavor Text", "139": "Illustration",
    "140": "Units", "147": "Gear", "153": "Spells", "160": "Runes",
    "164": "Basic Runes", "165": "Rune Pools", "169": "Battlefields",
    "173": "Legends", "177": "Multiple Types", "179": "Tokens",
    "185": "Control", "191": "Winning", "197": "Locations", "201": "Costs",
    "301": "The Turn", "307": "States of the Turn", "311": "Priority and Focus",
    "314": "Phases of the Turn", "315": "Start of Turn", "316": "Main Phase",
    "317": "Ending Phase", "318": "Cleanups",
    "325": "Chains and Showdowns", "327": "Chains", "337": "Step 1: Finalize",
    "338": "Step 2: Execute", "339": "Step 3: Pass", "340": "Step 4: Resolve",
    "341": "Showdowns", "349": "Playing Cards", "353": "The Process of Play",
    "360": "Abilities", "363": "Passive Abilities", "367": "Replacement Effects",
    "376": "Activated Abilities", "382": "Triggered Abilities",
    "386": "Reflexive Triggers", "389": "Delayed Abilities",
    "393": "Linked Abilities", "398": "Playing or Activating Abilities",
    "407": "Game Actions", "412": "Types of Actions",
    "413": "Draw", "414": "Exhaust", "415": "Ready", "416": "Recycle",
    "417": "Deal", "418": "Heal", "419": "Play", "420": "Move",
    "421": "Hide", "422": "Discard", "423": "Stun", "424": "Reveal",
    "425": "Counter", "426": "Buff", "427": "Banish", "428": "Kill",
    "429": "Add", "430": "Channel", "431": "Burn Out", "432": "Double",
    "433": "Swap", "434": "Attach", "435": "Detach", "436": "Predict",
    "437": "Prevent", "438": "Replace", "439": "Create", "440": "Burn",
    "441": "Empower", "442": "Disempower", "443": "Skip", "444": "Pay",
    "445": "Movement", "452": "Combat", "454": "Recalls", "459": "Combat Showdown",
    "463": "The Steps of Combat", "467": "Scoring", "473": "Layers",
    "481": "Modes of Play", "484": "Sanctioned Modes",
    "487": "FFA3 (Skirmish)", "488": "FFA4 (War)",
    "649": "Conceding",
    "701": "Buffs", "706": "Mighty", "712": "Bonus Damage",
    "716": "Attachment", "720": "Inactive", "726": "Dependent Keywords",
    "728": "XP", "734": "Additional Turns", "739": "Special Terms",
    "741": "Counters", "750": "Making New Choices", "756": "Untargetability",
    "759": "Naming Cards, Types, and Tags", "764": "Ignoring Effects",
    "804": "Keyword Glossary",
    "805": "Accelerate", "806": "Action", "807": "Assault",
    "808": "Deathknell", "809": "Deflect", "810": "Ganking",
    "811": "Hidden", "812": "Legion", "813": "Reaction",
    "814": "Shield", "815": "Tank", "816": "Temporary",
    "817": "Vision", "818": "Equip", "819": "Quick-Draw",
    "820": "Repeat", "821": "Weaponmaster", "822": "Ambush",
    "823": "Hunt", "824": "Level", "825": "Unique",
    "826": "Backline", "827": "Empower", "828": "Empowered", "829": "Flow",
}

# === Secciones del Tournament Rules ===
TOURNEY_SECTIONS = {
    "000": "Golden Rule",
    "100": "Introduction",
    "200": "Definitions",
    "300": "Tournament Procedures",
    "400": "Infractions and Penalties",
    "500": "Communication",
    "600": "Competition Formats",
}


def clean_pdf_text(text: str) -> str:
    """Limpia el texto extraido de pdftotext -layout."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        # Colapsar whitespace excesivo pero mantener la linea
        s = line.strip()
        if not s:
            # No acumular mas de 1 linea vacia
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        # Remover indentacion excesiva, pero mantener el contenido
        cleaned.append(s)
    return "\n".join(cleaned)


def pdf_to_markdown(text: str, sections: dict, subsections: dict, title: str) -> str:
    """Convierte texto de PDF a Markdown con headers."""
    text = clean_pdf_text(text)
    lines = text.split("\n")
    output = [f"# {title}\n"]

    for line in lines:
        # Detectar secciones principales (## )
        m = re.match(r"^(\d{3})\.\s+(.*)", line)
        if m:
            num = m.group(1)
            if num in sections:
                output.append(f"\n## {num}. {sections[num]}\n")
                # Si la linea tiene mas texto que el titulo de seccion, agregarlo
                rest = m.group(2).strip()
                if rest and rest != sections[num]:
                    output.append(f"**{num}.** {rest}")
                continue
            elif num in subsections:
                output.append(f"\n### {num}. {subsections[num]}\n")
                rest = m.group(2).strip()
                if rest and rest != subsections[num]:
                    output.append(f"**{num}.** {rest}")
                continue

        # Mantener reglas con su numero en negrita
        m = re.match(r"^(\d{3}(?:\.\d+)*(?:\.[a-z](?:\.\d+)*)?)\.\s+(.*)", line)
        if m:
            output.append(f"**{m.group(1)}.** {m.group(2)}")
        else:
            output.append(line)

    return "\n".join(output)


# === OCR cleanup ===
OCR_FIXES = [
    # Bullets mal reconocidos
    (r"^[©«'']\s*", "* "),
    (r"^[©«'']\s*\*\s*", "* "),
    (r"^'\*\s*", "* "),
    (r"^'\s+", "* "),
    (r"^\+\s+", "* "),
    # Errores comunes de OCR
    (r"\bitis\b", "it is"),
    (r"\bhada\b", "had a"),
    (r"\bwll\b", "will"),
    (r"\bgett,", "get it."),
    (r"\bItisa\b", "It is a"),
    (r"\bthem$", "them."),
    (r"\bIfacard\b", "If a card"),
    (r"\bIfa card\b", "If a card"),
    (r"\bitikely\b", "it likely"),
    (r"\bBum action\b", "Burn action"),
    (r"\btum\b", "turn"),
    (r"\bDisernpowered\b", "Disempowered"),
    (r"\bdisenpowered\b", "disempowered"),
    (r"\bFowis\b", "Flow is"),
    (r"\bItis\b", "It is"),
    (r"\bCLARIFIE!\b", "CLARIFIED:"),
    (r"^'ards\b", "Cards"),
    (r"\bfeferences\b", "References"),
    # Limpiar separadores de pagina
    (r"^--- Página (\d+) ---$", r"\n---\n"),
]


def clean_ocr_text(text: str) -> str:
    """Limpia errores comunes de OCR en patch notes."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        for pattern, replacement in OCR_FIXES:
            s = re.sub(pattern, replacement, s)

        cleaned.append(s)
    return "\n".join(cleaned)


def patch_notes_to_markdown(text: str, title: str) -> str:
    """Convierte patch notes OCR a Markdown."""
    text = clean_ocr_text(text)
    lines = text.split("\n")
    output = [f"# {title}\n"]

    for line in lines:
        # Detectar posibles headers (lineas cortas sin bullet que no son reglas)
        s = line.strip()
        if (s and not s.startswith("*") and not s.startswith("-")
                and len(s) < 60 and not s[0].islower()
                and s == s.rstrip(".")  # No termina en punto
                and not s.startswith("**")
                and s not in ("", "---")):
            # Podria ser un header de seccion
            if re.match(r"^[A-Z]", s) and not re.match(r"^(This|However|We |The |Many|Some|Please|If |In |For |As |A |You |Speaking|Also|Already|Before|After)", s):
                if len(s) < 50:
                    output.append(f"\n## {s}\n")
                    continue
        output.append(line)

    return "\n".join(output)


def main():
    MD_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Core Rules PDF
    print("Convirtiendo Core Rules...")
    raw = (RAW_DIR / "Riftbound Core Rules RUP4.txt").read_text(encoding="utf-8")
    md = pdf_to_markdown(raw, CORE_SECTIONS, CORE_SUBSECTIONS, "Riftbound Core Rules RUP4")
    (MD_DIR / "core_rules.md").write_text(md, encoding="utf-8")
    print(f"  -> core_rules.md ({len(md):,} chars)")

    # 2. Tournament Rules PDF
    print("Convirtiendo Tournament Rules...")
    raw = (RAW_DIR / "Riftbound Tournament Rules RUP4.txt").read_text(encoding="utf-8")
    md = pdf_to_markdown(raw, TOURNEY_SECTIONS, {}, "Riftbound Tournament Rules RUP4")
    (MD_DIR / "tournament_rules.md").write_text(md, encoding="utf-8")
    print(f"  -> tournament_rules.md ({len(md):,} chars)")

    # 3. Patch notes (OCR)
    patch_files = {
        "01. core rules patch notes.txt": "Core Rules Patch Notes",
        "02. spiritforge rules patch notes.txt": "Spiritforge Rules Patch Notes",
        "03. unleash rules patch notes.txt": "Unleash Rules Patch Notes",
        "04. vendetta rules patch notes.txt": "Vendetta Rules Patch Notes",
    }
    for filename, title in patch_files.items():
        print(f"Convirtiendo {filename}...")
        raw = (RAW_DIR / filename).read_text(encoding="utf-8")
        md = patch_notes_to_markdown(raw, title)
        out_name = filename.replace(".txt", ".md").replace(". ", "_")
        (MD_DIR / out_name).write_text(md, encoding="utf-8")
        print(f"  -> {out_name} ({len(md):,} chars)")

    # 4. Legality (OCR - simple cleanup)
    for filename in ["constructed format legality.txt", "2v2 constructed legality.txt"]:
        print(f"Convirtiendo {filename}...")
        raw = (RAW_DIR / filename).read_text(encoding="utf-8")
        clean = clean_ocr_text(raw)
        title = filename.replace(".txt", "").title()
        md = f"# {title}\n\n{clean}"
        out_name = filename.replace(" ", "_").replace(".txt", ".md")
        (MD_DIR / out_name).write_text(md, encoding="utf-8")
        print(f"  -> {out_name} ({len(md):,} chars)")

    print("\n=== Conversion completa ===")
    for f in sorted(MD_DIR.iterdir()):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
