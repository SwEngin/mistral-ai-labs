"""
Mistral API Integration Module

Provides a reusable interface to the Mistral AI API.
Separates API communication logic from application business logic.
"""

import os
from mistralai.client import Mistral


def generate_response(system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
    """
    Send prompts to Mistral and return the response.
    
    Args:
        system_prompt: System instructions for the model
        user_prompt: User message / query
        temperature: Sampling temperature (0.1 = deterministic, 0.7 = creative)
    
    Returns:
        The assistant's response as a string
    
    Raises:
        ValueError: If MISTRAL_API_KEY is not set
        mistralai.exceptions.MistralException: If the API call fails
    
    Example:
        >>> response = generate_response(
        ...     "You are a helpful assistant.",
        ...     "What is 2+2?"
        ... )
        >>> print(response)
        '4'
    """
    # TODO 1: Implement this function
    # Steps:
    # 1. Get MISTRAL_API_KEY from environment or raise ValueError if not found
    # 2. Initialize Mistral client with the API key
    # 3. Send a chat completion request with the system and user prompts
    # 4. Extract the assistant's message from the response
    # 5. Return the message as a string
    #
    # Hint: Review Lab 1 (01_first_request.py) for the pattern
    # Mistral SDK usage:
    #   - client = Mistral(api_key=api_key)
    #   - response = client.chat.complete(model="mistral-small-latest", messages=[...])
    #   - response.choices[0].message.content
    
    pass
