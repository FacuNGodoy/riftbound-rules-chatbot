"""
Extrae texto de PDFs (pdftotext) e imágenes (Tesseract OCR)
y guarda los resultados en raw_text/
"""

import subprocess
import os
from pathlib import Path

# Rutas
RIFT_DIR = Path(r"C:\Users\Facu\Desktop\chatbot\rift")
OUTPUT_DIR = Path(r"C:\Users\Facu\Desktop\chatbot\chatbot\raw_text")
PDFTOTEXT = r"C:\Users\Facu\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin\pdftotext.exe"
TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# PDFs a extraer
PDFS = [
    "Riftbound Core Rules RUP4.pdf",
    "Riftbound Tournament Rules RUP4.pdf",
]

# Carpetas de imágenes de patch notes
IMAGE_DIRS = [
    "01. core rules patch notes",
    "02. spiritforge rules patch notes",
    "03. unleash rules patch notes",
    "04. vendetta rules patch notes",
]

# Imágenes sueltas
SINGLE_IMAGES = [
    "constructed format legality.jpg",
    "2v2 constructed legality.jpg",
]


def extract_pdf(pdf_path: Path, output_path: Path):
    """Extrae texto de un PDF usando pdftotext."""
    print(f"  PDF: {pdf_path.name}")
    subprocess.run(
        [PDFTOTEXT, "-layout", str(pdf_path), str(output_path)],
        check=True,
    )
    print(f"    -> {output_path.name} ({output_path.stat().st_size:,} bytes)")


def extract_image(image_path: Path, output_path: Path):
    """Extrae texto de una imagen usando Tesseract OCR."""
    print(f"  IMG: {image_path.name}")
    # Tesseract agrega .txt automáticamente al output
    out_base = str(output_path).removesuffix(".txt")
    subprocess.run(
        [TESSERACT, str(image_path), out_base, "-l", "eng"],
        check=True,
        capture_output=True,
    )
    print(f"    -> {output_path.name} ({output_path.stat().st_size:,} bytes)")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Extraer PDFs
    print("\n=== Extrayendo PDFs ===")
    for pdf_name in PDFS:
        pdf_path = RIFT_DIR / pdf_name
        out_name = pdf_path.stem + ".txt"
        extract_pdf(pdf_path, OUTPUT_DIR / out_name)

    # 2. Extraer imágenes de patch notes (concatenadas por carpeta)
    print("\n=== Extrayendo patch notes (imágenes) ===")
    for dir_name in IMAGE_DIRS:
        dir_path = RIFT_DIR / dir_name
        images = sorted(dir_path.glob("*.jpg"), key=lambda p: int(p.stem))
        print(f"\n  Carpeta: {dir_name} ({len(images)} imágenes)")

        # Extraer cada imagen y concatenar en un solo .txt
        combined_text = []
        for img in images:
            temp_out = OUTPUT_DIR / f"_temp_{img.stem}"
            subprocess.run(
                [TESSERACT, str(img), str(temp_out), "-l", "eng"],
                check=True,
                capture_output=True,
            )
            temp_file = OUTPUT_DIR / f"_temp_{img.stem}.txt"
            combined_text.append(f"--- Página {img.stem} ---\n")
            combined_text.append(temp_file.read_text(encoding="utf-8"))
            combined_text.append("\n")
            temp_file.unlink()

        out_name = dir_name + ".txt"
        out_path = OUTPUT_DIR / out_name
        out_path.write_text("\n".join(combined_text), encoding="utf-8")
        print(f"    -> {out_name} ({out_path.stat().st_size:,} bytes)")

    # 3. Extraer imágenes sueltas
    print("\n=== Extrayendo imágenes sueltas ===")
    for img_name in SINGLE_IMAGES:
        img_path = RIFT_DIR / img_name
        out_name = Path(img_name).stem + ".txt"
        extract_image(img_path, OUTPUT_DIR / out_name)

    print("\n=== Extracción completa ===")
    print(f"Archivos en {OUTPUT_DIR}:")
    for f in sorted(OUTPUT_DIR.iterdir()):
        print(f"  {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
