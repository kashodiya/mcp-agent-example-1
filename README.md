

# MCP Research Assistant Agent

This project demonstrates how to build AI research assistants using the [MCP Agent](https://github.com/lastmile-ai/mcp-agent) framework. The examples showcase different workflow patterns for creating sophisticated AI agents that can search for information, analyze it, and present it in a structured format.

## Overview

The MCP Agent framework is built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), which provides a standardized interface for AI assistants to interact with external tools and services. This project demonstrates how to use MCP Agent to create research assistants that can:

1. Search for information online using the fetch MCP server
2. Save research results using the filesystem MCP server
3. Implement different workflow patterns (basic, evaluator-optimizer, parallel, router)

## Examples

### 1. Basic Research Assistant (`research_assistant.py`)

A simple research assistant that uses the Evaluator-Optimizer workflow pattern to:
- Search for information on a topic
- Generate a summary
- Have an evaluator critique the summary
- Refine the summary until it meets quality standards
- Save the results to a file

### 2. Parallel Research Assistant (`parallel_research.py`)

Demonstrates the Parallel workflow pattern with:
- Multiple specialized agents focusing on different aspects of a topic (technical details, use cases, limitations)
- An aggregator agent that combines their findings into a comprehensive report
- Saving the aggregated results to a file

### 3. Router Research Assistant (`router_research.py`)

Shows the Router workflow pattern by:
- Routing different types of research queries to specialized agents (technology, science, business)
- Processing multiple queries and directing each to the most appropriate agent
- Saving the results from each specialized agent to separate files

## Setup

1. Install the MCP Agent framework:
   ```
   pip install mcp-agent
   ```

2. Configure your API keys:
   - Copy `mcp_agent.secrets.yaml.example` to `mcp_agent.secrets.yaml`
   - Add your OpenAI and/or Anthropic API keys

3. Install required MCP servers:
   ```
   # For fetch server
   pip install mcp-server-fetch
   
   # For filesystem server
   npm install -g @modelcontextprotocol/server-filesystem
   ```

## Running the Examples

Run any of the example scripts:

```bash
# Simple research assistant (recommended)
python simple_agent.py

# Basic research assistant with evaluator-optimizer
python research_assistant.py

# Parallel research with multiple specialized agents
python parallel_research.py

# Router-based research with domain-specific agents
python router_research.py
```

### Example Output

When you run the simple agent, it will:

1. Connect to the fetch MCP server
2. Search for information about Model Context Protocol (MCP)
3. Fetch content from multiple URLs
4. Synthesize the information into a comprehensive response
5. Handle a follow-up question about the benefits of MCP for AI agents

Example command:
```bash
cd /workspace/mcp_research_agent && python simple_agent.py
```

## Key Concepts

- **Agent**: An entity with a specific purpose that has access to MCP servers and can use them via an LLM
- **MCP Server**: A service that exposes tools to agents (e.g., fetch for web access, filesystem for file operations)
- **Workflow Patterns**: Different ways to organize agents (evaluator-optimizer, parallel, router)
- **AugmentedLLM**: An LLM enhanced with tools from MCP servers

## Extending the Examples

You can extend these examples by:
- Adding more specialized agents
- Integrating additional MCP servers
- Implementing other workflow patterns (orchestrator-workers, intent-classifier, swarm)
- Creating a web interface using Streamlit or other frameworks

## Resources

- [MCP Agent Documentation](https://docs.mcp-agent.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

