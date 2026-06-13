from app.logger import get_logger

from app.config import settings
from pathlib import Path
import argparse

from app.ai_extractor import analyze_tender_text
from app.pdf_reader import extract_text_from_pdf
from app.utils import save_json

from app.report_generator import generate_markdown_report
from app.utils import save_json, save_markdown

SAMPLE_PDF = settings.sample_pdf_path
OUTPUT_PATH = settings.output_path
REPORT_PATH = settings.report_path

logger = get_logger(__name__)

def main(demo_mode: bool = False) -> None:
    try:
        if not SAMPLE_PDF.exists():
            raise FileNotFoundError(f"File not found: {SAMPLE_PDF}")

        logger.info(f"Reading {SAMPLE_PDF.name}...")

        text = extract_text_from_pdf(SAMPLE_PDF)

        if not text.strip():
            logger.info("No text could be extracted from the PDF.")
            return

        logger.info("PDF text extracted successfully.")
        logger.info("Analyzing tender document...")

        analysis = analyze_tender_text(text, demo_mode=demo_mode)
        result = analysis.model_dump()

        logger.info("\nTender Analysis Result:")
        logger.info(analysis.model_dump_json(indent=2))

        save_json(result, OUTPUT_PATH)

        report = generate_markdown_report(analysis)
        save_markdown(report, str(REPORT_PATH))
        logger.info(f"Report saved to: {REPORT_PATH}")

        logger.info(f"\nAnalysis saved to: {OUTPUT_PATH}")

    except FileNotFoundError as error:
        logger.info(error)

    except Exception as error:
        logger.info("An error occurred while analyzing the document.")
        logger.info(f"Details: {error}")


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
