import json
from openai import OpenAI
import os
from pathlib import Path

from dotenv import load_dotenv


from app.models import TenderAnalysis


load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)


BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "extraction_prompt.txt"

def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")

def analyze_tender_text(document_text: str) -> TenderAnalysis:
    prompt_template = load_prompt()

    # Keep the first version simple.
    # Later we can chunk long documents.
    prompt = prompt_template.format(document_text=document_text[:12000])

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You extract structured information from public tender documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    data = json.loads(content)

    print(json.dumps(data, indent=2))
    return TenderAnalysis(**data)