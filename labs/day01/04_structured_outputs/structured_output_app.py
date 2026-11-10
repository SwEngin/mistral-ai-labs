"""
Product Evaluation Application

Main application workflow that brings together:
- mistral_service: Mistral API integration
- prompts: Prompt templates
- data/: Product specifications

This is the entry point for the application.
"""

import os
import sys
import json
from dotenv import load_dotenv
from schemas import ProductSpecifications
from mistral_service_structured import generate_structured_response

# Load environment variables from .env file (if it exists)
load_dotenv()


# System prompt optimized for structured extraction
SYSTEM_PROMPT = """You are a product specification extraction specialist.

Your task is to extract technical specifications from product descriptions and classify them.

Rules for extraction:
1. Extract ONLY facts explicitly stated in the product description
2. Preserve original units and measurements exactly
3. For missing information, use None (do not invent values)
4. Classify the product into: battery, charger, or other
5. Be precise and factual

Output format: Structured JSON with required fields"""


def get_user_prompt(product_description: str) -> str:
    """Format product description for structured extraction."""
    return f"""Extract product specifications from this description:

<PRODUCT_DESCRIPTION>
{product_description}
</PRODUCT_DESCRIPTION>

Return the extracted specifications in JSON format matching this structure:
- product_name: Name of the product
- category: One of [battery, charger, other]
- capacity: Capacity (e.g., "5000 mAh"), or null if not specified
- voltage: Voltage (e.g., "3.7V"), or null if not specified
- manufacturer: Company name, or null if not specified
- weight: Weight (e.g., "185g"), or null if not specified
- operating_temperature_range: Temperature range (e.g., "0°C to 45°C"), or null
- certifications: Certification list (e.g., "CE, FCC, RoHS"), or null

Extract only explicitly stated facts. Do not invent or infer values."""


def load_product(filepath: str) -> str:
    """
    Load a product specification from a file.
    
    Args:
        filepath: Path to the product file
    
    Returns:
        The product description as a string
    
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Product file not found: {filepath}")


def analyze_product_structured(product_description: str) -> ProductSpecifications:
    """
    Analyze a product and return structured specifications.
    
    Args:
        product_description: The product text to analyze
    
    Returns:
        A ProductSpecifications object with validated fields
    
    Raises:
        ValidationError: If the model's response doesn't match the schema
    """
    user_prompt = get_user_prompt(product_description)
    specs = generate_structured_response(SYSTEM_PROMPT, user_prompt, ProductSpecifications)
    return specs


def main():
    """
    Main application entry point.
    
    Load product → Extract structured specs → Display results → Serialize to JSON
    """
    try:
        print("=" * 70)
        print("Product Evaluation Assistant — Structured Output")
        print("=" * 70)
        print()
        
        # Load product
        print("Loading product specification...")
        # Use relative path from this directory to Lab 3's data
        product_path = "../03_application/data/battery_datasheet.txt"
        product = load_product(product_path)
        print(f"✓ Loaded {len(product)} characters")
        print()
        
        # Analyze product
        print("Analyzing product with Mistral (structured output)...")
        specs = analyze_product_structured(product)
        print("✓ Extraction complete")
        print()
        
        # Display structured results
        print("=" * 70)
        print("EXTRACTED SPECIFICATIONS (Structured)")
        print("=" * 70)
        print()
        
        print(f"Product Name:     {specs.product_name}")
        print(f"Category:         {specs.category}")
        print(f"Capacity:         {specs.capacity}")
        print(f"Voltage:          {specs.voltage}")
        print(f"Manufacturer:     {specs.manufacturer}")
        print(f"Weight:           {specs.weight}")
        print(f"Operating Temp:   {specs.operating_temperature_range}")
        print(f"Certifications:   {specs.certifications}")
        print()
        
        # TODO: Serialize to JSON (Exploration)
        # Uncomment to also print raw JSON:
        # import json
        # json_output = json.dumps(specs.model_dump(), indent=2)
        # print("Raw JSON Output:")
        # print(json_output)
        
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        print("Make sure MISTRAL_API_KEY is set", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
