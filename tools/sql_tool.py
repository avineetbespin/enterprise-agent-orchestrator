from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import logging

logger = logging.getLogger(__name__)


class SQLToolInput(BaseModel):
    query: str = Field(description="The SQL query to execute")


class SQLTool(BaseTool):
    name: str = "sql_tool"
    description: str = "Mock tool to execute SQL queries on a database"
    args_schema: Type[BaseModel] = SQLToolInput

    def _run(self, query: str) -> str:
        logger.info(f"Executing SQL query: {query}")
        # Mock implementation - in real scenario, connect to DB
        if "SELECT" in query.upper():
            return "Mock data: [{'column1': 'value1', 'column2': 'value2'}]"
        return "Mock SQL execution result"

    async def _arun(self, query: str) -> str:
        return self._run(query)