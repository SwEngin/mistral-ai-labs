# Lab 4: Structured Outputs and Classification

**Duration**: 45 minutes  
**Scenario**: Product Evaluation Assistant (now with structured output)  
**Focus**: Machine-readable responses, schema validation, and data contracts

## Objective

Transform the product evaluation assistant from a text-based response into a structured, validated Python object. Learn how to use Pydantic schemas and Mistral's `chat.parse()` API to create machine-readable outputs that other applications can reliably consume.

## Scope: Required vs. Exploration

### ✅ Required (Must Complete in 45 minutes)

- Complete the `ProductSpecifications` schema in `schemas.py`
- Implement the `generate_structured_response()` function in `mistral_service_structured.py`
- Run the application and extract structured specifications
- Observe the response as a typed Python object

**Time estimate**: 30-35 minutes  
**Success criteria**: Application runs and returns structured `ProductSpecifications` object

### 🔍 Exploration (If You Finish Early)

- Test with missing specifications
- Add fields for manufacturer, warranty, or price
- Create a second product with different specifications
- Serialize results to JSON and save to a file
- Experiment with more complex schemas (solar panels, chargers)

## The Problem Lab 4 Solves

In Lab 3, the application returned beautifully formatted text:
```
Capacity: 5000 mAh
Voltage: 3.7V
...
```

But what if you want to:
- Store these specs in a database?
- Compare two products programmatically?
- Feed results into another system?
- Validate that required fields are present?

**You need a structured contract, not free-form text.**

## Architecture Overview

```
04_structured_outputs/
├── README.md                    ← You are here
├── schemas.py                   ← Data model (Pydantic) - YOUR TODO
├── structured_output_app.py     ← Enhanced app using schemas
├── mistral_service_structured.py ← New: parse() method
└── data/
    └── battery_datasheet.txt    ← Reuse from Lab 3
```

## Key Concepts

### 1. Pydantic Models

Instead of extracting text, define a Python class:

```python
from pydantic import BaseModel
from typing import Literal

class ProductSpecifications(BaseModel):
    product_name: str | None        # Optional: may be missing
    category: Literal["battery", "charger", "other"]  # Required
    capacity: str | None            # e.g., "5000 mAh"
    voltage: str | None             # e.g., "3.7V"
```

This is your **data contract**. It defines:
- Which fields are required (no default value)
- Which are optional (set `= None` as default)
- What type each is
- What values are allowed (Literal)

### 2. Structured Output

Instead of `client.chat.complete()`, use `client.chat.parse()`:

```python
response = client.chat.parse(
    model="mistral-small-latest",
    messages=[...],
    response_format=ProductSpecifications  # Pass the schema
)

specs = response.choices[0].message.parsed  # Get validated object
print(specs.capacity)  # Access fields directly
```

### 3. Classification

Use `Literal` types to restrict category values:

```python
category: Literal["battery", "charger", "other"]
```

The model must respond with one of these exact values—not a free-form description.

### 4. Validation Limitations

This is **critical**:
- ✅ Schema ensures **structure** is valid (all required fields present, correct types)
- ❌ Schema cannot ensure **factual accuracy** (model can invent values)
- ❌ Schema cannot ensure **completeness** (model can mark things as None)

Example: The model might invent `"capacity": "999 GW"` and still pass Pydantic validation because it's a valid string.

**That's why prompts matter.** Good prompts reduce hallucinations; schemas validate structure.

## Instructions

### Step 1: Review Mistral's Official Example

Before you start, read the [official structured output quickstart](https://docs.mistral.ai/inference/quickstarts/get-structured-output):

```python
from pydantic import BaseModel
from mistralai.client import Mistral
import os

class Ticket(BaseModel):
    title: str
    priority: int
    customer: str

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
response = client.chat.parse(
    model="mistral-small-latest",
    messages=[{
        "role": "user",
        "content": "Ada from Acme reports that checkout is down. Create a support ticket with priority 1 (urgent) to 3 (low)."
    }],
    response_format=Ticket,
)

ticket = response.choices[0].message.parsed
print(ticket.priority)  # Access as object, not string
```

Pay attention to:
- How Pydantic models are defined
- How `client.chat.parse()` differs from `client.chat.complete()`
- How `.parsed` gives you a typed object

### Step 2: Define the ProductSpecifications Schema

**TODO 1**: Complete `schemas.py`

```python
from typing import Literal, Optional
from pydantic import BaseModel

class ProductSpecifications(BaseModel):
    product_name: str | None
    category: Literal["battery", "charger", "other"]
    # TODO: Add fields for:
    # - capacity (e.g., "5000 mAh")
    # - voltage (e.g., "3.7V")
    # - manufacturer (e.g., "TechPower Industries")
    # - weight (e.g., "185g")
    # Use Optional[str] for fields that may be missing
```

Design decisions:
- Use `Optional[str]` (or `str | None` in Python 3.10+) for fields that might not appear in the product description
- Use `Literal` for restricted choices (category)

### Step 3: Implement Structured API Call

**TODO 2**: Complete the `generate_structured_response()` function in `mistral_service_structured.py`

This function should:
1. Get the `MISTRAL_API_KEY` from environment variables
2. Initialize the Mistral client
3. Call `client.chat.parse()` with:
   - `model="mistral-small-latest"`
   - `messages` list (system + user roles)
   - `response_format=response_schema` (pass the Pydantic model class)
   - `temperature=temperature`
4. Return `response.choices[0].message.parsed` (the validated object)

Reference the [Mistral docs](https://docs.mistral.ai/inference/quickstarts/get-structured-output) for the exact syntax.

### Step 4: Test the Application

**Core Task**: Run the application and see structured output

```bash
python structured_output_app.py
```

The application will:
- Load the product specification
- Extract and classify it using Mistral
- Display individual fields (product name, category, capacity, voltage, manufacturer, etc.)

The application is already orchestrated—just implement the two functions above.

### Step 5: Exploration Challenge — JSON Serialization

**Optional (TODO 1 in the code)**: In `structured_output_app.py`, uncomment the JSON serialization code to also print raw JSON:

```python
# Serialize to JSON
import json
json_output = json.dumps(specs.model_dump(), indent=2)
print("Raw JSON Output:")
print(json_output)
```

This is useful when you need to send the structured data to another system (database, API, file storage).

Create a second product description (e.g., solar panel, charger) with:
- Missing information
- Unusual units or formats
- Different category

Run the application and observe:
- Are missing fields marked as `None`?
- Does classification work correctly?
- Does the model invent values?

## Experimentation Questions

Test these scenarios:

**Scenario 1: Missing Information**
```
Create a product with no capacity specified.
Run the application.
Q: What does specs.capacity contain?
Q: Can you distinguish "not specified" from "hallucinated"?
```

**Scenario 2: Wrong Format**
```
Use a product description with ambiguous units (e.g., "500K for 5000").
Q: Does the model preserve your exact format?
Q: Can it infer the correct interpretation?
```

**Scenario 3: Classification**
```
Use a product description that's not a battery.
Q: Does the model choose the correct category?
Q: What if you give it a solar panel description?
```

**Scenario 4: Schema Validation**
```
Try to make the model invent a specification.
Q: Can Pydantic prevent this? (Hint: No)
Q: What role does the prompt play?
```

## Learning Goals

By the end of Lab 4, you'll understand:

1. **Data Contracts** — Pydantic models define exactly what fields an object must have
2. **Structured Extraction** — `client.chat.parse()` validates output against a schema
3. **Classification** — `Literal` types ensure categorical values are valid
4. **Validation Limits** — Schemas validate structure, not truthfulness
5. **Composition** — How to build reusable structured output functions

## Key Insight

> **Schema validation is not a replacement for good prompts. Together, they ensure both correctness (prompts) and structure (schemas).**

A schema by itself cannot prevent hallucinations. A prompt by itself cannot enforce type safety. Use both.

## Bonus Challenges

**Challenge 1**: Add more fields to `ProductSpecifications`
- Operating temperature range
- Safety certifications
- Warranty period

**Challenge 2**: Create a separate schema for solar panels
```python
class SolarPanelSpecifications(BaseModel):
    product_name: str
    category: Literal["solar_panel"]
    power_output: Optional[str]  # watts
    efficiency: Optional[str]    # percentage
    panel_dimensions: Optional[str]
```

**Challenge 3**: Compare two products
```python
specs1 = analyze_product_structured(product1)
specs2 = analyze_product_structured(product2)
print(f"{specs1.product_name} vs {specs2.product_name}")
```

**Challenge 4**: Implement output validation
```python
def is_valid_extraction(specs: ProductSpecifications) -> bool:
    """Check if extraction meets quality standards."""
    # At least 3 fields must be non-None
    # Category must be present
    # etc.
```

## Troubleshooting

**"Pydantic not found"**
- Run `pip install pydantic`

**"response.choices[0].message.parsed is None"**
- Check that `response_format=YourSchema` is passed to `chat.parse()`
- Verify your schema is a valid Pydantic model

**"ValidationError: field required"**
- Make sure required fields (without `Optional`) are filled by the model
- Or mark them as optional: `field: Optional[str] = None`

**"Model keeps inventing values"**
- This is the validation limitation in action
- Improve your prompt to reduce hallucinations
- Add extraction rules like "Only explicitly stated facts"

## Discussion Points

After completing the lab, think about:

1. **When would you use structured outputs?** (e.g., database inserts, API responses)
2. **When would unstructured text be better?** (e.g., narratives, explanations)
3. **How do you ensure accuracy in structured extractions?** (validation layer? human review? both?)
4. **What happens in production if the model returns invalid data?** (default values? error handling?)

## Getting Help

1. Review the [official Mistral structured output docs](https://docs.mistral.ai/inference/quickstarts/get-structured-output)
2. Check Pydantic documentation: https://docs.pydantic.dev
3. Ask your instructor

---

**Ready?** Start with `schemas.py`. Good luck! 🚀
