# Lab 1: Send Your First Mistral API Request

## Objective

Send a simple request to the Mistral API using the Python SDK and handle the response.

## Background

The Mistral API makes it easy to interact with Large Language Models (LLMs). In this lab, you'll:
- Initialize the Mistral client with your API key
- Send a chat completion request
- Extract and display the response

## Instructions

### Setup

Before starting, make sure:
1. Your `MISTRAL_API_KEY` environment variable is set
2. You've installed the dependencies: `pip install -r ../../requirements.txt`

### Your Tasks

Complete the three TODOs in `01_first_request.py`:

1. **TODO 1: Send a chat completion request**
   - Use `client.chat.complete()` method
   - Model: `mistral-small-latest`
   - Messages: Send a user message asking "Explain what an LLM is in two sentences."
   - Hint: Check the [Mistral quickstart](https://docs.mistral.ai/inference/quickstarts/send-your-first-request) for the exact method signature

2. **TODO 2: Extract the assistant's message**
   - The response object contains the model's reply
   - Access the message content from the response

3. **TODO 3: Print the response**
   - Display the assistant's message to the console

### Running Your Code

```bash
python 01_first_request.py
```

You should see the LLM's explanation of what an LLM is.

---

## Challenge Levels

### ✅ Required (Complete These First)

Complete the three TODOs above. Your output should be a single paragraph explaining LLMs.

**Expected output format:**
```
An LLM (Large Language Model) is...
```

### 🔍 Exploration (Once Required is Done)

Now that you've got a basic request working, explore:

1. **Inspect the response object**
   - Print the entire `response` object (or use `print(response.__dict__)` or similar)
   - What fields does it contain besides the message?

2. **Check usage information**
   - The response includes token usage (input tokens, output tokens)
   - Print the number of input and output tokens used
   - Hint: Look for a `usage` field in the response

3. **Change the prompt**
   - Modify the user message to ask a different question
   - Run it again with a new prompt, e.g., "What are the top 3 capabilities of LLMs?"

### 🎯 Bonus (Challenge Yourself)

Add a system message to control the assistant's behavior:

1. **Add a system message** that instructs the assistant to respond like a pirate
   - The `messages` parameter accepts a list where each message has a `role` (e.g., "system", "user", "assistant")
   - System messages set the tone/style for the response
   - Example role: `"role": "system"` with content: `"You are a pirate. Respond in pirate speak."`

2. **Send the same question** ("Explain what an LLM is in two sentences.") with the pirate system message

3. **Compare outputs**
   - Run both versions (with and without the system message)
   - Notice how the system message affects the response style without changing the content request

**Expected output:**
```
Arr, an LLM be a scallywag of language models, trained on vast amounts of text...
```

---

## Hints & Troubleshooting

**"ModuleNotFoundError: No module named 'mistralai'"**
- Run: `pip install -r ../../requirements.txt`

**"KeyError: 'MISTRAL_API_KEY'"**
- Set your API key: `export MISTRAL_API_KEY="your-key-here"`
- Verify it's set (without displaying it): `python -c "import os; print('API key configured' if os.getenv('MISTRAL_API_KEY') else 'API key missing')"`

**"What's the exact syntax for `client.chat.complete()`?"**
- Check the [official Mistral quickstart](https://docs.mistral.ai/inference/quickstarts/send-your-first-request)
- The starter code has hints in the TODO comments

**API call fails with a timeout or error**
- Check your internet connection
- Verify your API key is valid
- Try again (API can be temporarily slow)

---

## Next Steps

Once you've completed this lab:
- If all challenges feel easy, move on to Lab 2
- If you struggled with Bonus, re-read the Mistral docs on message roles
- Help a classmate who's stuck!
