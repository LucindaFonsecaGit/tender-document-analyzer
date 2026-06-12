from pydantic import BaseModel
from typing import Optional


class EvaluationCriterion(BaseModel):
    criterion: str
    weight_percent: Optional[int] = None


class TechnicalRequirements(BaseModel):
    functional: list[str] = []
    non_functional: list[str] = []


class TenderAnalysis(BaseModel):
    contracting_authority: str
    tender_title: str
    submission_deadline: str
    project_objectives: list[str]
    scope_of_work: list[str]
    deliverables: list[str]
    evaluation_criteria: list[EvaluationCriterion]
    technical_requirements: TechnicalRequirements
    risks_or_missing_information: list[str]
    summary: str