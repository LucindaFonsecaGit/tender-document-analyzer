from pathlib import Path

from app.pdf_reader import extract_text_from_pdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PDF = PROJECT_ROOT / "sample_documents" / "sample_tender.pdf"


def main():
    if not SAMPLE_PDF.exists():
        raise FileNotFoundError(f"File not found: {SAMPLE_PDF}")

    print(f"Reading {SAMPLE_PDF.name}...")

    text = extract_text_from_pdf(SAMPLE_PDF)

    print(f"Successfully extracted {len(text)} characters.\n")
    print(text[:1000])


if __name__ == "__main__":
    main()