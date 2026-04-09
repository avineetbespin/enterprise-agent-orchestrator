from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schema.models import QueryDecomposition, Task
import logging

logger = logging.getLogger(__name__)


class SupervisorAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=QueryDecomposition)

        self.prompt = ChatPromptTemplate.from_template(
            "You are a supervisor agent. Decompose the following business query into tasks for DataAnalyst and ReportGenerator agents.\n"
            "DataAnalyst: Handles data analysis, SQL queries, web searches.\n"
            "ReportGenerator: Creates reports from analysis results.\n\n"
            "Query: {query}\n\n"
            "Output format: {format_instructions}\n"
        ).partial(format_instructions=self.parser.get_format_instructions())

        self.chain = self.prompt | self.llm | self.parser

    def decompose_query(self, query: str) -> QueryDecomposition:
        logger.info(f"Decomposing query: {query}")
        result = self.chain.invoke({"query": query})
        return result