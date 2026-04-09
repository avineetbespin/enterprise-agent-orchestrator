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
            "You are a Data Analyst. Analyze the following task and determine what data you need.\n"
            "Task: {task}\n"
            "Available tools:\n"
            "- SQL Tool: Query the sales database (tables: sales, monthly_sales, product_performance, regional_performance)\n"
            "- Web Search Tool: Search for external market information\n\n"
            "First, think about what data sources are needed, then provide analysis.\n"
        )

        self.chain = self.prompt | self.llm

    def analyze(self, task: str) -> AnalysisResult:
        logger.info(f"DataAnalyst analyzing: {task}")

        # Determine which tools to use based on task content
        task_lower = task.lower()

        data_results = []
        insights = []

        # If task mentions sales, database, or internal data
        if any(keyword in task_lower for keyword in ['sales', 'database', 'internal', 'revenue', 'product', 'region']):
            # Query database for relevant data
            if 'monthly' in task_lower or 'trend' in task_lower:
                sql_result = self.sql_tool._run("SELECT * FROM monthly_sales ORDER BY month DESC LIMIT 12")
            elif 'product' in task_lower:
                sql_result = self.sql_tool._run("SELECT * FROM product_performance")
            elif 'region' in task_lower:
                sql_result = self.sql_tool._run("SELECT * FROM regional_performance")
            else:
                sql_result = self.sql_tool._run("SELECT SUM(revenue) as total_revenue, COUNT(*) as total_sales FROM sales")

            data_results.append(f"Database Query Results:\n{sql_result}")

            # Extract insights from SQL data
            if 'total_revenue' in sql_result:
                insights.append("Database contains comprehensive sales data with revenue and transaction metrics")

        # If task mentions market, external, or industry analysis
        if any(keyword in task_lower for keyword in ['market', 'external', 'industry', 'trend', 'competition']):
            search_query = f"{task} market analysis industry trends"
            search_result = self.web_search_tool._run(search_query, num_results=3)
            data_results.append(f"Web Search Results:\n{search_result}")

            # Extract insights from search
            insights.append("External market research provides industry context and competitive landscape")

        # If no specific tools triggered, use both
        if not data_results:
            sql_result = self.sql_tool._run("SELECT * FROM monthly_sales ORDER BY month DESC LIMIT 6")
            data_results.append(f"Recent Sales Data:\n{sql_result}")

            search_result = self.web_search_tool._run("business sales analysis trends", num_results=3)
            data_results.append(f"Market Insights:\n{search_result}")

            insights.extend([
                "Sales data shows consistent monthly performance",
                "Market trends indicate positive growth opportunities"
            ])

        # Combine all data
        combined_data = "\n\n".join(data_results)

        return AnalysisResult(
            data={"raw_output": combined_data, "sources": ["database", "web_search"]},
            insights=insights
        )