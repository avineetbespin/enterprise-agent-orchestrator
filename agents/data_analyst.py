from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.sql_tool import SQLTool
from tools.web_search_tool import WebSearchTool
from schema.models import AnalysisResult
import logging

logger = logging.getLogger(__name__)


class DataAnalystAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.sql_tool = SQLTool()
        self.web_search_tool = WebSearchTool()

        self.prompt = ChatPromptTemplate.from_template(
            "You are a Data Analyst. Use the available tools to analyze data and provide insights.\n"
            "Task: {task}\n"
            "Use SQL tool for database queries, Web Search for external information.\n"
        )

        self.chain = self.prompt | self.llm

    def analyze(self, task: str) -> AnalysisResult:
        logger.info(f"DataAnalyst analyzing: {task}")
        # Simple implementation: decide which tool to use based on task
        if "sql" in task.lower() or "database" in task.lower():
            result = self.sql_tool._run("SELECT * FROM sales")  # Mock query
        elif "search" in task.lower() or "web" in task.lower():
            result = self.web_search_tool._run("sales data analysis")
        else:
            result = "Mock analysis result"

        return AnalysisResult(
            data={"raw_output": result},
            insights=["Sales increased by 10%", "Top product is X"]
        )