

import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

# Create an MCP application
app = MCPApp(name="simple_research_agent")

async def run_simple_agent():
    """
    Run a simple research assistant agent that can search for information and summarize it.
    The agent uses the fetch MCP server to access web content.
    """
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        # Create a research assistant agent with access to the fetch server
        research_agent = Agent(
            name="research_assistant",
            instruction="""You are a helpful research assistant that can search for information online.
                You can fetch content from URLs and provide concise, accurate summaries.
                When asked to research a topic, search for relevant information and provide a well-structured summary.
                Always cite your sources with the URLs you used.""",
            server_names=["fetch"],  # Using the fetch MCP server to access web content
        )

        async with research_agent:
            # Initialize the MCP servers and get available tools
            tools = await research_agent.list_tools()
            logger.info("Available tools:", data=tools)

            # Attach an OpenAI LLM to the agent
            llm = await research_agent.attach_llm(OpenAIAugmentedLLM)

            # Example research query
            query = "What is Model Context Protocol (MCP) and how does it relate to AI agents? Include specific examples of how it's used."
            logger.info(f"Researching: {query}")
            
            # Generate a response using the agent
            result = await llm.generate_str(
                message=query
            )
            logger.info(f"Research summary:\n{result}")

            # Follow-up question to demonstrate multi-turn conversation
            follow_up = "What are the key benefits of using MCP for building AI agents?"
            logger.info(f"Follow-up question: {follow_up}")
            
            result = await llm.generate_str(follow_up)
            logger.info(f"Follow-up response:\n{result}")

if __name__ == "__main__":
    asyncio.run(run_simple_agent())

