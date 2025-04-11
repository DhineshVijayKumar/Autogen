import yaml
import asyncio

from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

# Load model configuration
with open("../.yaml", "r") as file:
    config = yaml.safe_load(file)
model_client = OpenAIChatCompletionClient(**config["model_config"])

# Documentation Agent
documentaion_agent = AssistantAgent(
    name="documentaion_agent",
    model_client=model_client,
    description="""
    You are a Documentation Agent tasked with creating clear, structured, and professional documentation 
    based on research findings. Collaborate with the Web Surfer Agent when external information is needed 
    by explicitly asking them to search.

    Responsibilities:
    - Structure findings in markdown format.
    - Ask the web surfer if more information is required.
    - Finalize the document before handing it off to the writer.
    - Only generate .md files. No programming codes.

    Output format example:
    ```md
    # Document Title
    ## Section 1
    ### Subsection 1.1
    paragraph
    ```
    """,
)

# Web Surfer Agent
web_surfer_agent = MultimodalWebSurfer(
    name="MultimodalWebSurfer",
    model_client=model_client,
    description="""
    You are a Web Surfer Agent specialized in finding relevant, up-to-date information from credible sources.
    
    Your role:
    - Perform accurate web searches for specific topics when asked.
    - Return structured and concise summaries suitable for technical documentation.
    - Ensure sources are trustworthy (e.g., .edu, .gov, reputable news and research sites).

    Only act when explicitly asked to retrieve specific information.
    """,
)

# Writer Agent
writer_agent = CodeExecutorAgent(
    name="writer_agent",
    code_executor=LocalCommandLineCodeExecutor(work_dir="./docs"),
    description="""
    You are a Writer Agent that receives finalized markdown content and writes it to a `.md` file in the docs folder.

    Output rules:
    - Once writing is complete, end the conversation by responding with "APPROVE".
    """
)

# Team with text-based termination
team = SelectorGroupChat(
    [documentaion_agent, web_surfer_agent, writer_agent],
    termination_condition=TextMentionTermination("APPROVE"),
    model_client=model_client
)

# Run the task
asyncio.run(Console(team.run_stream(task="Find 5 research that Nvidia is working on in 2025.")))
