from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
import logging

logger = logging.getLogger(__name__)


class WebSearchToolInput(BaseModel):
    query: str = Field(description="The search query")
    num_results: Optional[int] = Field(default=5, description="Number of results to return")


class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "Mock tool to search the web for information"
    args_schema: Type[BaseModel] = WebSearchToolInput

    def _run(self, query: str, num_results: int = 5) -> str:
        logger.info(f"Searching web for: {query}, num_results: {num_results}")
        # Mock implementation - in real scenario, use search API
        results = [f"Mock result {i+1}: Information about {query}" for i in range(num_results)]
        return "\n".join(results)

    async def _arun(self, query: str, num_results: int = 5) -> str:
        return self._run(query, num_results)