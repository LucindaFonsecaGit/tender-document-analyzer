from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text from a PDF file and preserve page markers for evidence tracking."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    pages: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        pages.append(f"===== PAGE {page_number} =====\n{page_text.strip()}")

    return "\n\n".join(pages)
