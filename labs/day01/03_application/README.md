# Lab 3: Build Your First Python Application

**Duration**: 45 minutes  
**Scenario**: Product Evaluation Assistant  
**Focus**: Application design, module organization, and reusability

## Objective

Turn your prompt engineering experiments from Lab 2 into a properly organized Python application that can analyze different products without code changes. Learn how to structure an LLM application for real-world use.

## Scope: Required vs. Exploration

### ✅ Required (Must Complete in 45 minutes)

- Implement `generate_response()` in `mistral_service.py`
- Move your Lab 2 prompts into `prompts.py`
- Implement `load_product()` and `analyze_product()` in `app.py`
- Run `python app.py` and see output

**Time estimate**: 35 minutes  
**Success criteria**: Application runs and produces extraction output

### 🔍 Exploration (If You Finish Early)

- Test with a different product file
- Add error handling for missing files
- Print formatted output with section headers
- Add usage statistics (tokens, API time)

## Architecture Overview

```
03_application/
├── app.py                      # Application workflow
├── mistral_service.py          # Reusable Mistral API integration
├── prompts.py                  # Prompts (from your Lab 2 work)
├── data/
│   ├── battery_datasheet.txt   # Product specification
│   └── (more products later)
├── .env.example                # Configuration template
└── README.md                   # This file
```

### Module Responsibilities

**`mistral_service.py`** — Mistral SDK wrapper
- Provides a single `generate_response()` function
- Handles API communication
- Makes the model and configuration testable

**`prompts.py`** — Prompt templates
- System prompts for the assistant
- User prompt formats
- Ensures consistency across the application

**`app.py`** — Application workflow
- `load_product()` — Reads product data from files
- `analyze_product()` — Calls Mistral with the product data
- `main()` — Orchestrates the workflow

**`data/`** — Product specifications
- External text files (not hardcoded)
- Easy to add new products without touching code

**`.env`** — Configuration (local, never committed)
- API key
- Model selection
- Any other runtime settings

## Setup

### 1. Create a Virtual Environment (if not already done)

```bash
cd /path/to/mistral-ai-workshop
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Your API Key

**Option A: Using .env file (Recommended)**

Create a `.env` file in this directory (03_application/):

```bash
cp .env.example .env
# Edit .env and add your Mistral API key
```

The application will automatically load this file.

**Option B: Using environment variable**

Set the API key directly:
```bash
export MISTRAL_API_KEY="your-api-key-here"  # macOS/Linux
set MISTRAL_API_KEY=your-api-key-here       # Windows
```

**Important**: Never commit `.env` to Git. It's already in `.gitignore`.

### 3. Review the Application Structure

Open each file and read the TODOs and docstrings. The structure is already set up—you just need to complete the function implementations.

## Instructions

### Step 1: Implement `mistral_service.py`

Create a reusable function that calls Mistral:

**TODO 1**: Implement `generate_response(system_prompt, user_prompt, temperature=0.1)`
- Initialize the Mistral client from `MISTRAL_API_KEY`
- Send the prompts to `mistral-small-latest`
- Return the assistant's message as a string

**Hint**: Use what you learned in Lab 1. The function should follow this pattern:
1. Create a Mistral client
2. Send a chat completion request
3. Extract and return the response text

### Step 2: Move Your Prompts to `prompts.py`

Copy your best prompts from Lab 2:

**TODO 2**: Define `SYSTEM_PROMPT` and `get_user_prompt(product_description)`
- `SYSTEM_PROMPT` — Your improved system instructions from Lab 2 Exercise 1
- `get_user_prompt()` — A function that formats the user message with the product data

Example format:
```python
def get_user_prompt(product_description):
    return f"""Extract the technical specifications from this product description:

{product_description}

Return only explicitly stated facts..."""
```

### Step 3: Implement the Application Workflow in `app.py`

**TODO 3**: Implement `load_product(filepath)`
- Open and read a text file
- Return the contents as a string
- Handle file not found errors gracefully

**TODO 4**: Implement `analyze_product(product_description)`
- Call `mistral_service.generate_response()` with the prompts and product data
- Return the result

### Step 4: Run the Application

```bash
python app.py
```

You should see the extracted specifications printed to the console.

### Step 5: Exploration Challenge — Test with a Different Product

**Optional**: Verify the application is truly reusable by testing with a different product.

**Simplest approach**: The architecture is already reusable. Just create a new product file and modify the hardcoded path in `app.py` temporarily:

```python
# In app.py, in the main() function:
product = load_product("data/solar_panel_spec.txt")  # Change the path here
```

This demonstrates that the same application can analyze different products by simply pointing to different data files.

**Advanced approach (Exploration+)**: Modify `main()` to accept an optional command-line filename:
```python
if __name__ == "__main__":
    product_file = sys.argv[1] if len(sys.argv) > 1 else "data/battery_datasheet.txt"
    
    try:
        print("=" * 70)
        print("Product Evaluation Assistant")
        print("=" * 70)
        print()
        
        product = load_product(product_file)
        print(f"✓ Loaded {len(product)} characters")
        print()
        
        result = analyze_product(product)
        
        print("=" * 70)
        print("EXTRACTION RESULTS")
        print("=" * 70)
        print(result)
        print("=" * 70)
    except FileNotFoundError as e:
        print(f"Error: {e}")
```

Then test with:
```bash
python app.py data/battery_datasheet.txt
python app.py data/solar_panel_spec.txt
```

The key insight: good architecture makes reuse trivial, whether through file changes or command-line parameters.

---

## Learning Goals

By the end of this lab, you'll understand:

1. **Application Architecture** — How to organize code into reusable modules
2. **Separation of Concerns** — Each module has a single responsibility
3. **Configuration Management** — Using `.env` for secrets and settings
4. **Reusability** — The same application can work with different data sources
5. **Scalability** — How to add new features (PDF parsing, validation, structured output) later

## Key Insight

The Mistral integration is just one module. The real application design challenge is organizing your code so you can:
- Change prompts without changing application logic
- Add new data sources (PDFs, APIs, databases) without rewriting the core
- Test each module independently
- Scale to multiple products and workflows

This is why we separated concerns into `mistral_service.py`, `prompts.py`, and `app.py`.

## Bonus Challenges

**Challenge 1**: Add error handling
- What if the product file doesn't exist?
- What if the Mistral API times out?
- How should the application fail gracefully?

**Challenge 2**: Make the product filename configurable
- Instead of hardcoding `"data/battery_datasheet.txt"`, read it from `.env` or command-line arguments

**Challenge 3**: Add logging
- Print which product is being analyzed
- Log the model's response with a timestamp
- Help troubleshoot production issues

**Challenge 4**: Validate the output
- Implement a `validate_extraction()` function
- Check that required fields are present
- Count how many specifications were extracted

## Discussion Points

At the end of the lab, think about:

1. **Why separate concerns?** Could we have put everything in one file?
2. **What would change** if we wanted to support PDF uploads instead of text files?
3. **How would we add** structured JSON output instead of plain text?
4. **What's missing** from this architecture for production use?

The answer to that last question leads naturally to topics like:
- API layer (FastAPI, Flask)
- Data validation (Pydantic)
- Structured outputs (JSON schemas)
- Scaling (multiple workers, queues)
- Monitoring (logging, observability)

But those are future labs!

## Troubleshooting

**"ModuleNotFoundError: No module named 'mistralai'"**
- Run `pip install -r requirements.txt`

**"MISTRAL_API_KEY not found"**
- Make sure you set `export MISTRAL_API_KEY="..."` before running
- Or add it to your `.env` file and load it at the top of `app.py`

**"FileNotFoundError: data/battery_datasheet.txt"**
- Make sure you're running from the `03_application/` directory
- Or check that the file path is correct

**API Errors**
- Check your API key is valid (get one at https://console.mistral.ai)
- Verify your account has API credits
- Review the error message—Mistral errors are usually descriptive

## Getting Help

1. Check the Mistral docs: https://docs.mistral.ai
2. Review your Lab 2 work for prompt patterns
3. Ask your instructor

---

**Ready?** Start with `mistral_service.py`. Good luck! 🚀
