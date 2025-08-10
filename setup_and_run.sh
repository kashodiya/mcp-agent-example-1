

#!/bin/bash

# Setup script for MCP Research Agent examples

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for filesystem server
echo "Installing Node.js dependencies for filesystem server..."
npm install -g @modelcontextprotocol/server-filesystem

# Check if secrets file exists, if not create from example
if [ ! -f "mcp_agent.secrets.yaml" ]; then
    echo "Creating secrets file from example..."
    cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
    echo "Please edit mcp_agent.secrets.yaml to add your API keys"
fi

# Display menu for running examples
echo ""
echo "Setup complete! Choose an example to run:"
echo "1) Basic Research Assistant (research_assistant.py)"
echo "2) Parallel Research Assistant (parallel_research.py)"
echo "3) Router Research Assistant (router_research.py)"
echo "q) Quit"
echo ""

read -p "Enter your choice: " choice

case $choice in
    1)
        echo "Running Basic Research Assistant..."
        python research_assistant.py
        ;;
    2)
        echo "Running Parallel Research Assistant..."
        python parallel_research.py
        ;;
    3)
        echo "Running Router Research Assistant..."
        python router_research.py
        ;;
    q|Q)
        echo "Exiting..."
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

# Deactivate virtual environment
deactivate

