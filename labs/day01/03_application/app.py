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
from dotenv import load_dotenv
from mistral_service import generate_response
from prompts import SYSTEM_PROMPT, get_user_prompt

# Load environment variables from .env file (if it exists)
load_dotenv()


def load_product(filepath: str) -> str:
    """
    Load a product specification from a file.
    
    Args:
        filepath: Path to the product file (e.g., "data/battery_datasheet.txt")
    
    Returns:
        The product description as a string
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If the file can't be read
    
    Example:
        >>> product = load_product("data/battery_datasheet.txt")
        >>> print(len(product))
        245
    """
    # TODO 3: Implement this function
    # Steps:
    # 1. Open the file at `filepath`
    # 2. Read its contents
    # 3. Return the contents as a string
    # 4. Let exceptions bubble up (file not found, permission denied, etc.)
    
    pass


def analyze_product(product_description: str) -> str:
    """
    Analyze a product using Mistral.
    
    Args:
        product_description: The product text to analyze
    
    Returns:
        The extracted specifications as a string
    
    Example:
        >>> product = load_product("data/battery_datasheet.txt")
        >>> result = analyze_product(product)
        >>> print(result)
        'Capacity: 5000 mAh\nVoltage: 3.7V\n...'
    """
    # TODO 4: Implement this function
    # Steps:
    # 1. Create the user prompt by calling get_user_prompt(product_description)
    # 2. Call mistral_service.generate_response() with SYSTEM_PROMPT and the user prompt
    # 3. Return the response
    
    pass


def main():
    """
    Main application entry point.
    
    Workflow:
    1. Load the product specification from data/battery_datasheet.txt
    2. Analyze it using Mistral
    3. Print the results
    """
    try:
        print("=" * 70)
        print("Product Evaluation Assistant")
        print("=" * 70)
        print()
        
        # Load product
        print("Loading product specification...")
        product = load_product("data/battery_datasheet.txt")
        print(f"✓ Loaded {len(product)} characters")
        print()
        
        # Analyze product
        print("Analyzing product with Mistral...")
        result = analyze_product(product)
        print("✓ Analysis complete")
        print()
        
        # Display results
        print("=" * 70)
        print("EXTRACTION RESULTS")
        print("=" * 70)
        print()
        print(result)
        print()
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
