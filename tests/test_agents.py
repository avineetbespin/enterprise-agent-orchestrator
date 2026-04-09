import pytest
from unittest.mock import Mock, patch
from langchain_openai import ChatOpenAI
from agents.supervisor import SupervisorAgent
from agents.data_analyst import DataAnalystAgent
from agents.report_generator import ReportGeneratorAgent
from schema.models import QueryDecomposition, Task, AnalysisResult, Report


@pytest.fixture
def mock_llm():
    return Mock(spec=ChatOpenAI)


def test_supervisor_decompose_query(mock_llm):
    mock_llm.return_value.invoke.return_value = QueryDecomposition(
        tasks=[
            Task(id="1", description="Analyze data", agent="data_analyst"),
            Task(id="2", description="Generate report", agent="report_generator")
        ]
    )
    supervisor = SupervisorAgent(mock_llm)
    result = supervisor.decompose_query("Test query")
    assert isinstance(result, QueryDecomposition)
    assert len(result.tasks) == 2


def test_data_analyst_analyze(mock_llm):
    with patch('agents.data_analyst.AgentExecutor') as mock_executor:
        mock_executor.return_value.invoke.return_value = {"output": "Mock analysis"}
        analyst = DataAnalystAgent(mock_llm)
        result = analyst.analyze("Test task")
        assert isinstance(result, AnalysisResult)


def test_report_generator_generate_report(mock_llm):
    mock_llm.return_value.invoke.return_value = Report(
        title="Test Report",
        content="Test content",
        recommendations=["Rec 1", "Rec 2"]
    )
    generator = ReportGeneratorAgent(mock_llm)
    analysis = AnalysisResult(data={}, insights=[])
    result = generator.generate_report(analysis)
    assert isinstance(result, Report)
    assert result.title == "Test Report"