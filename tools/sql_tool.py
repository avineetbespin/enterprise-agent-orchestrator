from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import logging
import sqlite3
import pandas as pd

logger = logging.getLogger(__name__)


class SQLToolInput(BaseModel):
    query: str = Field(description="The SQL query to execute on the sales database")


class SQLTool(BaseTool):
    name: str = "sql_tool"
    description: str = "Execute SQL queries on the sales database. Available tables: sales, monthly_sales, product_performance, regional_performance"
    args_schema: Type[BaseModel] = SQLToolInput

    def __init__(self):
        super().__init__()
        self._db_path = "data/sales.db"

    def _run(self, query: str) -> str:
        logger.info(f"Executing SQL query: {query}")
        try:
            conn = sqlite3.connect(self._db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()

            if df.empty:
                return "Query executed successfully. No results returned."

            # Format the results nicely
            result = f"Query Results ({len(df)} rows):\n"
            result += df.to_string(index=False)
            return result

        except Exception as e:
            logger.error(f"SQL query failed: {e}")
            return f"Error executing query: {str(e)}"

    async def _arun(self, query: str) -> str:
        return self._run(query)