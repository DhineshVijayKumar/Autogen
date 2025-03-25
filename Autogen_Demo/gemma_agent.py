import os
import dotenv
import asyncio
from huggingface_hub import InferenceClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken

# Load environment variables
dotenv.load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Create a custom client for Hugging Face Inference API
class HuggingFaceInferenceClient:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.client = InferenceClient(
            provider="hf-inference",
            api_key=api_key,
        )
    
    async def chat_completion(self, messages, **kwargs):
        # Format messages for the Hugging Face API
        formatted_messages = []
        for msg in messages:
            if msg.role == "system":
                # Skip system messages as they'll be included in the user prompt
                continue
            elif msg.role == "user":
                formatted_messages.append({
                    "role": "user",
                    "content": msg.content
                })
            elif msg.role == "assistant":
                formatted_messages.append({
                    "role": "assistant",
                    "content": msg.content
                })
        
        # Call the Hugging Face API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            max_tokens=kwargs.get("max_tokens", 500),
            temperature=kwargs.get("temperature", 0.7),
        )
        
        # Format the response to match what Autogen expects
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content
                    }
                }
            ]
        }

# Create a calculation tool
async def calculate_sum(numbers: str) -> str:
    """Calculate the sum of numbers"""
    try:
        nums = [float(n) for n in numbers.split()]
        return f"{sum(nums)}"
    except ValueError:
        return "Invalid input"

# Create a weather tool
async def get_current_weather(location: str) -> str:
    """Get weather information"""
    return f"Sunny, 25°C in {location}"

# Initialize the Hugging Face client with Gemma 3
hf_client = HuggingFaceInferenceClient(
    model_name="google/gemma-3-27b-it",
    api_key=HUGGINGFACE_API_KEY,
)

# Create an agent with the Gemma 3 model
gemma_agent = AssistantAgent(
    name="GemmaAssistant",
    model_client=hf_client,
    tools=[calculate_sum, get_current_weather],
    system_message="You are a helpful assistant powered by the Gemma 3 model. For calculations use calculate_sum, for weather use get_current_weather. Keep responses brief."
)

async def process_query(query: str):
    print(f"\n{'='*50}\nProcessing query: {query}\n{'='*50}")
    try:
        await Console(
            gemma_agent.on_messages_stream(
                [TextMessage(content=query, source="user")],
                cancellation_token=CancellationToken(),
            ),
            output_stats=True,
        )
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have accepted the Gemma 3 license at https://huggingface.co/google/gemma-3")

async def main():
    queries = [
        "What's the sum of 42, 17, and 23?",
        "What's the weather in Tokyo?",
        "Explain how photosynthesis works in one sentence."
    ]
    
    for query in queries:
        await process_query(query)
        await asyncio.sleep(1)  # Small delay between queries

# Run the assistant
if __name__ == "__main__":
    asyncio.run(main())