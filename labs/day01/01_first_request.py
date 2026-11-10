import os
from mistralai.client import Mistral

# Step 1: Read the Mistral API key from the environment
api_key = os.environ["MISTRAL_API_KEY"]

# Step 2: Initialize the Mistral client
client = Mistral(api_key=api_key)

# TODO 1: Send a chat completion request
# Model: mistral-small-latest
# Ask: "Explain what an LLM is in two sentences."

# TODO 2: Extract the assistant's message

# TODO 3: Print the response
