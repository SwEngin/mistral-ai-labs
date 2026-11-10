import os
from mistralai.client import Mistral

# Initialize the client
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

# ============================================================================
# LAB 2: Prompt Engineering and Model Behavior
# ============================================================================
# Your goal: Extract technical specifications from a product description.
# Complete the exercises below by modifying SYSTEM_PROMPT, USER_PROMPT, 
# and TEMPERATURE. Observe how each change affects the model's output.
# ============================================================================

# Product description (same for all experiments)
PRODUCT_DESCRIPTION = """
The BX-3000 Ultra Lithium is a premium rechargeable lithium-ion battery 
designed for high-performance portable electronics. It features a nominal 
capacity of 5000 mAh with a rated energy of 18.5 Wh. The nominal voltage 
is 3.7V with a maximum voltage of 4.2V. The battery weighs 185 grams and 
measures 85 mm × 65 mm × 12 mm. It supports fast charging up to 2A 
(0-100% in ~2.5 hours) and has a maximum continuous discharge current of 
3.5A. The battery has a cycle life of 500-800 full charge cycles at 80% 
capacity retention. It operates in temperature ranges from 0°C to 45°C. 
The battery is manufactured by TechPower Industries and includes CE, FCC, 
RoHS, and UL certifications. It features over-temperature, over-current, 
and short-circuit protection. The standard warranty is 24 months from 
date of purchase.
"""

# ============================================================================
# EXERCISE 1: Basic Prompt (Try this first)
# ============================================================================
SYSTEM_PROMPT = """You are a product evaluation assistant."""

USER_PROMPT = """Extract the technical specifications from the product description below.

Product description:
{product}
"""

TEMPERATURE = 0.1

print("=" * 80)
print("EXERCISE 1: Basic Prompt")
print("=" * 80)

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT.format(product=PRODUCT_DESCRIPTION)}
    ],
    temperature=TEMPERATURE
)

output_1 = response.choices[0].message.content
print(output_1)
print()

# TODO 1: Improve the system instructions
# Modify SYSTEM_PROMPT above to include extraction rules:
# - Extract ONLY explicitly stated facts
# - Preserve units (mAh, V, kg, A, °C, cycles, $)
# - Use "Not specified" for missing information
# - Avoid inventing details
# - Format results clearly (e.g., as a structured list)

# TODO 2: Add a few-shot example
# Modify USER_PROMPT to include an example of the expected format
# Show what good extraction looks like

# TODO 3: Compare model behavior at different temperatures
# After completing exercises 1 and 2, modify TEMPERATURE and compare
# Try 0.1 (deterministic) vs 0.7 (creative), make multiple requests
