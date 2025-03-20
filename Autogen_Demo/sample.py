import os
import dotenv
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the model client
model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=GOOGLE_API_KEY,
)   

async def calculate_sum(numbers: str) -> str:
    """Calculate the sum of numbers"""
    try:
        nums = [float(n) for n in numbers.split()]
        return f"{sum(nums)}"
    except ValueError:
        return "Invalid input"

async def get_current_weather(location: str) -> str:
    """Get weather information"""
    return f"Sunny, 25°C in {location}"

# Create an agent with multiple tools
agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[calculate_sum, get_current_weather],
    system_message="You are a concise assistant. For calculations use calculate_sum, for weather use get_current_weather. Keep responses brief."
)

async def process_query(query: str):
    print(f"\n{'='*50}\nProcessing query: {query}\n{'='*50}")
    await Console(
        agent.on_messages_stream(
            [TextMessage(content=query, source="user")],
            cancellation_token=CancellationToken(),
        ),
        output_stats=True,
    )

async def main():
    queries = [
        "What's the addition of 5 3 2?",
        "What's the weather in New York?",
        "Can you explain photosynthesis in one sentence?"
    ]
    
    for query in queries:
        await process_query(query)
        await asyncio.sleep(1)  # Small delay between queries

# Run the assistant
asyncio.run(main())
