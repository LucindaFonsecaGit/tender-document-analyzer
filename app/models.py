from pydantic import BaseModel, Field
from typing import Optional


class EvaluationCriterion(BaseModel):
    criterion: str
    weight_percent: Optional[int] = None


class TechnicalRequirements(BaseModel):
    functional: list[str] = Field(default_factory=list)
    non_functional: list[str] = Field(default_factory=list)


class AIField(BaseModel):
    value: str | None = None
    confidence: float = 0.0


class Evidence(BaseModel):
    value: str | None = None
    confidence: float = 0.0
    page: int | None = None
    quote: str | None = None


class ReviewStatus(BaseModel):
    reviewed: bool = False
    reviewer: str | None = None
    comments: str | None = None


class TenderAnalysis(BaseModel):
    contracting_authority: Evidence
    tender_title: Evidence
    submission_deadline: Evidence
    estimated_budget: Evidence
    project_objectives: list[str] = Field(default_factory=list)
    scope_of_work: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    evaluation_criteria: list[EvaluationCriterion] = Field(default_factory=list)
    technical_requirements: TechnicalRequirements
    risks_or_missing_information: list[str] = Field(default_factory=list)
    summary: str
    review_status: ReviewStatus = Field(default_factory=ReviewStatus)