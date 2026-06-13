import pytest

from app.pdf_reader import extract_text_from_pdf


def test_extract_text_from_missing_pdf():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("missing_file.pdf")
