from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schema.models import Report, AnalysisResult
import logging

logger = logging.getLogger(__name__)


class ReportGeneratorAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=Report)

        self.prompt = ChatPromptTemplate.from_template(
            "You are a Report Generator. Create a comprehensive report based on the analysis results.\n"
            "Analysis: {analysis}\n\n"
            "Output format: {format_instructions}\n"
        ).partial(format_instructions=self.parser.get_format_instructions())

        self.chain = self.prompt | self.llm | self.parser

    def generate_report(self, analysis: AnalysisResult) -> Report:
        logger.info("Generating report from analysis")
        result = self.chain.invoke({"analysis": analysis.model_dump_json()})
        return result