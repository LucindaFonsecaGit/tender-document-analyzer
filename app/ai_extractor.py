from app.config import settings
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.models import TenderAnalysis


load_dotenv()


def load_prompt() -> str:
    return settings.prompt_path.read_text(encoding="utf-8")


def get_demo_analysis() -> TenderAnalysis:
    return TenderAnalysis(
        contracting_authority={
            "value": "Municipality of Example City",
            "confidence": 0.95,
            "page": 1,
            "quote": "The contracting authority is the Municipality of Example City."
        },
        tender_title={
            "value": "Public Tender for Administrative Process Automation",
            "confidence": 0.92,
            "page": 1,
            "quote": "Public Tender for Administrative Process Automation."
        },
        submission_deadline={
            "value": "2026-07-15",
            "confidence": 0.90,
            "page": 2,
            "quote": "Proposals must be submitted by 2026-07-15."
        },
        estimated_budget={
            "value": "€75,000",
            "confidence": 0.88,
            "page": 3,
            "quote": "The estimated contract value is €75,000."
        },
        project_objectives=[
            "Reading tender documentation (PDF, Word, Excel)",
            "Extracting technical requirements",
            "Suggesting budget estimates",
            "Identifying missing information",
            "Generating draft procurement documents"
        ],
        scope_of_work=[
            "Phase 1 – Discovery: Requirements gathering, stakeholder workshops, current process analysis; deliverables: Business Requirements Document (BRD), Functional Specification, Solution Architecture",
            "Phase 2 – AI Development: Develop AI components for OCR processing, document classification, information extraction, cost estimation suggestions, risk identification, natural language search"
        ],
        deliverables=[
            "Technical proposal",
            "Financial proposal",
            "Company registration certificate",
            "Tax compliance certificate",
        ],
        evaluation_criteria=[
            {
                "criterion": "Technical Solution",
                "weight_percent": 40
            },
            {
                "criterion": "Relevant Experience",
                "weight_percent": 20
            }
        ],
        technical_requirements={
            "functional": [
                "Support English and Portuguese",
                "Process PDF files up to 500 pages"
            ],
            "non_functional": [
                "Availability 99.9%",
                "Authentication via Microsoft Entra ID"
            ]
        },
        risks_or_missing_information=[
            "Integration details are not fully specified",
            "Data format requirements need clarification",
            "Acceptance criteria should be confirmed",
        ],
        summary=(
            "This tender concerns the implementation of a digital solution "
            "to support administrative process automation and reporting."
        ),
    )


def clean_json_response(content: str) -> str:
    content = content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]

        if content.startswith("json"):
            content = content[4:]

        content = content.strip()

    return content


def _split_pages(document_text: str) -> list[tuple[int, str]]:
    pages: list[tuple[int, str]] = []
    current_page: int | None = None
    current_lines: list[str] = []

    for line in document_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("===== PAGE ") and stripped.endswith("====="):
            if current_page is not None:
                pages.append((current_page, "\n".join(current_lines).strip()))

            number_text = stripped.replace("===== PAGE ", "").replace(" =====", "")
            try:
                current_page = int(number_text)
            except ValueError:
                current_page = None

            current_lines = []
        else:
            current_lines.append(line)

    if current_page is not None:
        pages.append((current_page, "\n".join(current_lines).strip()))

    return pages


def _short_quote_around(page_text: str, search_value: str) -> str | None:
    if not search_value:
        return None

    compact_text = " ".join(page_text.split())
    compact_value = " ".join(search_value.split())

    lower_text = compact_text.lower()
    lower_value = compact_value.lower()

    index = lower_text.find(lower_value)
    if index == -1:
        return None

    start = max(0, index - 80)
    end = min(len(compact_text), index + len(compact_value) + 80)
    return compact_text[start:end].strip()


def _find_evidence(document_text: str, value: str | None) -> tuple[int | None, str | None]:
    if not value or value.lower() == "not specified":
        return None, None

    pages = _split_pages(document_text)

    for page_number, page_text in pages:
        quote = _short_quote_around(page_text, value)
        if quote:
            return page_number, quote

    return None, None


def _normalise_evidence_fields(data: dict, document_text: str) -> dict:
    evidence_fields = [
        "contracting_authority",
        "tender_title",
        "submission_deadline",
        "estimated_budget",
    ]

    for field_name in evidence_fields:
        field = data.get(field_name)

        if not isinstance(field, dict):
            data[field_name] = {
                "value": field,
                "confidence": 0.0,
                "page": None,
                "quote": None,
            }
            field = data[field_name]

        # Backwards compatibility with older prompt versions that returned "evidence".
        if not field.get("quote") and field.get("evidence"):
            field["quote"] = field.get("evidence")

        field.pop("evidence", None)

        value = field.get("value")
        page = field.get("page")
        quote = field.get("quote")

        # If the model found a value but did not provide page/quote, derive it from the page markers.
        if value and str(value).lower() != "not specified" and (not page or not quote):
            derived_page, derived_quote = _find_evidence(document_text, str(value))
            field["page"] = page or derived_page
            field["quote"] = quote or derived_quote

        field.setdefault("confidence", 0.0)
        field.setdefault("page", None)
        field.setdefault("quote", None)

    return data


def analyze_tender_text(document_text: str, demo_mode: bool = False) -> TenderAnalysis:
    api_key = settings.llm_api_key
    base_url = settings.llm_base_url
    model = settings.llm_model

    if demo_mode or not api_key:
        print("Running in demo mode. No API key was used.")
        return get_demo_analysis()

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    prompt_template = load_prompt()
    document_excerpt = document_text[: settings.max_document_length]
    prompt = prompt_template.replace("{document_text}", document_excerpt)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You extract structured information from public tender documents.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=settings.temperature,
    )

    content = response.choices[0].message.content
    content = clean_json_response(content)

    data = json.loads(content)

    data = _normalise_evidence_fields(data, document_text)

    print(json.dumps(data, indent=2, ensure_ascii=False))

    return TenderAnalysis(**data)