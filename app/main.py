from app.config import settings
from pathlib import Path
import argparse

from app.ai_extractor import analyze_tender_text
from app.pdf_reader import extract_text_from_pdf
from app.utils import save_json

SAMPLE_PDF = settings.sample_pdf_path
OUTPUT_PATH = settings.output_path


def main(demo_mode: bool = False) -> None:
    try:
        if not SAMPLE_PDF.exists():
            raise FileNotFoundError(f"File not found: {SAMPLE_PDF}")

        print(f"Reading {SAMPLE_PDF.name}...")

        text = extract_text_from_pdf(SAMPLE_PDF)

        if not text.strip():
            print("No text could be extracted from the PDF.")
            return

        print("PDF text extracted successfully.")
        print("Analyzing tender document...")

        analysis = analyze_tender_text(text, demo_mode=demo_mode)
        result = analysis.model_dump()

        print("\nTender Analysis Result:")
        print(analysis.model_dump_json(indent=2))

        save_json(result, OUTPUT_PATH)

        print(f"\nAnalysis saved to: {OUTPUT_PATH}")

    except FileNotFoundError as error:
        print(error)

    except Exception as error:
        print("An error occurred while analyzing the document.")
        print(f"Details: {error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze a public tender document using AI."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run without calling the AI model."
    )

    args = parser.parse_args()
    main(demo_mode=args.demo)
