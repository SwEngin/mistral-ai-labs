# Day 03, Lab 03: Durable Change-Request Workflow

**75 minutes · Hands-on exercise**

Build a code-defined workflow for fictional software changes. A Mistral model
assesses risk, but Python code decides the mandatory sequence and approval
policy. This exercise records decisions; it does **not** deploy changes,
request an approval, or wait for a person.


## Setup

Mistral Workflows is a hosted service; access, a Mistral API key, an available
chat model and internet are required. Requests and workflow executions may
incur charges. Use only the fictional inputs below. You need the Mistral CLI,
Bun, and Python 3.12 or later. Follow the
[CLI setup](https://docs.mistral.ai/studio/mistral-cli/quickstart) and sign
in with `mistral login`. Your instructor may supply a prepared scaffold.

Otherwise, in a separate working directory (not inside this workshop):

```bash
mistral workflows init change-workflow
cd change-workflow
```

In the generated `.env`, configure `MISTRAL_API_KEY` and `MISTRAL_MODEL`
with your approved credentials and a chat model available to your workspace.
Never commit or share the key. The generated project ignores `.env`; verify
that before using Git.

Copy this lab's `change_request.py` to
`apps/worker/src/worker/workflows/change_request.py` in the generated project.
Add `.lab_state/` to the **generated project's** `.gitignore` before running
the lab. Work on the copied file; the worker discovers workflow modules in
that package. If you also use the instructor solution, use it **instead of**
the starter, not alongside it: both register the same workflow and activities.

## First 10 minutes — predict the flow

Read `change_request.py`. Identify the input schema, the three activities,
and the workflow entry point. Which operations call an external service or
write a file? Which result is needed before applying the approval rule?
Predict which steps must run for production and for a high-risk staging
change. Compare this with the model-directed tool selection in Lab 01.

## Required — implement and execute

Complete TODOs 1–3 in the copied module:

1. Validate with `ChangeRequest.model_validate`. Reject blank IDs and
   services and descriptions shorter than 15 characters after trimming.
   The schema rejects invalid environments.
2. Await validation and the provided risk assessment, then apply this rule
   in workflow code: **production OR high risk requires manual approval**.
   Otherwise, mark the request `eligible_for_automatic_processing`.
3. Record **both** decisions. Return `request_id`, `risk_assessment`,
   `status` and `record_id`. Pass `simulate_failure` to the recording
   activity. Do not actually approve or execute a change.

The assessment activity is supplied. It calls Mistral through the
workflow-aware client, requests JSON and validates the result with
`RiskAssessment`. Schema validation checks the shape, not whether the model's
risk judgment is correct. The starter raises `NotImplementedError` until
your implementation is complete.

From the generated project root, start the worker:

```bash
mistral dev
```

Keep it running. In Mistral Console, open **Workflows**, select
`software-change-review`, start an execution and provide this input:

```json
{
  "request_id": "CHG-1042",
  "service": "payment-api",
  "environment": "production",
  "description": "Upgrade the payment API database schema",
  "simulate_failure": false
}
```

The result must require manual approval regardless of the model's risk.
Inspect the execution and returned record ID. Then use a **new request ID**
and a development environment for a low-impact description: the request is
eligible only if the model returns low or medium risk. The assessment can
vary; inspect it rather than assuming a category.

Try a missing or short description, a whitespace-only service and an invalid
environment. Invalid typed inputs may be rejected before the validation
activity starts. All must fail explicitly; no decision should be recorded.

## Exploration — failure and retry

Use another new ID and run:

```json
{
  "request_id": "CHG-1043",
  "service": "catalog-api",
  "environment": "staging",
  "description": "Update service configuration settings",
  "simulate_failure": true
}
```

The recording activity writes a decision, creates a marker and raises an
exception on the first attempt. The workflow service should retry it; the
next attempt writes the same decision to the same path and completes. Inspect
execution history and worker logs for the failed attempt, retry and result.
Find the one JSON record in `apps/worker/src/worker/workflows/.lab_state/`;
the `.retry` file is the demonstration marker, not a second decision.

Use a fresh ID for each new execution. Reusing an ID with a different
decision fails rather than overwriting it, and an existing marker suppresses
the simulated first failure. Never delete markers during an active execution.
For a fresh demonstration, use a new ID or, after the execution has stopped,
remove only the relevant record and marker. The returned record ID is the
SHA-256 filename stem.

This local-file fixture assumes **one local worker** and is not safe shared
storage or a production idempotency mechanism. In production, use a durable,
shared store with atomic idempotent writes and a deliberate conflict policy.
Even durable orchestration does not guarantee exactly-once side effects.

## Bonus — evaluate and extend

- Explain why production cannot be automatically eligible even if the model
  reports low risk. How would you test the high-risk staging branch without
  relying on the model returning high risk?
- If a worker stops after assessment completes, what should replay reuse?
  Compare that with a recording activity that failed after its side effect.
- Sketch how a signal and `workflow.wait_condition()` could support real
  approval, including rejection, timeout, authorization and audit. Do not
  confuse a recorded approval requirement with an actual approval.

Stop the worker with Ctrl+C. If the hosted service is unavailable, trace the
code and discuss the expected behavior; do not claim a live retry occurred.
See [workflow quickstart](https://docs.mistral.ai/studio/workflows/quickstarts/your-first-workflow)
and [activity retries](https://docs.mistral.ai/studio/workflows/building-workflows/activities/basics).
