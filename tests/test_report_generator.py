from app.ai_extractor import get_demo_analysis
from app.report_generator import generate_markdown_report


def test_generate_markdown_report_contains_summary():
    analysis = get_demo_analysis()

    report = generate_markdown_report(analysis)

    assert "# Tender Analysis Report" in report
    assert "Executive Summary" in report
    assert analysis.summary in report