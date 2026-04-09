import asyncio
import logging
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from schema.models import OrchestratorState, Task, AnalysisResult, Report
from agents.supervisor import SupervisorAgent
from agents.data_analyst import DataAnalystAgent
from agents.report_generator import ReportGeneratorAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiAgentOrchestrator:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.supervisor = SupervisorAgent(self.llm)
        self.data_analyst = DataAnalystAgent(self.llm)
        self.report_generator = ReportGeneratorAgent(self.llm)

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
            query = state["query"]
            decomposition = self.supervisor.decompose_query(query)
            return {
                "tasks": decomposition.tasks,
                "query": query
            }

        def data_analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
            tasks = state["tasks"]
            analyst_tasks = [t for t in tasks if t.agent == "data_analyst"]
            if analyst_tasks:
                task = analyst_tasks[0].description
                analysis = self.data_analyst.analyze(task)
                return {"analysis_results": analysis}
            return {}

        def report_generator_node(state: Dict[str, Any]) -> Dict[str, Any]:
            analysis = state.get("analysis_results")
            if analysis:
                report = self.report_generator.generate_report(analysis)
                return {"report": report}
            return {}

        def human_approval_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Human-in-the-loop: In real implementation, wait for user input
            logger.info("Waiting for human approval...")
            # For demo, auto-approve
            return {"human_approval": True}

        def router(state: Dict[str, Any]) -> str:
            if not state.get("tasks"):
                return "supervisor"
            if not state.get("analysis_results"):
                return "data_analyst"
            if not state.get("report"):
                return "report_generator"
            if not state.get("human_approval"):
                return "human_approval"
            return END

        graph = StateGraph(OrchestratorState)
        graph.add_node("supervisor", supervisor_node)
        graph.add_node("data_analyst", data_analyst_node)
        graph.add_node("report_generator", report_generator_node)
        graph.add_node("human_approval", human_approval_node)

        graph.add_conditional_edges("supervisor", router)
        graph.add_conditional_edges("data_analyst", router)
        graph.add_conditional_edges("report_generator", router)
        graph.add_conditional_edges("human_approval", router)

        graph.set_entry_point("supervisor")
        return graph.compile()

    async def run(self, query: str) -> Dict[str, Any]:
        logger.info(f"Starting orchestration for query: {query}")
        initial_state: OrchestratorState = {
            "query": query,
            "tasks": [],
            "analysis_results": None,
            "report": None,
            "human_approval": False
        }
        result = await self.graph.ainvoke(initial_state)
        logger.info("Orchestration completed")
        return result


async def main():
    orchestrator = MultiAgentOrchestrator()
    query = "Analyze sales data and generate a quarterly report"
    result = await orchestrator.run(query)
    print(f"Final result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
