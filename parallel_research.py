

import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

# Create an MCP application
app = MCPApp(name="parallel_research_agent")

async def run_parallel_research():
    """
    Run a parallel research workflow that uses multiple specialized agents to analyze different
    aspects of a topic and then combines their findings.
    """
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        # Create specialized research agents for different aspects
        technical_agent = Agent(
            name="technical_researcher",
            instruction="""You are a technical researcher specializing in technical details and implementation.
                Focus on the technical aspects, architecture, and implementation details of the topic.
                Provide specific technical information with examples when possible.""",
            server_names=["fetch"],
        )
        
        use_cases_agent = Agent(
            name="use_cases_researcher",
            instruction="""You are a researcher specializing in practical applications and use cases.
                Focus on real-world applications, examples, and case studies related to the topic.
                Provide specific examples of how the technology is being used in practice.""",
            server_names=["fetch"],
        )
        
        limitations_agent = Agent(
            name="limitations_researcher",
            instruction="""You are a critical researcher specializing in identifying limitations and challenges.
                Focus on the current limitations, challenges, and potential drawbacks of the topic.
                Provide a balanced view of what the technology can and cannot do well.""",
            server_names=["fetch"],
        )
        
        # Create an aggregator agent to combine the findings
        aggregator_agent = Agent(
            name="research_aggregator",
            instruction="""You are a research aggregator that combines findings from multiple specialized researchers.
                Synthesize the information from different researchers into a cohesive, well-structured report.
                Ensure the final report is comprehensive, balanced, and addresses technical details, use cases, and limitations.
                Format the report with clear sections and proper citations.""",
            server_names=["fetch", "filesystem"],
        )

        # Initialize all agents
        async with technical_agent, use_cases_agent, limitations_agent, aggregator_agent:
            # Create a parallel workflow
            parallel = ParallelLLM(
                fan_in_agent=aggregator_agent,
                fan_out_agents=[technical_agent, use_cases_agent, limitations_agent],
                llm_factory=OpenAIAugmentedLLM,
            )

            # Example research topic
            topic = "Model Context Protocol (MCP) and its role in AI agent development"
            logger.info(f"Starting parallel research on: {topic}")
            
            # Run the parallel research workflow
            result = await parallel.generate_str(
                f"""Research the following topic thoroughly: {topic}
                
                Provide a comprehensive analysis covering:
                1. Technical details and implementation
                2. Practical use cases and examples
                3. Current limitations and challenges
                
                Each specialized researcher should focus on their area of expertise.
                """
            )
            
            logger.info(f"Parallel research complete. Saving results...")
            
            # Save the research result to a file
            research_file_path = "/workspace/mcp_research_agent/parallel_research_results.md"
            
            # Format the content as Markdown
            content = f"""# Comprehensive Research: {topic}

## Research Query
Comprehensive analysis of {topic} covering technical details, use cases, and limitations.

## Aggregated Results
{result}

"""
            
            # Use the filesystem server to write the file
            await aggregator_agent.call_tool(
                name="write_file",
                arguments={
                    "path": research_file_path,
                    "content": content
                }
            )
            
            logger.info(f"Parallel research results saved to {research_file_path}")

if __name__ == "__main__":
    asyncio.run(run_parallel_research())

