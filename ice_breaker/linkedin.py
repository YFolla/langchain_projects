"""
LinkedIn Profile Data Scraper

This module handles the extraction of LinkedIn profile data that feeds into the
LangChain processing pipeline. While not directly using LangChain components,
it provides structured data that the LLM chain processes.

Data Flow Integration:
1. Agent finds LinkedIn URL
2. This module scrapes profile data
3. LangChain processes the data with LLM
4. Structured output is generated

Key Features:
- Mock data support for development/testing
- Production API integration with Scrapin.io
- Data cleaning and filtering
- Structured output for LLM consumption
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrapes LinkedIn profile information for a given profile URL.
    
    This function provides clean, structured data that can be effectively
    processed by Language Models in the LangChain pipeline. It supports
    both mock data (for development) and real API calls (for production).
    
    Args:
        linkedin_profile_url (str): LinkedIn profile URL to scrape
        mock (bool): If True, uses mock data instead of real API call
        
    Returns:
        dict: Cleaned LinkedIn profile data ready for LLM processing
        
    Data Pipeline Role:
    - Provides structured input for LangChain LLM processing
    - Filters out irrelevant/empty fields to reduce token usage
    - Ensures consistent data format for prompt templates
    
    Mock vs Production:
    - Mock: Uses GitHub Gist with sample LinkedIn data (for development)
    - Production: Uses Scrapin.io API for real LinkedIn profile scraping
    """
    
    if mock:
        # Development Mode: Use Mock Data
        # This allows testing the LangChain pipeline without API costs or rate limits
        # Mock data is hosted on GitHub Gist for easy access and updates
        linkedin_profile_url = "https://gist.githubusercontent.com/YFolla/ff1954753eb6354728a292e77ee10795/raw/b177fcc64b7308b8b3a81eddbbb09bf647ed19c6/yfolla_linkedin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    
    else: 
        # Production Mode: Use Real LinkedIn Scraping API
        # Scrapin.io provides LinkedIn profile data through their API
        # Requires API key stored in environment variables
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)
    
    # Extract Person Data from API Response
    # Most LinkedIn scraping APIs wrap the profile data in a "person" object
    data = response.json().get("person")
    
    # Clean and Filter Data for LLM Processing
    # This reduces token usage and improves LLM focus by:
    # 1. Removing empty/null values that don't add information
    # 2. Filtering out noisy fields like certifications
    # 3. Keeping only relevant profile information
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)           # Remove empty values
        and k not in ["certifications"]      # Remove noisy fields
    }
    
    return data

if __name__ == "__main__":
    """
    Example usage and testing.
    
    This demonstrates how to use the scraper in mock mode for development.
    The mock data allows testing the entire LangChain pipeline without
    external API dependencies.
    """
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/yannickfolla/",
            mock=True,  # Use mock data for testing
        )
    )