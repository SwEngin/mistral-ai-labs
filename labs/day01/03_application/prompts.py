"""
Prompt Templates for Product Evaluation Assistant

Contains reusable prompts from Lab 2.
Centralizing prompts here makes them easy to refine and version.
"""

# TODO 2: Update these with your best prompts from Lab 2

SYSTEM_PROMPT = """You are a product evaluation assistant.
Your job is to extract technical specifications from product descriptions.
Focus on facts explicitly stated in the description.
Use consistent units and formatting.
Mark information as "Not specified" if not provided.
Never invent specifications."""


def get_user_prompt(product_description: str) -> str:
    """
    Format the product description for analysis.
    
    Args:
        product_description: The raw product specification text
    
    Returns:
        A formatted user prompt ready to send to the model
    """
    # TODO 2 (continued): Format this prompt with extraction rules from Lab 2
    return f"""Extract the technical specifications from this product description:

{product_description}

Return only explicitly stated facts.
Preserve original units and measurements.
Use "Not specified" for missing information.
Do not invent or infer specifications.

Format your response as a clear, structured list."""
