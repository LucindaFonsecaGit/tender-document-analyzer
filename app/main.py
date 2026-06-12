from pathlib import Path

from app.pdf_reader import extract_text_from_pdf
from app.ai_extractor import analyze_tender_text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PDF = PROJECT_ROOT / "sample_documents" / "sample_tender.pdf"


def main():
    if not SAMPLE_PDF.exists():
        raise FileNotFoundError(f"File not found: {SAMPLE_PDF}")

    print(f"Reading {SAMPLE_PDF.name}...")

    text = extract_text_from_pdf(SAMPLE_PDF)

    print("PDF text extracted successfully.")
    print("Analyzing tender document with AI...")

    analysis = analyze_tender_text(text)

    print("\nTender Analysis Result:")
    print(analysis.model_dump_json(indent=2))


if __name__ == "__main__":
    main()