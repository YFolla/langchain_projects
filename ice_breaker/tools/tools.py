"""
LangChain Tools Module

This module provides external tools that can be used by LangChain agents.
It demonstrates how to integrate third-party services (like web search) into 
LangChain workflows using the Community tools ecosystem.

Tools are essential for agents because they allow AI models to interact with
the external world - searching the web, making API calls, reading files, etc.

Key Concepts:
1. Tool Wrapping: Converting external functions into LangChain-compatible tools
2. LangChain Community: Pre-built integrations with popular services
3. Agent Tool Usage: How agents can call these tools during reasoning
"""

from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    """
    Searches for a person's LinkedIn profile URL using Tavily web search.
    
    This function wraps the Tavily search service in a format that can be used
    by LangChain agents. Tavily is a search API optimized for AI applications,
    providing clean, structured results that are easier for LLMs to process.
    
    Args:
        name (str): Full name of the person to search for
        
    Returns:
        str: Search results containing LinkedIn profile information
        
    LangChain Integration:
    - Uses TavilySearchResults from langchain_community
    - Returns structured search results that agents can process
    - Configured for single result to reduce token usage and improve focus
    
    Tool Design Pattern:
    - Simple interface: takes string input, returns string output
    - Focused purpose: specifically searches for LinkedIn profiles
    - Error handling: Tavily handles API errors and rate limiting
    """
    
    # Initialize Tavily Search Tool
    # max_results=1 keeps the response focused and reduces token usage
    # Tavily is designed for AI applications, so results are LLM-friendly
    search = TavilySearchResults(max_results=1)
    
    # Execute Search with LinkedIn-Specific Query
    # The query format is optimized to find LinkedIn profiles specifically
    # Tavily will return structured results that include URLs, snippets, and metadata
    result = search.run(f"{name} LinkedIn profile")
    
    return result