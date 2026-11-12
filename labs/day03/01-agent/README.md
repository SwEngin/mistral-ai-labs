# Day 03, Lab 01: IT Incident Investigation Agent

**65 minutes · Hands-on exercise**

Build an agent that investigates fictional incidents using three read-only
Python tools. The model chooses tools and arguments; your application
executes the functions and returns their results. Your application uses Chat
Completions with a local orchestration loop; it does not create a persistent
hosted agent.


## Setup

Requires Python 3.10+, internet access, the project's dependencies, a Mistral
API key and access to a function-calling model. From the repository root:
The instructor solution and offline tests were checked with Mistral SDK 3.7.0.

```bash
python -m pip install -r requirements.txt
cd day03/01-agent
python -c "from mistralai.client import Mistral; print('SDK import OK')"
```

Set `MISTRAL_API_KEY` through the training center's approved method or in the
repository root's `.env`. Never print or commit it. The default model is
`mistral-small-latest`; `MISTRAL_MODEL` can select another compatible model.
Requests send your question and tool results to the model and may incur
charges. Use only fictional or approved data.

## First 10 minutes — predict the flow

Read `incident_tools.py` and the starter in `incident_agent.py`. For the
default question, write down:

1. Which tool should be called first, and with what argument?
2. Which value returned by that tool is needed by the other two tools?
3. What evidence would support a possible connection to a deployment? What
   would be needed to confirm it as the root cause?

The tools are local functions, not API calls. Their data is fictional. A
recent deployment is a possible lead, **not proof** that it caused the
incident. Consult [Mistral function calling](https://docs.mistral.ai/inference/conversations/function-calling)
and revisit the instructor's Day 3 demonstration.

## Required — implement and trace the investigation

Complete TODOs 1–4 in `incident_agent.py`:

1. Instruct the agent to investigate using evidence, acknowledge missing
   information and distinguish correlation from a confirmed cause.
2. Register function schemas for `get_incident_details(incident_id)`,
   `get_service_health(service_name)` and
   `get_recent_deployments(service_name)`. Each parameter is a required
   string. Include descriptions and `additionalProperties: false`.
3. Send system and user messages using `client.chat.complete()`, the schemas
   and `tool_choice="auto"`. Inspect the assistant's `tool_calls`.
4. Append the assistant message, execute the requested local functions,
   print names, arguments and results, and send **one** `role="tool"` message
   per call with its matching `tool_call_id` and JSON-serialized result.
   Repeat until a final text answer or the request limit. Fail explicitly
   on missing choices, call IDs or final text.

The starter raises `NotImplementedError` until implemented:

```bash
python incident_agent.py
```

**Success:** inspect the trace for incident details followed by health and
deployment data for `checkout-api`; the answer describes degraded health
and a deployment ten minutes before the incident without asserting that it
caused the incident. Model behavior varies: a prompt doesn't guarantee tool
selection or a correct answer. Verify both trace and answer against the tools.

## Exploration — failure and validation

Complete TODO 5: dispatch only allowlisted tool names; validate decoded JSON,
required keys and nonempty string arguments. Invalid tool calls should fail
explicitly. Return expected tool error objects as tool results so the model
can report missing information.

```bash
python incident_agent.py "Investigate INC-9999 and identify its affected service."
python incident_agent.py "Investigate INC-1043, including service health and recent deployments."
```

`INC-9999` is unknown. For `INC-1043`, health data is unavailable and the
deployment list is empty; **unavailable** is not the same as healthy, and
an empty list does not prove a cause. Check whether the model acknowledges
these limits. Do not retry by inventing tool results.

## Bonus — evaluate and explain

Use [the evaluation worksheet](evaluation.md) to compare the expected flow
with actual calls and record any unsupported claims. Test both a relevant
deployment and a missing-data case. What changes would be needed before
connecting the agent to real incident systems? Discuss authorization,
untrusted tool output, sensitive data and approval for actions.

If live API access is unavailable, inspect the supplied tool outputs and
discuss the predicted flow; do not describe that as a live model result.
