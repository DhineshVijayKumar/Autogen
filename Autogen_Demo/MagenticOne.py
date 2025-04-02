import asyncio
import yaml
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console


# Load model client configuration from YAML
with open(".yaml", "r") as file:
    config = yaml.safe_load(file)

model_client = OpenAIChatCompletionClient(**config["model_config"])

assistant = AssistantAgent(
    name="Assistant",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

critic = AssistantAgent(
    name="Critic",
    model_client=model_client,
    system_message="You are a strict critic. Provide constructive feedback. Respond with 'APPROVE' when your feedback is addressed.",
)

team = MagenticOneGroupChat([assistant, critic], model_client=model_client)

asyncio.run(Console(team.run_stream(task="Write a 4-line happy poem about the IT employee.")))
