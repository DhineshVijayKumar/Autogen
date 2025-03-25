import os
import dotenv
import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from typing import Dict, List, Any

# Load environment variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the model client with proper parameters for Gemini
model_client = OpenAIChatCompletionClient(
    model="gemini-2.0-flash",
    api_key=GOOGLE_API_KEY,
)

async def get_stock_info(symbol: str) -> Dict[str, Any]:
    return {"price": 100, "volume": 1000, "pe_ratio": 10}

async def get_news(symbol: str) -> List[Dict[str, Any]]:
    return [
        {
            "title": "Tesla Expands Cybertruck Production",
            "date": "2024-03-20",
            "summary": "Tesla ramps up Cybertruck manufacturing capacity at Gigafactory Texas, aiming to meet strong demand.",
        },
        {
            "title": "Tesla FSD Beta Shows Promise",
            "date": "2024-03-19",
            "summary": "Latest Full Self-Driving beta demonstrates significant improvements in urban navigation and safety features.",
        },
        {
            "title": "Model Y Dominates Global EV Sales",
            "date": "2024-03-18",
            "summary": "Tesla's Model Y becomes best-selling electric vehicle worldwide, capturing significant market share.",
        },
    ]

    

#planner agent
planner_agent = AssistantAgent(
    "planner",
    model_client=model_client,
    system_message="""
    You are the planner for the team.

    - First, collect research data from the researcher.
    - Then, collect financial data from the financer.
    - Only when both are available, hand off to the writer.
    - After the writer completes the documentation, verify it and hand off to user_proxy for finalization.

    Track progress:
    - If research is missing, request researcher.
    - If financial data is missing, request financer.
    - If both are available, request writer.

    """,
    handoffs=["resercher", "financer", "writer", "user_proxy"],
) 

#resercher agent
resercher = AssistantAgent(
    "resercher",
    model_client=model_client,
    system_message="""
    You are a helpful AI assistant. You will be the resercher for the team. 
    Use the search_web function to search for information.
    Once the information is found, always handoff to planner.
    """,
    tools=[get_news],
    handoffs=["planner", "financer", "writer"],
) 

#financer
financer = AssistantAgent(
    "financer",
    model_client=model_client,
    system_message="""
    You are a expert finnace advisor and suggester. 
    You will be the financer for the team. Use the get_stock_info function to get stock information.
    
    Once the information is found, always handoff to planner.
    """,
    tools=[get_stock_info],
    handoffs=["planner", "resercher", "writer"],
) 

#writer
writer = AssistantAgent(
    "writer",
    model_client=model_client,
    system_message="""
    You are the writer for the team.

    - Use research and financial data to create a structured report.
    - If you do not have both, return to planner and request missing data.
    - Once documentation is done, hand off to the planner.

    Do NOT send an empty response.
    """,
    handoffs=["planner"],
) 

#user_proxy
user_proxy = UserProxyAgent(
    name="user_proxy",
    description="""
    You are a documentation expert. 
    You will be the user_proxy for the team. Document the findings related to the task and make a text file.
    Terminate the task when you are done by saying "TERMINATE".

    -output format
    create a file inside .docs folder called report.txt
    make markdown format, include title, date, summary, and analysis.
    """,
    input_func=None
)

text_termination = TextMentionTermination("TERMINATE")
termination=text_termination

# task="find Tesla stock information and let me know is it a good time to buy."
task="Conduct market research for TSLA stock"

swarm = Swarm(
    participants=[planner_agent, resercher, financer, writer, user_proxy],
    termination_condition=termination,
)

asyncio.run(Console(swarm.run_stream(task=task)))