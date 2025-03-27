from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Create the token provider
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

gemma3 = AzureOpenAIChatCompletionClient(
    model="gemma3:1b",
    base_url="http://127.0.0.1:11434/api/generate.openai.azure.com",
)

primary_agent = AssistantAgent(
    "primary",
    model_client=gemma3,
    system_message="You are a helpful AI assistant.",
)

asyncio.run(Console(primary_agent.run_stream(task="Write a 4 line happy poem about the IT employee.")))


