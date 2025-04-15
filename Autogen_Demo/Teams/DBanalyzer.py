from platform import architecture
import sqlite3
import asyncio
import yaml
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
from typing import Dict, Any

with open("../.yaml", "r") as file:
    config = yaml.safe_load(file)
    model_client = OpenAIChatCompletionClient(**config["model_config"])
    gemma_clinet = OpenAIChatCompletionClient(**config["gemma_config"])
    qwen_client = OpenAIChatCompletionClient(**config["qwen_config"])

def get_db_summary(db_path: str) -> Dict[str, Any]:
    """
    Generates a summary of an SQLite database, including:
    - Table names
    - Schema (columns and data types)
    - Number of rows in each table
    - Foreign key relationships between tables

    Parameters:
        db_path (str): Path to the SQLite .db file. Defaults to 'chinook.db'.

    Returns:
        dict: A dictionary summarizing each table in the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        tables = get_table_names(cursor)
        db_summary = {}

        for table in tables:
            schema = get_table_schema(cursor, table)
            row_count = get_row_count(cursor, table)
            foreign_keys = get_table_foreign_keys(cursor, table)

            db_summary[table] = {
                'schema': schema,
                'row_count': row_count,
                'foreign_keys': foreign_keys
            }

        return db_summary

    finally:
        conn.close()  # Ensure it's closed *after* you're done

def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]

def get_table_schema(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()

def get_row_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    return cursor.fetchone()[0]

def get_table_foreign_keys(cursor, table_name):
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    return cursor.fetchall()

db_analyzer = AssistantAgent(
    name="db_analyzer",
    model_client=model_client,
    system_message="""
    You are a Database Analyzer. Your goal is to analyze the database and provide insights.
    The database should be analyzed and the insights such as table_name, schema, row_count, relationships should be provided in a structured format.
    use tools to provide insights about the db.

    """,
    tools=[get_db_summary],
    description="Analyzes the database and provides insights in a structured format."
)

writer = AssistantAgent(
    name="writer",
    model_client=gemma_clinet,
    system_message="""
    You are a Writer. Your goal is to write a report based on the database insights.
    The report should be written in a structured format.
    Ask for approval to user.
    ---
    output format:
    table:
    schema:
    row_count:
    foreign_keys and realtion:
    """,
    description="Writes a report based on the database insights in a structured format."
)

architect = AssistantAgent(
    name="architect",
    model_client=model_client,
    system_message="""
    You are responsible for any technical and non-technical diagrams.
    You are an Architect and expert in creating er diagram in mermaid format.
    Ask for approval to user.
    ---
    output format:
    .mmd 
    """,
    description="Designs the database based on the report in a structured format."
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    input_func=input
)

team = SelectorGroupChat([db_analyzer, writer, architect, user_proxy], termination_condition=TextMentionTermination("APPROVE"), model_client=model_client)

task="Draw an usecase diagram for ATM."
task="provide an ER diagram for db_path=chinook.db."
asyncio.run(Console(team.run_stream(task=task)))
# Example usage:
# db_path = 'chinook.db'
# summary = get_db_summary()
# for table, info in summary.items():
#     print(f"Table: {table}")
#     print(f"Schema: {info['schema']}")
#     print(f"Row Count: {info['row_count']}")
#     print(f"Foreign Keys: {info['foreign_keys']}")
#     print("\n")