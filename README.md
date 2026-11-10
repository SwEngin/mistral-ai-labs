# Mistral AI Workshop

Welcome to the Mistral AI Workshop! This repository contains hands-on labs to learn how to work with Mistral's Large Language Models through their Python SDK.

## Workshop Structure

```
mistral-ai-labs/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
└── labs/
    └── day01/
        ├── 01_first_request.py        # Lab 1 starter code
        ├── 01_first_request.md        # Lab 1 instructions
        ├── 02_prompt_engineering.py   # Lab 2 starter code
        ├── 02_prompt_engineering.md   # Lab 2 instructions
        ├── 02_OBSERVATION_TABLE.md    # Lab 2 worksheet
        ├── 03_application/            # Lab 3 starter application
        │   ├── app.py
        │   ├── mistral_service.py
        │   ├── prompts.py
        │   ├── .env.example
        │   ├── data/
        │   │   └── battery_datasheet.txt
        │   └── README.md
        └── 04_structured_outputs/     # Lab 4 structured outputs
            ├── schemas.py
            ├── mistral_service_structured.py
            ├── structured_output_app.py
            └── README.md
```

## Prerequisites

- Python 3.10+
- A Mistral API key (get one at https://console.mistral.ai)

## Setup

1. **Clone the repository** (or extract the files):
   ```bash
   cd mistral-ai-labs
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API key**:
   ```bash
   export MISTRAL_API_KEY="your-api-key-here"  # On Windows: set MISTRAL_API_KEY=your-api-key-here
   ```

## Labs Overview

### Lab 1: First API Request

Learn the basics of sending a request to Mistral's API and handling responses.

- **File**: `labs/day01/01_first_request.py`
- **Topics**: Client initialization, chat completion requests, response handling
- **Format**: Complete TODOs to build the script from scratch
- **Challenge levels**: Required → Exploration → Bonus

**Key skill**: "I can use the Mistral SDK"

### Lab 2: Prompt Engineering and Model Behavior

Understand how prompt design affects model output, consistency, and data quality. Discover that good prompts improve behavior, but aren't sufficient alone.

- **File**: `labs/day01/02_prompt_engineering.py`
- **Topics**: Prompt design, few-shot examples, temperature control, data validation
- **Format**: Modify variables in a working script; observe results and record findings
- **Challenge levels**: Improve prompt → Few-shot example → Temperature comparison

**Key skill**: "I understand the limits of prompt engineering and why validation matters"

**Scenario**: Build a product evaluation assistant that extracts specifications from product descriptions.

### Lab 3: Build Your First Python Application

Turn your prompt engineering experiments into a properly organized, reusable Python application. Learn application architecture and module separation.

- **Directory**: `labs/day01/03_application/`
- **Topics**: Module architecture, separation of concerns, configuration management, reusability
- **Format**: Complete TODO functions to build a working application from components
- **Challenge levels**: Required (core functions) → Exploration (error handling) → Bonus (logging, validation)

**Key skill**: "I can architect an LLM application and scale it to multiple products"

**Scenario**: Transform the product evaluation assistant from Lab 2 into a modular application that supports any product without code changes.

### Lab 4: Structured Outputs and Classification

Make LLM responses machine-readable using Pydantic schemas and Mistral's structured output API. Learn the difference between structural and factual validation.

- **Directory**: `labs/day01/04_structured_outputs/`
- **Topics**: Pydantic models, `client.chat.parse()`, schema validation, classification, validation limits
- **Format**: Define schemas, implement structured API calls, test edge cases
- **Challenge levels**: Required (core schema) → Exploration (alternate schemas) → Bonus (validation logic)

**Key skill**: "I can extract data as typed objects and understand validation limitations"

**Scenario**: Transform the product evaluation assistant from Lab 3 into a structured output system that returns validated Python objects instead of text.

---

## Quick Start

**First time?** Start with Lab 1:
```bash
cd labs/day01
python 01_first_request.py
```

**Lab 2 — Prompt Engineering**:
```bash
cd labs/day01
python 02_prompt_engineering.py
```

**Lab 3 — Full Application**:
```bash
cd labs/day01/03_application
cp .env.example .env
# Edit .env with your API key
python app.py
```

**Lab 4 — Structured Outputs**:
```bash
cd labs/day01/04_structured_outputs
python structured_output_app.py
```

## Resources

- [Mistral Official Quickstart](https://docs.mistral.ai/inference/quickstarts/send-your-first-request)
- [Mistral API Documentation](https://docs.mistral.ai)
- [Python SDK Repository](https://github.com/mistralai/client-python)

## Notes for Participants

- Each lab builds on the previous one, but you can start anywhere
- Use the official Mistral docs—learning to read documentation is a valuable skill!
- Don't peek at the solutions folder until you've attempted the labs
- Challenges are tiered: Required → Exploration → Bonus

## Getting Help

If you get stuck:
1. Check the official Mistral documentation
2. Revisit the lab README instructions
3. Review the challenge levels—start with the Required level
4. Ask your instructor or classmates

Happy learning! 🚀
