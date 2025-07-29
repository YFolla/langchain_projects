"""
LangChain Output Parsers Module

This module implements structured output parsing using Pydantic models, which is
a crucial pattern in LangChain for ensuring reliable, consistent LLM responses.

Without structured parsing, LLM outputs can be unpredictable in format, making
them difficult to use in applications. This module solves that by:

1. Defining exact output schemas using Pydantic
2. Providing format instructions to the LLM
3. Parsing and validating LLM responses
4. Ensuring type safety and data consistency

Key LangChain Patterns:
- Pydantic Output Parsing: Structured data extraction from LLM responses
- Schema Validation: Automatic validation of LLM outputs
- Format Instructions: Teaching LLMs how to structure their responses
- Type Safety: Strong typing for reliable application integration
"""

from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Summary(BaseModel):
    """
    Pydantic model defining the expected structure of LLM-generated summaries.
    
    This model serves multiple purposes:
    1. Schema Definition: Defines exactly what fields the LLM should return
    2. Validation: Automatically validates LLM responses match the schema
    3. Type Safety: Provides strong typing for the application
    4. Format Instructions: Generates instructions for the LLM
    
    Fields:
        summary (str): 2-3 sentence summary of the person
        facts (List[str]): List of interesting facts about the person
        
    LangChain Integration:
    - Used by PydanticOutputParser to validate LLM responses
    - Automatically generates format instructions for prompts
    - Ensures consistent output structure across all LLM calls
    """
    
    # Primary summary field with descriptive metadata
    # The Field description helps both developers and the LLM understand the purpose
    summary: str = Field(description="summary of the person")
    
    # Facts as a list to ensure structured, parseable output
    # Using List[str] ensures each fact is a separate string element
    facts: List[str] = Field(description="interesting facts about the person")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Pydantic model to a dictionary for JSON serialization.
        
        This method provides a clean interface for converting the structured
        LLM output to formats needed by web APIs, databases, or other systems.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the summary data
            
        Usage:
        - Flask API responses
        - Database storage
        - Frontend JavaScript consumption
        """
        return {"summary": self.summary, "facts": self.facts}

# Global Output Parser Instance
# This parser is used throughout the application to ensure consistent LLM output formatting
summary_output_parser = PydanticOutputParser(pydantic_object=Summary)

"""
How PydanticOutputParser Works:

1. Format Instructions Generation:
   - Calls summary_output_parser.get_format_instructions()
   - Returns detailed JSON schema instructions for the LLM
   - Instructions are injected into prompt templates

2. LLM Response Processing:
   - LLM generates response following the provided format
   - Parser validates response matches Summary schema
   - Converts raw text to Summary object with type safety

3. Error Handling:
   - Automatically handles parsing errors
   - Provides clear error messages for debugging
   - Ensures application stability with malformed LLM responses

Example Generated Format Instructions:
"The output should be formatted as a JSON instance that conforms to the JSON schema below.

{
  "$defs": {
    "Summary": {
      "properties": {
        "summary": {"description": "summary of the person", "title": "Summary", "type": "string"},
        "facts": {"description": "interesting facts about the person", "items": {"type": "string"}, "title": "Facts", "type": "array"}
      },
      "required": ["summary", "facts"],
      "title": "Summary",
      "type": "object"
    }
  }
}"
"""

