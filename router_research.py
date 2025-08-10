


import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.router.router_llm import LLMRouter

# Create an MCP application
app = MCPApp(name="router_research_agent")

async def run_router_research():
    """
    Run a router-based research workflow that directs different types of research
    queries to specialized agents based on the query content.
    """
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        
        # Create specialized research agents for different domains
        tech_agent = Agent(
            name="technology_researcher",
            instruction="""You are a technology researcher specializing in software, hardware, and digital technologies.
                When asked about technology topics, provide comprehensive, accurate information with technical details.
                Focus on explaining how the technology works, its architecture, and implementation details.""",
            server_names=["fetch", "filesystem"],
        )
        
        science_agent = Agent(
            name="science_researcher",
            instruction="""You are a science researcher specializing in natural sciences, physics, chemistry, and biology.
                When asked about scientific topics, provide evidence-based explanations with references to scientific literature.
                Focus on explaining scientific concepts, theories, and recent discoveries.""",
            server_names=["fetch", "filesystem"],
        )
        
        business_agent = Agent(
            name="business_researcher",
            instruction="""You are a business researcher specializing in business models, market trends, and industry analysis.
                When asked about business topics, provide insights on business strategies, market dynamics, and industry developments.
                Focus on explaining business concepts, case studies, and market analyses.""",
            server_names=["fetch", "filesystem"],
        )

        # Initialize all agents
        async with tech_agent, science_agent, business_agent:
            # Create a router using an LLM to classify and route queries
            router = LLMRouter(
                llm=OpenAIAugmentedLLM(),
                agents=[tech_agent, science_agent, business_agent],
            )
            
            # Example research queries for different domains
            queries = [
                "Explain how Model Context Protocol (MCP) works and its benefits for AI agent development",
                "What are the latest discoveries in quantum computing and how might they impact AI?",
                "Analyze the business model of AI agent platforms and their market potential"
            ]
            
            for i, query in enumerate(queries):
                logger.info(f"Processing query {i+1}: {query}")
                
                # Route the query to the most appropriate agent
                routing_results = await router.route(
                    request=query,
                    top_k=1  # Get the top 1 most relevant agent
                )
                
                if routing_results:
                    chosen_agent = routing_results[0].result
                    logger.info(f"Query routed to: {chosen_agent.name}")
                    
                    # Use the chosen agent to research the query
                    async with chosen_agent:
                        llm = await chosen_agent.attach_llm(OpenAIAugmentedLLM)
                        result = await llm.generate_str(query)
                        
                        logger.info(f"Research result from {chosen_agent.name}:\n{result}")
                        
                        # Save the result to a file
                        result_file_path = f"/workspace/mcp_research_agent/result_{i+1}_{chosen_agent.name}.md"
                        
                        # Format the content as Markdown
                        content = f"""# Research Query {i+1}
## Query
{query}

## Agent
{chosen_agent.name}

## Results
{result}

"""
                        
                        # Use the filesystem server to write the file
                        await chosen_agent.call_tool(
                            name="write_file",
                            arguments={
                                "path": result_file_path,
                                "content": content
                            }
                        )
                        
                        logger.info(f"Research results saved to {result_file_path}")
                else:
                    logger.error(f"Failed to route query: {query}")

if __name__ == "__main__":
    asyncio.run(run_router_research())


