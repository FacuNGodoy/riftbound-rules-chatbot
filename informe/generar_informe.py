# -*- coding: utf-8 -*-
"""Genera el informe PDF/DOCX de la entrega final."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor, Cm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG = HERE / "figuras"
DOCX = HERE / "Entrega_final_Riftbound_Chatbot.docx"
PDF = HERE / "Entrega_final_Riftbound_Chatbot.pdf"

NAVY = RGBColor(0x1A, 0x1A, 0x2E)
MAGENTA = RGBColor(0xC4, 0x2B, 0x45)
GRAY = RGBColor(0x44, 0x44, 0x55)

# Completar cuando existan. El script no inventa URLs vivas.
GITHUB = "https://github.com/FacuNGodoy/riftbound-rules-chatbot"
APP_URL = "https://riftbound-rules-chatbot.onrender.com"
FIGMA = (
    "https://www.figma.com/make/AGMq8C6qLXKILCSnCtWujt/"
    "Rifbound---Bienvenida--Copy-?t=0m2XhVKWIFPBIlUx-1"
)
VIDEO = "https://youtu.be/I7B1EFWfUKE"


def set_run_font(run, size=11, bold=False, color=None, name="Calibri", italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        run.font.color.rgb = NAVY if level > 1 else MAGENTA
    return p


def add_p(doc, text, *, size=11, bold=False, space_after=8, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    for run in p.runs:
        set_run_font(run, size=11)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    set_run_font(run, size=9, italic=True, color=GRAY)
    return p


def add_image(doc, path, width=6.2):
    if not Path(path).exists():
        add_p(doc, f"[Falta figura: {path}]", italic=True)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Inches(width))


def shade_header(row):
    from docx.oxml import parse_xml

    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        for old in tcPr.findall(qn("w:shd")):
            tcPr.remove(old)
        tcPr.append(
            parse_xml(
                r'<w:shd {} w:fill="1A1A2E" w:val="clear"/>'.format(
                    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
                )
            )
        )
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                run.font.bold = True
                run.font.size = Pt(9)


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        set_run_font(run, size=9, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
    shade_header(table.rows[0])
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            cell = table.rows[r_i + 1].cells[c_i]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            set_run_font(run, size=9)
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table


def font_pair():
    try:
        return ImageFont.truetype("arial.ttf", 16), ImageFont.truetype("arial.ttf", 13)
    except OSError:
        f = ImageFont.load_default()
        return f, f


def draw_box(d, box, text, font, fill=(15, 52, 96), accent=(233, 69, 96)):
    x1, y1, x2, y2 = box
    d.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=fill, outline=accent, width=3)
    lines = text.split("\n")
    total_h = len(lines) * 20
    y = y1 + (y2 - y1 - total_h) / 2
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        d.text((x1 + (x2 - x1 - tw) / 2, y), line, fill=(255, 255, 255), font=font)
        y += 20


def arrow(d, a, b, accent=(233, 69, 96)):
    d.line([a, b], fill=accent, width=3)
    x2, y2 = b
    d.polygon([(x2, y2), (x2 - 10, y2 - 6), (x2 - 10, y2 + 6)], fill=accent)


def draw_architecture(path: Path):
    w, h = 1500, 720
    img = Image.new("RGB", (w, h), (26, 26, 46))
    d = ImageDraw.Draw(img)
    font, font_s = font_pair()
    draw_box(d, (40, 300, 200, 400), "Jugador", font)
    draw_box(d, (250, 300, 430, 400), "Chat web\n(HTML/JS)", font)
    draw_box(d, (480, 280, 700, 420), "FastAPI\norquestador", font)
    draw_box(d, (760, 40, 1020, 150), "Gemini Vision\n(Ollama local)", font)
    draw_box(d, (760, 180, 1020, 290), "cards.json\nlógica exacta", font)
    draw_box(d, (760, 320, 1020, 430), "ChromaDB\nmemoria reglas", font)
    draw_box(d, (760, 460, 1020, 570), "Historial RAM\nmemoria de turno", font)
    draw_box(d, (1100, 180, 1440, 300), "Gemini Flash\nIA · DRAFT", font)
    draw_box(d, (1100, 340, 1440, 460), "Gemini Lite\nIA · VERIFIER", font)
    arrow(d, (200, 350), (250, 350))
    arrow(d, (430, 350), (480, 350))
    d.line([(700, 310), (760, 95)], fill=(233, 69, 96), width=3)
    d.line([(700, 340), (760, 235)], fill=(233, 69, 96), width=3)
    d.line([(700, 360), (760, 375)], fill=(233, 69, 96), width=3)
    d.line([(700, 390), (760, 515)], fill=(233, 69, 96), width=3)
    arrow(d, (1020, 240), (1100, 240))
    arrow(d, (1270, 300), (1270, 340))
    d.text(
        (40, 660),
        "Violeta = IA generativa. Azul = lógica tradicional / datos. Chroma + historial = memoria persistente y de sesión.",
        fill=(180, 180, 190),
        font=font_s,
    )
    d.text(
        (40, 685),
        "Riftbound Rules Chatbot — arquitectura (entrega final)",
        fill=(180, 180, 190),
        font=font_s,
    )
    img.save(path)


def draw_agents(path: Path):
    w, h = 1400, 520
    img = Image.new("RGB", (w, h), (26, 26, 46))
    d = ImageDraw.Draw(img)
    font, font_s = font_pair()
    boxes = [
        (40, 200, 260, 320, "1. Retrieval\nreglas + cartas"),
        (320, 200, 560, 320, "2. Draft\nGemini Flash"),
        (620, 200, 880, 320, "3. Verifier\n¿hay evidencia?"),
        (940, 40, 1220, 160, "4a. 2ª búsqueda\nsi faltan reglas"),
        (940, 280, 1220, 400, "4b. Respuesta\nal jugador"),
    ]
    for x1, y1, x2, y2, t in boxes:
        draw_box(d, (x1, y1, x2, y2), t, font)
    arrow(d, (260, 260), (320, 260))
    arrow(d, (560, 260), (620, 260))
    d.line([(880, 230), (940, 100)], fill=(233, 69, 96), width=3)
    d.line([(880, 290), (940, 340)], fill=(233, 69, 96), width=3)
    d.line([(1080, 160), (440, 160), (440, 200)], fill=(180, 180, 190), width=2)
    d.text((40, 460), "Ciclo: retrieve → draft → verify → (re-retrieve) → finalize. Una sola re-búsqueda para no quemar cuota.", fill=(180, 180, 190), font=font_s)
    img.save(path)


def draw_sequence(path: Path):
    w, h = 1400, 620
    img = Image.new("RGB", (w, h), (26, 26, 46))
    d = ImageDraw.Draw(img)
    font, font_s = font_pair()
    actors = [("Jugador", 120), ("UI", 400), ("FastAPI", 700), ("Chroma/\ncartas", 1000), ("Gemini", 1280)]
    for name, x in actors:
        draw_box(d, (x - 80, 30, x + 80, 110), name, font_s)
        d.line([(x, 110), (x, 580)], fill=(80, 80, 110), width=2)
    steps = [
        (140, 120, 400, "pregunta + foto"),
        (140, 400, 700, "POST /ask-stream"),
        (180, 700, 1000, "retrieve + card DB"),
        (230, 700, 1280, "draft"),
        (290, 1280, 700, "JSON verifier"),
        (350, 700, 1280, "verify"),
        (420, 700, 400, "SSE result"),
        (480, 400, 120, "ruling + citas"),
    ]
    y0 = 160
    for i, (y, x1, x2, label) in enumerate(steps):
        yy = y0 + i * 50
        xa, xb = sorted((x1, x2))
        d.line([(xa, yy), (xb, yy)], fill=(233, 69, 96), width=2)
        d.text((xa + 8, yy - 18), label, fill=(220, 220, 230), font=font_s)
    img.save(path)


def build():
    FIG.mkdir(parents=True, exist_ok=True)
    arch = FIG / "arquitectura_final.png"
    agents = FIG / "flujo_agentes.png"
    seq = FIG / "secuencia.png"
    draw_architecture(arch)
    draw_agents(agents)
    draw_sequence(seq)

    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Universidad Tecnológica Nacional · FRBA")
    set_run_font(r, size=12, color=NAVY)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Curso de Inteligencia Artificial para Programadores")
    set_run_font(r, size=12, color=GRAY)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.paragraph_format.space_before = Pt(18)
    r = t.add_run("ENTREGA FINAL DE PROYECTO")
    set_run_font(r, size=14, bold=True, color=NAVY)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Riftbound Rules Chatbot")
    set_run_font(r, size=26, bold=True, color=MAGENTA)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Juez de mesa con RAG, visión de cartas y verificación de rulings")
    set_run_font(r, size=12, italic=True)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.paragraph_format.space_before = Pt(12)
    r = t.add_run("Facundo Nahuel Godoy · proyecto individual")
    set_run_font(r, size=11, color=GRAY)

    add_heading(doc, "Links de acceso (el docente evalúa acá)", 1)
    add_p(
        doc,
        "El producto es el repositorio y la app publicada. Este PDF es el índice.",
    )
    add_table(
        doc,
        ["Recurso", "URL"],
        [
            ["Repositorio GitHub", GITHUB],
            ["Aplicación en funcionamiento", APP_URL],
            ["Video de demo", VIDEO],
            ["Prototipo Figma (3 pantallas)", FIGMA],
            ["Log de sesión real", "eval/sesion_real.md en el repo"],
        ],
        col_widths=[5.5, 11.5],
    )
    add_p(
        doc,
        "La app está publicada en Render. El primer acceso después de un rato inactivo "
        "puede tardar ~50 s (plan gratuito). Abrir la URL antes de la corrección.",
        italic=True,
        size=10,
    )
    add_p(
        doc,
        "Cómo verificar en 2 minutos: abrir el repo (README + commits), abrir la URL "
        "pública, preguntar “Si counterean un spell con Repeat, ¿se resuelve el Repeat?” "
        "y chequear que cite 820. Una pregunta de combate (Deathknell vs heal) debería "
        "mencionar la regla 320: durante Cleanup no se resuelve la chain.",
    )

    doc.add_page_break()
    add_heading(doc, "PARTE 1 — El proyecto como aplicación real", 1)
    add_heading(doc, "Sección 1 · Equipo y proyecto", 2)
    add_p(doc, "Integrantes")
    add_table(
        doc,
        ["Nombre", "Rol en el desarrollo"],
        [
            [
                "Facundo Nahuel Godoy",
                "Producto, backend, prompts, ingestión del reglamento, "
                "base de cartas, eval de juez, UI y publicación",
            ]
        ],
        col_widths=[5, 12],
    )
    add_p(
        doc,
        "Nombre del proyecto: Riftbound Rules Chatbot. Es el mismo problema de la "
        "entrega de medio ciclo, ahora implementado: un jugador en partida no puede "
        "hojear el Core Rules para decidir si un Deathknell se resuelve antes o después "
        "del heal de Combat Cleanup. Discord tarda y a veces inventa. La app responde "
        "en español, cita reglas y texto de carta, y se abstiene si no tiene evidencia.",
    )
    add_p(
        doc,
        "Público objetivo: jugadores casuales y competitivos de Riftbound (PC, durante "
        "o después de la partida) y jueces amateur que necesitan citar el texto, no la intuición.",
    )

    add_heading(doc, "Sección 2 · Arquitectura técnica", 2)
    add_p(
        doc,
        "Entrada: texto y, opcionalmente, fotos. El frontend manda FormData a "
        "/ask-stream. FastAPI orquesta. Salida: veredicto, confianza, explicación y citas. "
        "IA: Gemini Vision en producción (minicpm-v local), Gemini draft y verifier. "
        "Tradicional: búsqueda "
        "de cartas en JSON, Chroma, pineado de mecánicas, atajos determinísticos, "
        "validación de IDs de cita. Memoria persistente de conocimiento: ChromaDB en disco "
        "(reglamento indexado). Memoria de sesión: conversation_history en RAM (últimos "
        "10 turnos), se limpia al recargar o POST /reset. No hay base de usuarios.",
    )
    add_image(doc, arch, 6.4)
    add_caption(doc, "Figura 1. Arquitectura general. Componentes IA vs lógica tradicional.")

    add_p(
        doc,
        "Orquestación multi-rol (no es un framework tipo LangChain): el código propio "
        "decide el ciclo. Retrieval elige chunks y cartas. Draft redacta. Verifier ataca "
        "el borrador y exige JSON con citas. Si el veredicto es NO_RESUELTO y trae "
        "missing_rules_query, hay una segunda pasada de retrieval. finalize_ruling() "
        "tira abajo citas que no estén en la evidencia.",
    )
    add_image(doc, agents, 6.4)
    add_caption(doc, "Figura 2. Flujo de agentes / ciclo de decisión.")
    add_image(doc, seq, 6.4)
    add_caption(doc, "Figura 3. Diagrama de secuencia de una consulta completa.")

    add_p(
        doc,
        "Evolución respecto de la entrega de medio ciclo: el diseño ya planteaba RAG + "
        "visión + Gemini. Lo que se implementó después es el ciclo de decisión (draft → "
        "verifier → re-retrieve), la validación determinística de citas, atajos para "
        "interacciones ya juzgadas, el streaming SSE para no dejar la UI en silencio, "
        "y la publicación en Render. La memoria persistente no es un chat histórico en "
        "la nube: es el índice Chroma del reglamento, que sobrevive al reinicio. El "
        "historial de la partida vive en RAM a propósito (privacidad).",
    )
    add_p(doc, "Código Mermaid equivalente (anexo de arquitectura):")
    add_p(
        doc,
        "flowchart LR  |  U[Jugador] --> UI[Chat web] --> API[FastAPI] --> V[Gemini Vision / minicpm-v local] / C[cards.json] / R[ChromaDB] / H[historial] / D[draft] --> F[verifier] --> UI",
        italic=True,
        size=10,
    )

    add_p(doc, "Casos de uso (quién hace qué):")
    add_table(
        doc,
        ["Actor", "Caso de uso", "Resultado"],
        [
            ["Jugador", "Preguntar una regla o interacción", "Ruling + números de regla"],
            ["Jugador", "Adjuntar foto de carta", "Texto oficial desde cards.json"],
            ["Jugador", "Desambiguar (varias prints)", "El bot pide el subtítulo"],
            ["Autor / eval", "Correr judge_cases.json", "Log de aciertos/citas"],
        ],
        col_widths=[4, 6.5, 6.5],
    )

    add_heading(doc, "Sección 3 · Stack tecnológico", 2)
    add_table(
        doc,
        ["Componente", "Tecnología", "Por qué esta y no otra"],
        [
            [
                "Frontend",
                "HTML + JS + CSS",
                "Una pantalla de chat. React no sumaba al TP y complicaba el deploy en PC propia.",
            ],
            [
                "Backend",
                "Python / FastAPI",
                "El ingest y Chroma ya eran Python. FastAPI sirve estáticos y SSE sin un Node extra.",
            ],
            [
                "Base de datos",
                "ChromaDB + JSON",
                "Chroma para RAG del reglamento, con el índice ya construido y versionado. SQLite/Postgres no aportan: no hay usuarios. Las cartas van en JSON para no alucinar el texto.",
            ],
            [
                "Embeddings",
                "API de Gemini (gemini-embedding-001)",
                "Empezó con sentence-transformers local, pero eso arrastra PyTorch y el plan gratuito de Render (512 MB) moría por falta de memoria. Los embeddings por API son multilingües y dejan el servidor sin modelos cargados. Medido: la suite de juez dio el mismo 5/7 antes y después del cambio.",
            ],
            [
                "Modelo de IA",
                "Gemini Flash + Gemini Vision; minicpm-v local",
                "Qwen3 8B local no obedecía el prompt de juez. Flash vigente: gratis y breve. Gemini solo identifica número/nombre de la foto; cards.json aporta el texto exacto. En local puede usarse minicpm-v.",
            ],
            [
                "Orquestación",
                "Código propio (draft/verify/retry)",
                "LangChain hubiera tapado el ciclo que hay que explicar. n8n no corre bien el retrieval de 960 cartas + reglas pineadas.",
            ],
            [
                "Despliegue",
                "Render (Docker, plan Free)",
                "Da una URL HTTPS estable sin depender de la PC. El límite de 512 MB obligó a sacar PyTorch: el índice Chroma se construye antes y los embeddings/visión salen por Gemini API.",
            ],
        ],
        col_widths=[3.2, 4.3, 9.5],
    )

    doc.add_page_break()
    add_heading(doc, "Sección 4 · Evidencia de funcionamiento", 2)
    add_p(
        doc,
        "Capturas de la aplicación publicada en Render "
        "(https://riftbound-rules-chatbot.onrender.com), no de un mock. "
        "El flujo: el jugador entra, pregunta o adjunta una carta, y obtiene veredicto, "
        "confianza, explicación y evidencia clicable.",
    )
    prod1 = FIG / "prod_defy.jpg"
    prod2 = FIG / "prod_repeat.jpg"
    add_image(doc, prod1, 6.2)
    add_caption(
        doc,
        "Figura 4. Producción: foto de Defy identificada por Gemini Vision. "
        "Veredicto SI, confianza ALTA, evidencia Defy (cards.json) y regla 206.",
    )
    add_image(doc, prod2, 6.2)
    add_caption(
        doc,
        "Figura 5. Producción: Repeat + Defy. Veredicto NO, reglas 425.1 y 820.1: "
        "si el hechizo es countereado no hay resolución y Repeat no se ejecuta.",
    )
    add_p(
        doc,
        "Las tres pantallas de diseño (bienvenida, chat, config) siguen en Figma; "
        "abajo se conservan como prototipo de interfaz, no como el sitio live.",
    )
    f1 = FIG / "tp1_p4_1.png"
    f2 = FIG / "tp1_p4_2.png"
    f3 = FIG / "tp1_p5_1.png"
    add_image(doc, f1, 5.2)
    add_caption(doc, "Figura 6. Home / bienvenida (prototipo Figma).")
    add_image(doc, f2, 5.2)
    add_caption(doc, "Figura 7. Flujo principal de consulta (prototipo Figma).")
    add_image(doc, f3, 5.2)
    add_caption(
        doc,
        "Figura 8. Configuración objetivo (Figma). En producción el modo es siempre juez con citas.",
    )
    add_p(
        doc,
        "Output de la IA visible: cada respuesta trae veredicto (SI/NO/RESUELTO/…), "
        "confianza, explicación en español y chips de citas. El frontend muestra estados "
        "intermedios (buscando, generando, verificando) vía SSE.",
    )
    add_p(
        doc,
        "Log de sesión real (datos de juego, no lorem): 2026-08-27, 8 casos de juez. "
        "Pipeline LLM 5/7 (71,4 %). Ejemplo — pregunta: «Si counterean (Defy) un spell "
        "con Repeat, ¿se puede usar el Repeat igual?». Veredicto NO, regla 820.1: Repeat "
        "se ejecuta al resolver; si hay counter, no hay resolución. Detalle completo en "
        "eval/sesion_real.md y eval/results_run1_backup.json.",
        space_after=10,
    )

    doc.add_page_break()
    add_heading(doc, "Sección 5 · Evaluación UX/UI", 2)
    add_heading(doc, "5.1 Heurísticas de Nielsen", 3)
    add_table(
        doc,
        ["Heurística", "¿Cumple?", "Evidencia"],
        [
            [
                "Visibilidad del estado",
                "Sí",
                "Spinner + textos de status del server (searching / draft / verify). El jugador ve que no se colgó.",
            ],
            [
                "Coincidencia con el mundo real",
                "Sí",
                "Vocabulario TCG (countereado, chain, Might), no traducciones inventadas. Navy/magenta de herramienta de juego.",
            ],
            [
                "Control y libertad",
                "Parcial",
                "Hay /reset al recargar. No hay undo de un ruling ya dicho: se hace otra pregunta. Aceptable para un juez, no para un editor.",
            ],
            [
                "Consistencia y estándares",
                "Sí",
                "Chat clásico: burbujas, adjuntar, Enter para enviar. Citas como metadatos, no como otro producto.",
            ],
            [
                "Prevención de errores",
                "Parcial",
                "Si la carta es ambigua (varias prints) el bot pide el subtítulo en vez de rulinear la equivocada. No hay confirmación antes de gastar cuota.",
            ],
            [
                "Reconocimiento sobre recuerdo",
                "Sí",
                "Placeholder, chips de citas, preview de imagen. No hay que recordar números de regla para preguntar.",
            ],
            [
                "Flexibilidad y eficiencia",
                "Parcial",
                "Ctrl+V de fotos, números OGN-xxx y chips de ejemplo (Defy, Deathknell, Repeat).",
            ],
            [
                "Estético y minimalista",
                "Sí",
                "Una columna, sin arte de campeones (copyright y distracción). Config no está en el prototipo código para no competir con el chat.",
            ],
            [
                "Ayuda a reconocer errores",
                "Sí",
                "Si Gemini se queda sin cuota o falla la visión, el mensaje dice qué pasó (cuota vs Ollama caído), no un 500 vacío.",
            ],
            [
                "Ayuda y documentación",
                "Parcial",
                "El saludo inicial explica foto + pregunta. El README es para quien clona, no un help in-app largo.",
            ],
        ],
        col_widths=[4.2, 2.3, 10.5],
    )
    add_heading(doc, "5.2 Público objetivo", 3)
    add_p(
        doc,
        "El usuario final no es un data scientist: es alguien con el mazo en la mesa. "
        "Por eso hay un solo campo de texto, español, y la respuesta va al veredicto "
        "antes que al ensayo. El lenguaje visual (contraste alto, sans-serif) se pensó "
        "para leerlo con mala luz. Prueba informal: se usaron preguntas reales de discordia "
        "de partida (Rex vs Yi / Deathknell, Hidden Blade + Zhonya, Kennen desde Hidden). "
        "Feedback: sirve cuando cita el número de regla; no sirve si se pone verboso o si "
        "cambia el timing. Eso empujó el verifier y los pineados de la 320. No hubo ronda "
        "formal de usability testing con grabación.",
    )

    doc.add_page_break()
    add_heading(doc, "Sección 6 · Ciberseguridad", 2)
    add_table(
        doc,
        ["Riesgo", "Tipo", "Medida o decisión"],
        [
            [
                "Inyección de prompt",
                "Prompt injection / OWASP LLM01",
                "El usuario no edita el system prompt. La query viaja como pregunta. El verifier solo puede citar IDs que ya están en la evidencia recuperada.",
            ],
            [
                "Exposición de API keys",
                "Secretos en código",
                "GEMINI_API_KEY en .env, listado en .gitignore. .env.example sin secreto. La clave que estuvo hardcodeada en una versión local se saca del repo; conviene rotarla en Google AI Studio.",
            ],
            [
                "Fotos y preguntas del jugador",
                "Privacidad",
                "No se guardan imágenes ni historial en disco. En producción la foto se envía a Gemini solo para identificar la carta; el historial vive en RAM. En local puede usarse Ollama para que la imagen no salga de la PC.",
            ],
            [
                "Acceso no autorizado a la URL pública",
                "Autenticación / superficie",
                "No hay login: es un juez público de reglas (dato no sensible). Render expone solo FastAPI, no el filesystem. Riesgo residual: abuso de cuota Gemini si alguien bombardea /ask.",
            ],
            [
                "Alucinación presentada como regla oficial",
                "Integridad / supply de la respuesta",
                "Abstención si no hay citas válidas. cards.json es la fuente del texto de carta, no el LLM. Atajos determinísticos en interacciones ya validadas.",
            ],
        ],
        col_widths=[4.2, 3.8, 9.0],
    )

    add_heading(doc, "Sección 7 · IAs usadas en el co-work", 2)
    add_table(
        doc,
        ["Herramienta", "Para qué", "Aportó bien / mal / sorprendió"],
        [
            [
                "Claude / Cursor",
                "Backend, prompts, eval, este informe",
                "Bien para iterar retrieval y el ciclo draft/verify. Mal cuando inventaba timing; hubo que pinear la 320 a mano.",
            ],
            [
                "Gemini Flash",
                "Modelo de producción del juez",
                "Bien en preguntas simples y en español breve. Mal en Cleanup/Deathknell hasta meter verifier + reglas críticas.",
            ],
            [
                "Qwen3 8B (Ollama)",
                "Intento de juez 100 % local",
                "Mal: verboso, “contado” por countereado, no nombraba la carta. Descartado.",
            ],
            [
                "Gemini Vision / minicpm-v",
                "Leer número/nombre de la foto",
                "Gemini se usa en Render y minicpm-v localmente. Ambos solo identifican; cards.json es la fuente del texto. Al principio minicpm-v mezclaba prints y se agregó Name + Subtitle.",
            ],
            [
                "Figma Make / Leonardo",
                "UI de 3 pantallas y paleta",
                "Figma = entregable. Leonardo = clima visual, no el producto. Make pisaba pantallas al iterar.",
            ],
        ],
        col_widths=[3.5, 4.5, 9.0],
    )
    add_p(
        doc,
        "Reflexión: sin co-work con IA no existiría el cruce de ~960 cartas + Core Rules "
        "en un cuatrimestre de una sola persona (scraper, chunking, system prompt de juez, "
        "suite de casos). La parte que la IA hizo mal y hubo que corregir es el timing de "
        "combate: los modelos afirman con seguridad que Deathknell se resuelve “de inmediato”. "
        "Eso no se arregló con más prosa en el prompt; se arregló con evidencia forzada, un "
        "segundo agente que tiene que atacar el borrador, y un atajo de código en Hidden Blade "
        "+ Zhonya. El criterio humano fue filtrar modelos, no copiar la primera arquitectura.",
    )

    doc.add_page_break()
    add_heading(doc, "PARTE 2 — IA local en el proyecto", 1)
    add_p(
        doc,
        "1. Papel de un LLM/SLM local. Ya hay un SLM local disponible: minicpm-v, "
        "subagente de visión. En Render ese rol lo toma Gemini porque no hay GPU, pero "
        "localmente evita enviar fotos a terceros. No reemplaza a Gemini como juez. Se probó reemplazar el "
        "agente principal con Qwen3 8B y no cumplió el contrato de juez (brevedad, "
        "vocabulario, citar la carta). Un LLM local más capaz (Llama 3.1 70B, etc.) "
        "reemplazaría el draft/verifier para no mandar jugadas de un grupo a Google, "
        "pero no entra en una PC de escritorio razonable. El rol realista hoy: visión + "
        "quizá un filtro de prompt injection, no el Head Judge.",
    )
    add_p(
        doc,
        "2. Aporte al usuario. La visión cambia lo que puede pedir: saca la foto "
        "de la mesa y no tiene que tipear OGN-195. La variante local es más privada (la imagen no viaja a "
        "Gemini) y no tiene costo por token de visión; la variante publicada permite la misma UX sin GPU. No es más rápido en el ruling: el "
        "cuello es Flash + verifier. Un juez 100 % local mejoraría privacidad y seguiría "
        "andando sin internet; hoy, si se corta la API, el bot se abstiene.",
    )
    add_p(
        doc,
        "3. Aporte profesional. Tener Ollama en el loop permitió comparar calidad real, "
        "no slides: se vio el vocabulario roto y se documentó. Si el bot se usara en un club "
        "o tienda, un modelo local dejaría logs de preguntas (qué interacciones duelen) "
        "sin subir partidas a un proveedor. Eso cambia el trabajo día a día: eval sobre "
        "casos propios, no sobre la memoria del modelo de turno que Google retire "
        "(ya pasó con gemini-2.0-flash).",
    )
    add_p(
        doc,
        "4. Limitaciones vs API en la nube. Hardware: esta PC corre minicpm-v; no corre un "
        "juez al nivel de Flash. Calidad: Qwen 8B falló el caso de uso. Cuota y retiro de "
        "modelos: el problema de la nube. Mantenimiento: hay que pullear pesos, versionar "
        "Modelfile y re-correr judge_cases.json cada vez que Ollama actualiza. Conclusión: "
        "híbrido a propósito (visión local opcional y visión/juez por API en producción), no por no haber pensado lo local.",
    )
    add_p(
        doc,
        "Entregable opcional (Ollama): en una terminal, con Ollama instalado, "
        "`ollama run minicpm-v` o `ollama run llama3.2` y preguntar p.ej. “En Riftbound, "
        "¿Deathknell se resuelve antes o después del heal de Combat Cleanup?”. Pegar "
        "captura en el anexo. Sirve para mostrar que lo local responde, y para contrastar "
        "con la respuesta verificada de la app (regla 320).",
        italic=True,
        size=10,
    )

    leonardo = FIG / "tp1_p6_1.png"
    if leonardo.exists():
        add_image(doc, leonardo, 4.0)
        add_caption(doc, "Figura 9. Exploración de estilo (Leonardo.ai) de la entrega anterior: paleta, no el producto.")

    doc.add_page_break()
    add_heading(doc, "Anexo A · Cómo reproducir", 2)
    add_bullet(doc, "Clonar el repo, pip install -r requirements.txt, copiar .env.example → .env.")
    add_bullet(doc, "python ingest.py && uvicorn app:app --port 8000")
    add_bullet(doc, "Túnel: cloudflared tunnel --url http://127.0.0.1:8000")
    add_bullet(doc, "Eval: python eval/run_eval.py --base-url http://127.0.0.1:8000")

    add_heading(doc, "Anexo B · Extracto del log de sesión (2026-08-27)", 2)
    add_p(
        doc,
        "Pregunta: Si juego de Hidden a Kennen, Keeper of Balance, ¿puede stunear cualquier battlefield? "
        "→ NO / ALTA / 811.1.d.2: los targets del play effect desde Hidden tienen que estar en ese battlefield.",
    )
    add_p(
        doc,
        "Pregunta: Si counterean (Defy) un spell con Repeat, ¿se puede usar el Repeat igual? "
        "→ NO / ALTA / 820.1: Repeat ocurre al resolver; sin resolución no hay Repeat.",
    )
    add_p(
        doc,
        "Pregunta: Si Nidalee, Cat Form muere en combate pero quedan unidades, ¿roba igual? "
        "→ NO / ALTA. “I remain after combat” refiere a la carta, no al jugador (053).",
    )
    add_p(
        doc,
        "Pregunta (Rex vs Yi, Deathknell): ¿el daño se resuelve antes o después del heal? "
        "→ INFORMATIVO / ALTA / 320: triggerea en Cleanup y se resuelve después del heal. Yi sobrevive.",
    )
    add_p(
        doc,
        "Pregunta: Hidden Blade vs Zhonya, ¿roba 2? → SI (código determinístico, 359.3.e.14). "
        "Reemplazo del kill ≠ mistarget. JSON completo: eval/results_run1_backup.json.",
    )

    add_p(
        doc,
        "Fin del informe. Historia de trabajo: commits en GitHub (no un ZIP único). "
        "La app debe estar con el túnel levantado al momento de la corrección.",
        space_after=4,
    )

    doc.save(DOCX)
    print(f"DOCX {DOCX}")


if __name__ == "__main__":
    build()
