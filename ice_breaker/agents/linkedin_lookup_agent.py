"""
LinkedIn Profile URL Lookup Agent

This module implements a ReAct (Reasoning + Acting) agent using LangChain to find LinkedIn
profile URLs given a person's name. It demonstrates several advanced LangChain concepts:

1. ReAct Agent Pattern: The agent can reason about what to do and take actions iteratively
2. Tool Integration: Uses web search tools to perform external actions
3. Agent Executor: Manages the agent's reasoning loop and tool execution
4. LangChain Hub: Leverages pre-built prompts from the community

ReAct Process Flow:
1. Agent receives a name and reasoning prompt
2. Agent decides it needs to search for LinkedIn profile
3. Agent uses Tavily search tool to find profile URL
4. Agent processes search results and extracts URL
5. Agent returns the final LinkedIn profile URL

This pattern is powerful for multi-step tasks that require external data gathering.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor, AgentType)
from langchain import hub

import os
import sys
from dotenv import load_dotenv

# Fix import path issue - allows importing from sibling directories
# This is needed because the agents/ directory needs to access tools/ directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str: 
    """
    Uses a ReAct agent to find a person's LinkedIn profile URL.
    
    This function demonstrates the ReAct (Reasoning + Acting) pattern where an AI agent:
    1. Reasons about what action to take
    2. Acts by using available tools
    3. Observes the results
    4. Repeats until it has the answer
    
    Args:
        name (str): Full name of the person to search for
        
    Returns:
        str: LinkedIn profile URL or empty string if not found
        
    LangChain Components:
    - ReAct Agent: Multi-step reasoning with tool usage
    - Tool Wrapper: Makes external functions available to the agent
    - Agent Executor: Manages the agent's execution loop
    - LangChain Hub: Uses community-maintained prompts
    """
    
    # Initialize Language Model for Agent Reasoning
    # Using deterministic output (temperature=0) for consistent results
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Define the Agent's Task Template
    # This tells the agent what its goal is and how to format the response
    template = """
        given the full name {name_of_person}, I want you to get back the LinkedIn profile URL. Your answer should ONLY contain a URL.
        If you cannot find it, return an empty string.
    """

    # Create Prompt Template for Agent Task
    # This will be formatted with the person's name at runtime
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"],
        template=template,
    )
    
    # Define Tools Available to the Agent
    # Tools are external functions the agent can call during reasoning
    tools_for_agent = [
        Tool(
            name="crawl Google 4 linkedin profile",  # Tool identifier for agent
            func=get_profile_url_tavily,              # Actual function to execute
            description="useful when you need to find LinkedIn profile URL from a person's name"  # Helps agent decide when to use this tool
        )
    ]

    # Load Pre-built ReAct Prompt from LangChain Hub
    # This is a community-maintained prompt that implements the ReAct pattern
    # It teaches the agent how to reason step-by-step and use tools
    react_prompt = hub.pull("hwchase17/react")
    
    # Create ReAct Agent
    # The agent combines the LLM, tools, and ReAct prompt to enable reasoning
    agent = create_react_agent(
        llm=llm,                    # Language model for reasoning
        tools=tools_for_agent,      # Available tools/actions
        prompt=react_prompt,        # ReAct reasoning template
    )

    # Create Agent Executor
    # This manages the agent's execution loop, handling tool calls and reasoning iterations
    # verbose=True shows the agent's reasoning process (useful for debugging)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    # Execute Agent with Task
    # The agent will iteratively reason and act until it finds the LinkedIn URL
    result = agent_executor.invoke({"input": prompt_template.format_prompt(name_of_person=name)})

    # Extract Final Answer
    # The agent executor returns a dictionary with the final output
    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    # Example usage: Find LinkedIn profile URL
    linkedin_url = lookup(name="Yannick Folla")
    print(linkedin_url)
    