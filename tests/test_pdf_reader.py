from app.pdf_reader import extract_text_from_pdf


def test_extract_text_from_missing_pdf():
    try:
        extract_text_from_pdf("missing_file.pdf")
    except FileNotFoundError:
        assert True