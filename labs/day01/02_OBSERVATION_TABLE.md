# Lab 2 — Observation Table (Participant Worksheet)

Record your findings as you complete each exercise. Use this to document what changed and what you observed.

## Exercise 1: Improve the Prompt

**What changed?** 
(List the rules you added to SYSTEM_PROMPT)

```
1. 
2. 
3. 
4. 
5. 
```

**What did you observe?** 
(Compare this output to the basic prompt from the starter code)

```
Notable differences:
- 
- 
- 
```

**Did accuracy improve?** (Yes / No / Partially)

Why or why not?

---

## Exercise 2: Add Few-Shot Example

**What changed?** 
(Describe the example you added)

```
I added an example showing:
- 
- 
- 
```

**What did you observe?**
(Compare format, consistency, completeness)

```
- Format: 
- Consistency: 
- Completeness: 
```

**Did accuracy improve?** (Yes / No / Partially)

Why or why not?

---

## Exercise 3: Temperature Comparison

### Part A: Temperature = 0.1 (Run 3 times)

**Run 1 output:**
```
(Paste key specs here)
```

**Run 2 output:**
```
(Paste key specs here)
```

**Run 3 output:**
```
(Paste key specs here)
```

**Observation**: How similar are these three runs?

```
- Identical: [ ]
- Very similar: [ ]
- Somewhat different: [ ]
- Quite different: [ ]
```

### Part B: Temperature = 0.7 (Run 3 times)

**Run 1 output:**
```
(Paste key specs here)
```

**Run 2 output:**
```
(Paste key specs here)
```

**Run 3 output:**
```
(Paste key specs here)
```

**Observation**: How different are these three runs?

```
- Identical: [ ]
- Very similar: [ ]
- Somewhat different: [ ]
- Quite different: [ ]
```

---

## Temperature Analysis

**Which temperature produced more consistent results?**

Temp 0.1 [ ]   Temp 0.7 [ ]

**Why would you use each temperature?**

Temp 0.1 is better for:
- 
- 
- 

Temp 0.7 is better for:
- 
- 
- 

---

## Final Questions

**1. Which exercise improved output the most?**

[ ] Exercise 1 (better rules)
[ ] Exercise 2 (few-shot example)
[ ] Both equally

Why?

---

**2. What specifications were reliably extracted?** (Mark all that were consistently in all outputs)

- [ ] Product name/model
- [ ] Capacity (mAh)
- [ ] Voltage (V)
- [ ] Weight (grams)
- [ ] Dimensions (mm)
- [ ] Operating temperature range (°C)
- [ ] Cycle life (cycles)
- [ ] Manufacturer
- [ ] Certifications
- [ ] Other: ________

---

**3. What specs were missing or inconsistent?**

```
- 
- 
- 
```

---

**4. Would you trust this system to extract specs in production?**

Yes [ ]   No [ ]   With validation [ ]

Why?

```


```

---

**5. What would you add to make this production-ready?**

Rank these from most important (1) to least important:

- [ ] Validation against ground truth
- [ ] Post-processing to standardize format
- [ ] Repeated runs to check consistency
- [ ] Human review for high-value fields
- [ ] Fallback rules for missing specs
- [ ] Error tracking and monitoring
- [ ] Better prompt engineering (more examples)

Additional ideas:

```
- 
- 
```

---

## Key Insight

**The Prompt Engineering Paradox:**

"Prompting improves behavior, but prompting alone is not a reliable data contract."

What this means: Even our best prompt (Exercise 2) can't guarantee perfect extraction. We still need:
- Validation
- Post-processing
- Monitoring
- Fallback logic

**In your own words, why is this important?**

```
(Your answer here)



```

---

## Share Your Observations

Bring this completed worksheet to the group discussion. Be ready to:
1. Show one interesting observation
2. Ask one question
3. Compare your results with 2-3 classmates
