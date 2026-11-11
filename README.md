# Mistral AI Workshop

Hands-on Python labs for exploring Mistral's APIs, document processing and
knowledge retrieval. Follow the instructions in each lab and complete the
challenges at your own pace.

## Workshop topics

### [Day 01 — Building with Mistral](labs/day01/)

- Making your first API request and inspecting the response
- Prompt engineering, few-shot examples and model behavior
- Building a modular Python application
- Structured outputs, Pydantic schemas and validation

### [Day 02 — Documents and knowledge](day02/)

- OCR, document annotations and document Q&A
- Managed knowledge retrieval with Mistral Libraries
- Embeddings, semantic search and retrieval evaluation
- Accessing external knowledge with connectors and MCP

## Getting started

You need Python 3.10 or later, internet access and a
[Mistral API key](https://console.mistral.ai/). Some labs also require
specific model access or workspace permissions; check the lab instructions
before starting. Hosted API requests and persistent resources may incur
charges.

From the repository root, create an environment and install dependencies:

```bash
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.
Set `MISTRAL_API_KEY` using your training center's approved method. Never
commit or share your key.

Start with the [first request instructions](labs/day01/01_first_request.md),
then follow each lab's instructions for its exercises, data and cleanup.
The labs use fictional materials where provided. Only send fictional or
otherwise approved content to hosted services.

## Resources

- [Mistral quickstart](https://docs.mistral.ai/inference/quickstarts/send-your-first-request)
- [Mistral documentation](https://docs.mistral.ai/)
- [Mistral Python SDK](https://github.com/mistralai/client-python)
