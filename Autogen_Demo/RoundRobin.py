import asyncio
import os
import dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
dotenv.load_dotenv()

# ✅ Correctly configure OpenAIChatCompletionClient for Ollama
model_client = OpenAIChatCompletionClient(
    model="gemma3:1b",
    base_url="http://127.0.0.1:11434/v1/",  # ✅ Adjust base URL for Ollama
    api_key="key",  
    model_info={
        "vision": False,
        "function_calling": False,
        "json_output": False,
        "family": "gemma",
    },
    seed=42,
    temperature=0,
)

# Create the primary agent
primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

# Create the critic agent
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="You are a strict critic. Provide constructive feedback. Respond with 'APPROVE' when your feedback is addressed.",
)

# Define a termination condition that stops the task if the critic approves
text_termination = TextMentionTermination("APPROVE")

# Create a team with the primary and critic agents
team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)

# Run the task
asyncio.run(Console(team.run_stream(task="Write a 4-line happy poem about the IT employee.",)))
