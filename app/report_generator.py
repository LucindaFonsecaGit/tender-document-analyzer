from app.models import TenderAnalysis


def generate_markdown_report(analysis: TenderAnalysis) -> str:
    return f"""# Tender Analysis Report

## Executive Summary

{analysis.summary}

## Key Information

| Field | Value | Confidence | Page |
|---|---|---:|---:|
| Contracting Authority | {analysis.contracting_authority.value or "Not found"} | {analysis.contracting_authority.confidence} | {analysis.contracting_authority.page or "N/A"} |
| Tender Title | {analysis.tender_title.value or "Not found"} | {analysis.tender_title.confidence} | {analysis.tender_title.page or "N/A"} |
| Submission Deadline | {analysis.submission_deadline.value or "Not found"} | {analysis.submission_deadline.confidence} | {analysis.submission_deadline.page or "N/A"} |
| Estimated Budget | {analysis.estimated_budget.value or "Not found"} | {analysis.estimated_budget.confidence} | {analysis.estimated_budget.page or "N/A"} |

## Project Objectives

{format_list(analysis.project_objectives)}

## Scope of Work

{format_list(analysis.scope_of_work)}

## Deliverables

{format_list(analysis.deliverables)}

## Evaluation Criteria

{format_evaluation_criteria(analysis)}

## Functional Requirements

{format_list(analysis.technical_requirements.functional)}

## Non-Functional Requirements

{format_list(analysis.technical_requirements.non_functional)}

## Risks or Missing Information

{format_risks(analysis)}

## Human Review

- Reviewed: {analysis.review_status.reviewed}
- Reviewer: {analysis.review_status.reviewer or "N/A"}
- Comments: {analysis.review_status.comments or "N/A"}
"""


def format_list(items: list[str]) -> str:
    if not items:
        return "- Not identified"

    return "\n".join(f"- {item}" for item in items)


def format_evaluation_criteria(analysis: TenderAnalysis) -> str:
    if not analysis.evaluation_criteria:
        return "- Not identified"

    return "\n".join(
        f"- {item.criterion}: {item.weight_percent or 'N/A'}%"
        for item in analysis.evaluation_criteria
    )

def format_risks(analysis: TenderAnalysis) -> str:
    if not analysis.risks_or_missing_information:
        return "- Not identified"

    return "\n".join(
        (
            f"- **Description:** {risk.description}\n"
            f"  - **Severity:** {risk.severity}\n"
            f"  - **Recommendation:** {risk.recommendation}"
        )
        for risk in analysis.risks_or_missing_information
    )