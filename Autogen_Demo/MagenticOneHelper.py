import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne
from autogen_agentchat.ui import Console
import yaml

async def example_usage_hil():
    with open(".yaml", "r") as file:
        config = yaml.safe_load(file)
    
    client = OpenAIChatCompletionClient(**config["model_config"])
    # client = OpenAIChatCompletionClient(model="gpt-4o")
    # to enable human-in-the-loop mode, set hil_mode=True
    m1 = MagenticOne(client=client, hil_mode=True)
    task = "Write a Python script to fetch data from an API."
    result = await Console(m1.run_stream(task=task))
    print(result)


if __name__ == "__main__":
    asyncio.run(example_usage_hil())

# import asyncio
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_ext.teams.magentic_one import MagenticOne
# from autogen_agentchat.ui import Console
# import yaml
 
# with open(".yaml", "r") as file:
#     config = yaml.safe_load(file)
 
# client = OpenAIChatCompletionClient(**config["model_config"])
 
# async def example_usage():
#     # client = OpenAIChatCompletionClient(model="gpt-4o")
#     m1 = MagenticOne(client=client)
#     task = "Browse for myanmar earthquake 2025 and summarize it."
#     result = await Console(m1.run_stream(task=task))
#     print(result)
 
# asyncio.run(example_usage())