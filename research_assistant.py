
import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.evaluator_optimizer.evaluator_optimizer import EvaluatorOptimizerLLM, QualityRating

# Create an MCP application
app = MCPApp(name="research_assistant_agent")

async def run_research_assistant():
    """
    Run a research assistant agent that can search for information and summarize it.
    The agent uses the fetch MCP server to access web content and the filesystem server to save results.
    """
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        # Create a research assistant agent with access to the fetch and filesystem servers
        research_agent = Agent(
            name="research_assistant",
            instruction="""You are a helpful research assistant that can search for information online.
                You can fetch content from URLs and provide concise, accurate summaries.
                When asked to research a topic, search for relevant information and provide a well-structured summary.
                Always cite your sources with the URLs you used.""",
            server_names=["fetch", "filesystem"],  # Using both fetch and filesystem MCP servers
        )

        # Create an evaluator agent to critique the research
        evaluator_agent = Agent(
            name="research_evaluator",
            instruction="""You are a critical evaluator of research summaries.
                Evaluate the quality, accuracy, and comprehensiveness of research summaries.
                Check if the summary includes proper citations and covers the key aspects of the topic.
                Rate the summary on a scale from POOR to EXCELLENT.""",
            server_names=["fetch"],  # The evaluator can also fetch content to verify information
        )

        async with research_agent, evaluator_agent:
            # Initialize the MCP servers and get available tools
            tools = await research_agent.list_tools()
            logger.info("Available tools:", data=tools)

            # Create an evaluator-optimizer workflow
            eo_llm = EvaluatorOptimizerLLM(
                optimizer=research_agent,
                evaluator=evaluator_agent,
                llm_factory=OpenAIAugmentedLLM,
                min_rating=QualityRating.EXCELLENT,  # Keep iterating until the quality is excellent
                # The max_iterations parameter is not supported in this version
            )

            # Example research query
            query = "What is Model Context Protocol (MCP) and how does it relate to AI agents? Include specific examples of how it's used."
            logger.info(f"Researching: {query}")
            
            # Generate a response using the evaluator-optimizer workflow
            result = await eo_llm.generate_str(
                message=query
            )
            logger.info(f"Research summary:\n{result}")

            # Save the research result to a file
            fs_tools = [tool for tool in tools if tool.get("name") == "write_file"]
            if fs_tools:
                logger.info("Saving research results to file...")
                research_file_path = "/workspace/mcp_research_agent/research_results.md"
                
                # Format the content as Markdown
                content = f"""# Research: Model Context Protocol (MCP) and AI Agents

## Query
{query}

## Results
{result}

"""
                
                # Use the filesystem server to write the file
                await research_agent.call_tool(
                    name="write_file",
                    arguments={
                        "path": research_file_path,
                        "content": content
                    }
                )
                logger.info(f"Research results saved to {research_file_path}")

if __name__ == "__main__":
    asyncio.run(run_research_assistant())
