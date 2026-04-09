from pydantic import BaseModel
from typing import List, Optional, Dict, Any, TypedDict


class Task(BaseModel):
    id: str
    description: str
    agent: str  # 'data_analyst' or 'report_generator'


class QueryDecomposition(BaseModel):
    tasks: List[Task]


class SQLQuery(BaseModel):
    query: str


class WebSearchQuery(BaseModel):
    query: str
    num_results: Optional[int] = 5


class AnalysisResult(BaseModel):
    data: Dict[str, Any]
    insights: List[str]


class Report(BaseModel):
    title: str
    content: str
    recommendations: List[str]


class OrchestratorState(TypedDict):
    query: str
    tasks: List[Task]
    analysis_results: Optional[AnalysisResult]
    report: Optional[Report]
    human_approval: bool