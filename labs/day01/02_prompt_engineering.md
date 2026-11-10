# Lab 2: Prompt Engineering and Model Behavior

## Objective

Learn how prompt design affects model accuracy, consistency, and data quality. Discover that while good prompts improve behavior, they alone cannot guarantee data contracts.

## Scenario: Product Evaluation Assistant

You're building a system to extract technical specifications from product descriptions. Your first attempt uses vague prompts, but you'll discover how to improve precision through better instruction design.

The test product is the **BX-3000 Battery**—a fictional lithium battery with clearly stated specifications. Your job is to extract these specs accurately using increasingly sophisticated prompts.

## Background

Many teams make the same mistake: they assume that once you craft a "good prompt," the model will reliably extract data the same way every time. This lab will challenge that assumption.

### Key Concepts

**Prompt Engineering**: The art of writing clear, structured instructions to guide LLM behavior.

**Few-Shot Prompting**: Providing examples of desired behavior to improve consistency.

**Temperature**: A parameter controlling randomness. Lower values (0.1) = more deterministic; higher values (0.7) = more creative.

**Data Reliability**: Good prompts improve behavior, but are not a substitute for validation, post-processing, or explicit data contracts.

## Instructions

### Setup

1. Make sure your `MISTRAL_API_KEY` is set: `python -c "import os; print('API key configured' if os.getenv('MISTRAL_API_KEY') else 'API key missing')"`
2. Open `02_prompt_engineering.py`
3. Read the product description and the three TODOs
4. Work through the exercises in order

### Running the Script

```bash
python 02_prompt_engineering.py
```

The script will print the model's extraction. After each modification, **record your observations** in the table at the end of this README.

---

## Exercises

### Exercise 1: Improve the Prompt (Required)

**Current state**: The basic prompt is too vague. The model might invent specifications, use inconsistent formats, or miss details.

**Your task**: 
Modify `SYSTEM_PROMPT` to include **explicit extraction rules**. Think about:
- How do you tell the model to extract ONLY stated facts (not assumptions)?
- How do you preserve units correctly?
- What should the model do when information is missing?
- How do you prevent invention of specifications?

**Guidelines** (not the solution):
- Start with "You are a product evaluation assistant" or similar
- List 3-5 specific rules the model should follow
- Be explicit about edge cases (missing data, unit handling)
- Specify the output format

**What to observe and record:**
- Does the output include all visible specifications?
- Are units preserved exactly as written?
- What happens when information is missing?
- Is the format consistent across multiple runs?

### Exercise 2: Add Few-Shot Prompting (Exploration)

**Current state**: Even with better instructions, the model might format results differently each time.

**Your task**: 
Add one or more **examples** to your `USER_PROMPT` showing the expected extraction format. Think about:
- What's a simple, realistic input example?
- What does the expected output look like?
- How do you present this to the model?

**Guidelines** (not the solution):
- Show an example input (short product description)
- Show the expected output in your desired format
- Include an example of "Not specified" for missing fields
- Explain to the model: "Follow this format for the real extraction"

**What to observe and record:**
- Does the model now follow the example format more consistently?
- Does few-shot prompting improve consistency compared to Exercise 1?
- Are there any formats the example didn't cover?

### Exercise 3: Experiment with Temperature (Bonus)

**Current state**: You've optimized the prompt, but how stable is the output?

**Your task**: 
Test the same prompt at two different temperatures to observe consistency:

1. **At low temperature** (0.1): Run the same extraction multiple times
2. **At high temperature** (0.7): Run the same extraction multiple times
3. **Compare**: How does variability differ?

**Guidelines**:
- Write a simple loop that runs the same extraction 3-5 times
- Save each output and compare them side-by-side
- Look for differences in formatting, wording, or content

**What to observe and record:**
- At low temperature: How much do outputs vary?
- At high temperature: How much do outputs vary?
- Which is better for reliable data extraction? Why?
- Are there any fields that change more than others?

---

## Observation Table

Record your findings as you progress through the exercises:

| Exercise | What Changed? | What Did You Observe? | Did Accuracy Improve? |
|----------|---------------|----------------------|-----------------------|
| Basic Prompt | No detailed instructions | _Your notes here_ | N/A |
| Exercise 1: Improved Instructions | Clear extraction rules + "Not specified" rule | _Your notes here_ | Yes/No |
| Exercise 2: Few-Shot Example | Example format added | _Your notes here_ | Yes/No |
| Exercise 3a: Temp 0.1 (multiple runs) | Temperature = 0.1 | _Your notes here_ | N/A |
| Exercise 3b: Temp 0.7 (multiple runs) | Temperature = 0.7 | _Your notes here_ | N/A |

### Questions to Consider

1. **Which exercise improved output the most?** Why?
2. **Did the "Not specified" rule work consistently?**
3. **Which specifications did the model reliably extract? Which ones were ambiguous?**
4. **Why is a low temperature (0.1) preferable for data extraction tasks?**
5. **Could you trust this system to extract specs from unknown products without additional validation?**

---

## Challenge Levels

### ✅ Required: Improve the Prompt

Complete Exercise 1. Your improved prompt should:
- Include at least 3 clear extraction rules
- Use "Not specified" for missing data
- Produce a readable, structured output
- Be applied consistently (test by running twice)

**Success criteria**: Output includes all explicit specs, uses consistent format, includes "Not specified" where needed.

### 🔍 Exploration: Few-Shot Prompting

Complete Exercise 2. Add a worked example to show the expected extraction format.

**Success criteria**: Output format matches your example; extractions are more consistent.

### 🎯 Bonus: Temperature Comparison

Complete Exercise 3. Test both temperatures and document the variations.

**Success criteria**: You've identified differences between temp 0.1 and 0.7; you can explain why 0.1 is better for this task.

### 🚀 Extra Challenge: Validation Layer

Once all exercises are complete, try this advanced approach:

1. Extract specs with your best prompt
2. Compare against a "ground truth" list:
   ```python
   GROUND_TRUTH = {
       "capacity": "5000 mAh",
       "voltage": "3.7V",
       "weight": "185g",
       "dimensions": "85 mm × 65 mm × 12 mm",
       "operating_temp": "0°C to 45°C",
       "cycle_life": "500-800 cycles",
       "manufacturer": "TechPower Industries",
       "certifications": "CE, FCC, RoHS, UL"
   }
   ```
3. Count how many specs were extracted correctly
4. List any hallucinations or missing data
5. **Conclusion**: Even with a great prompt, would you deploy this in production without a validation layer?

---

## Key Takeaway

**Prompting improves behavior, but prompting alone is not a reliable data contract.**

Good prompts and structured output formats work together to reduce errors. But for mission-critical data extraction (pricing, technical specs, warranty info), you need:
- **Validation**: Check outputs against ground truth
- **Post-processing**: Clean up formatting, standardize units
- **Fallback rules**: Define what to do when extraction fails
- **Monitoring**: Track extraction quality over time

This is why production systems use prompt engineering + structured output formats (like JSON schemas) + validation pipelines.

---

## Troubleshooting

**"The output looks random or completely wrong"**
- Check your `SYSTEM_PROMPT` and `USER_PROMPT` for typos
- Make sure you're using `{product}` placeholder correctly
- Try running Exercise 1 again from scratch

**"I'm getting the same output every time"**
- That's expected at temp 0.1! Lower temperatures reduce sampling variability.
- Try temp 0.7 in Exercise 3 to observe increased variation.

**"The model still makes up information"**
- Add a line to your system prompt: `"NEVER INVENT OR ASSUME SPECIFICATIONS NOT EXPLICITLY STATED."`
- Consider adding this to the example too

**"'Not specified' isn't showing up"**
- Try making the instruction more prominent: `"Use exactly the phrase 'Not specified' for missing information."`

---

## Next Steps

- Compare your results with classmates—did you get the same output?
- Discuss with your instructor what you learned about prompts
- Ready for the next challenge? Ask your instructor!
