from app.ai_extractor import analyze_tender_text
from app.models import TenderAnalysis


def test_analyze_tender_text_demo_mode():
    result = analyze_tender_text("Sample tender text", demo_mode=True)

    assert isinstance(result, TenderAnalysis)
    assert result.contracting_authority is not None
    assert result.tender_title is not None
    assert len(result.deliverables) > 0

def test_demo_analysis_contains_evidence_fields():
    result = analyze_tender_text("Sample tender text", demo_mode=True)

    assert result.contracting_authority.value is not None
    assert result.contracting_authority.confidence > 0
    assert result.tender_title.value is not None
    assert result.submission_deadline.value is not None