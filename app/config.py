import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings:
    project_root: Path = PROJECT_ROOT
    prompt_path: Path = PROJECT_ROOT / "prompts" / "v1" / "extraction_prompt.txt"
    sample_pdf_path: Path = PROJECT_ROOT / "sample_documents" / "sample_tender.pdf"
    output_path: Path = PROJECT_ROOT / "output" / "tender_analysis.json"
    report_path: Path = PROJECT_ROOT / "output" / "report.md"

    llm_api_key: str | None = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    llm_base_url: str | None = os.getenv("LLM_BASE_URL")
    llm_model: str = os.getenv("LLM_MODEL", "openai/gpt-oss-120b:free")

    max_document_length: int = int(os.getenv("MAX_DOCUMENT_LENGTH", "12000"))
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0"))


settings = Settings()