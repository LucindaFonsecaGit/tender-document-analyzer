from app.ai_extractor import analyze_tender_text
from app.models import TenderAnalysis


def test_analyze_tender_text_demo_mode():
    result = analyze_tender_text("Sample tender text", demo_mode=True)

    assert isinstance(result, TenderAnalysis)
    assert result.contracting_authority is not None
    assert result.tender_title is not None
    assert len(result.deliverables) > 0