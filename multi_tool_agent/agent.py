import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.tools import agent_tool, google_search
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

GEMINI_MODEL = "gemini-2.0-flash"

search_agent = Agent(
    model=GEMINI_MODEL,
    name='SearchAgent',
    instruction="""
    You're a specialist in Google Search
    """,
    tools=[google_search],
)

root_agent = Agent(
    name="personal_finance_agent",
    model=GEMINI_MODEL,
    description=(
        "Agent to answer questions about personal finance and provide stock recommendations"
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about thei financial data and provide recommendations on stocks to buy or sell by accessing functions from FiMoney's MCP server and the internet"
    ),
    tools=[
        agent_tool.AgentTool(agent=search_agent),
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "mcp-remote",
                    "http://localhost:8080/mcp/stream",
                    "--allow-http"
                ],
            ),
        )
    ]
)
