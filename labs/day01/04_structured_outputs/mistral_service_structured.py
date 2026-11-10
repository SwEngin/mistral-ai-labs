"""
Mistral API Integration with Structured Outputs

Provides structured extraction using Pydantic schemas and client.chat.parse()
"""

import os
from typing import Type, TypeVar
from pydantic import BaseModel
from mistralai.client import Mistral


T = TypeVar('T', bound=BaseModel)


def generate_response(system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
    """
    Send prompts to Mistral and return free-form text response.
    
    (Same as Lab 3 - provided for reference)
    
    Args:
        system_prompt: System instructions for the model
        user_prompt: User message / query
        temperature: Sampling temperature (0.1 = deterministic, 0.7 = creative)
    
    Returns:
        The assistant's response as a string
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is not set")
    
    client = Mistral(api_key=api_key)
    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    
    return response.choices[0].message.content


def generate_structured_response(
    system_prompt: str,
    user_prompt: str,
    response_schema: Type[T],
    temperature: float = 0.1
) -> T:
    """
    Use Mistral's chat.parse() to get validated structured output.
    
    This is the key difference from generate_response():
    - Uses client.chat.parse() instead of client.chat.complete()
    - Passes a Pydantic model as response_format
    - Returns a validated object instance, not a string
    
    Args:
        system_prompt: System instructions for the model
        user_prompt: User message / query
        response_schema: A Pydantic model class (e.g., ProductSpecifications)
        temperature: Sampling temperature (0.1 = deterministic, 0.7 = creative)
    
    Returns:
        An instance of response_schema (validated by Pydantic)
    
    Raises:
        ValueError: If MISTRAL_API_KEY is not set
        ValidationError: If the model's response doesn't match the schema
    
    Example:
        >>> from schemas import ProductSpecifications
        >>> specs = generate_structured_response(
        ...     "You are a product specialist.",
        ...     "Extract specs from: ...",
        ...     ProductSpecifications
        ... )
        >>> print(specs.capacity)  # Access as object
        '5000 mAh'
    """
    # TODO 2: Implement this function
    # Steps:
    # 1. Get MISTRAL_API_KEY from environment or raise ValueError
    # 2. Initialize Mistral client
    # 3. Call client.chat.parse() with:
    #    - model="mistral-small-latest"
    #    - messages list (system + user)
    #    - response_format=response_schema  (KEY: pass the Pydantic model)
    #    - temperature=temperature
    # 4. Extract and return response.choices[0].message.parsed
    #
    # Hint: The main difference from generate_response() is:
    #   - Use client.chat.parse() instead of client.chat.complete()
    #   - Pass response_format parameter
    #   - Return .parsed instead of .content
    
    pass
