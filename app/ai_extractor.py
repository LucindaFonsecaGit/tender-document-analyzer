import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.models import TenderAnalysis


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "extraction_prompt.txt"


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


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


def analyze_tender_text(document_text: str, demo_mode: bool = False) -> TenderAnalysis:
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL", "openai/gpt-oss-120b:free")

    if demo_mode or not api_key:
        print("Running in demo mode. No API key was used.")
        return get_demo_analysis()

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    prompt_template = load_prompt()
    prompt = prompt_template.replace("{document_text}", document_text[:12000])

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
        temperature=0,
    )

    content = response.choices[0].message.content
    content = clean_json_response(content)

    data = json.loads(content)

    print(json.dumps(data, indent=2, ensure_ascii=False))

    return TenderAnalysis(**data)