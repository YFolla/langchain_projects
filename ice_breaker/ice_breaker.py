"""
Ice Breaker Main Module

This module orchestrates the complete ice-breaker generation process using LangChain.
It demonstrates several key LangChain patterns:
1. Chain Pattern: Linear processing pipeline using the | operator
2. Structured Output: Pydantic-based output parsing for reliable data extraction
3. Multi-LLM Support: Easy switching between different language models
4. Agent Integration: Uses ReAct agent for complex URL discovery

Architecture Flow:
Name Input → LinkedIn URL Discovery (Agent) → Data Scraping → LLM Processing → Structured Output
"""

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser 
from dotenv import load_dotenv
from linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_output_parser, Summary
import os
from typing import Tuple

load_dotenv()

def ice_break_with(name: str) -> Tuple[Summary, str]:
    """
    Main function that generates ice-breaker content for a given person.
    
    This function demonstrates the LangChain chain pattern where data flows through
    multiple processing stages: Agent → Scraper → LLM → Parser
    
    Args:
        name (str): Full name of the person to generate ice-breaker content for
        
    Returns:
        Tuple[Summary, str]: Structured summary object and profile photo URL
        
    LangChain Patterns Used:
    - Agent-based URL discovery with ReAct pattern
    - Chain composition using | operator
    - Structured output parsing with Pydantic
    - Prompt templating with variable substitution
    """
    
    # Step 1: Use ReAct Agent to find LinkedIn profile URL
    # The agent uses web search tools and multi-step reasoning to locate the profile
    linkedin_username = linkedin_lookup_agent(name=name)
    
    # Step 2: Extract profile data from LinkedIn
    # This provides raw data that will be processed by the LLM
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    # Step 3: Initialize Language Model
    # Using OpenAI's GPT-4o-mini with deterministic output (temperature=0)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # Alternative: Local Ollama model (uncomment to use)
    # llm = ChatOllama(model="llama3.3:latest")

    # Step 4: Create Structured Prompt Template
    # The template includes format instructions from the Pydantic parser
    # This ensures the LLM knows exactly what structure to return
    summary_template = """
          given the LinkedIn information {information} about a person, I want you to create a short summary of 2-3 sentences that includes two interesting facts about them.
          \n{format_instructions}
    """

    # Create PromptTemplate with both dynamic variables and partial variables
    # - input_variables: Values provided at runtime (information)
    # - partial_variables: Values set at template creation (format_instructions)
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_output_parser.get_format_instructions()},
    )

    # Step 5: Build LangChain Processing Chain
    # Chain Pattern: prompt → llm → parser
    # Each step processes and transforms the data for the next step
    chain = summary_prompt_template | llm  | summary_output_parser

    # Step 6: Execute the Chain
    # The chain processes: template filling → LLM generation → structured parsing
    result: Summary = chain.invoke({"information": linkedin_data})

    # Step 7: Return structured results
    # Extract profile photo URL from LinkedIn data (fallback handled in Flask app)
    return result, linkedin_data.get("photoUrl")


if __name__ == "__main__":
    print("Hello, Langchain!")
    
    # Example usage: Generate ice-breaker content
    print(ice_break_with(name="Yannick Folla"))