# Day 03, Lab 03: Durable Change-Request Workflow

**75 minutes · Hands-on exercise**

Build a code-defined workflow for fictional software changes. A Mistral model
assesses risk, but Python code decides the mandatory sequence and approval
policy. This exercise records decisions; it does **not** deploy changes,
request an approval, or wait for a person.


## Setup — Windows and Docker

Your instructor prepares a Linux image and a generated project before class.
You need Docker Desktop running in **Linux container mode**, internet access,
access to Mistral's hosted Workflows and an API key in the assigned workspace.
Docker supplies the Linux tools; it does not supply service access. Model calls
and workflow executions may incur charges. Docker Desktop may itself use a
WSL 2 or Hyper-V backend, depending on the VM configuration; a working Linux
container backend must already be configured. Use only fictional data.

From the **repository root** in Windows PowerShell, check Docker and confirm
that your instructor's image is present:

```powershell
docker info --format '{{.OSType}}'
docker image inspect mistral-workshop-workflows:day03
Test-Path day03/03-workflows/workspace/change-workflow/apps/worker/src/worker/workflows/change_request.py
```

The first command must print `linux` and the last must print `True`. If a
check fails, ask the instructor for the prepared environment. The instructor
has already created
`day03/03-workflows/workspace/change-workflow/` for you; it holds your
individual generated project and is ignored by the workshop Git repository.
Do not share the project or any credentials it may contain.

Set `MISTRAL_API_KEY` in your PowerShell environment using the approved
training method. Use the key for the workspace assigned by the instructor.
Check that it is set without displaying it:

```powershell
if ([string]::IsNullOrWhiteSpace($env:MISTRAL_API_KEY)) { throw "Set MISTRAL_API_KEY first." }
```

Start your container from the repository root. Replace the deployment name
with the unique name assigned by your instructor, and use the model they
have verified in your workspace:

```powershell
docker run --rm -it `
  -e MISTRAL_API_KEY `
  -e MISTRAL_MODEL="mistral-small-2603" `
  -e DEPLOYMENT_NAME="workshop-student01" `
  --mount "type=bind,source=${PWD}/day03/03-workflows/workspace,target=/workspace" `
  -w /workspace/change-workflow `
  mistral-workshop-workflows:day03
```

Commands inside the container below use **Linux Bash**, not PowerShell. Your
project remains on the Windows bind mount after the container stops; the
container's own filesystem does not. No CLI login is required for this setup:
the CLI uses the key in its shell. Check the workspace identity shown when
`mistral dev` starts. The instructor must ensure the generated project's
`.env` has no conflicting key, model or deployment settings. Do not print,
commit or share credentials. Docker administrators can inspect container
environment variables, so use only a trusted training VM.

Each participant must also use a unique **workflow name** in the copied
`change_request.py` decorator, for example `software-change-review-alice`.
Use an instructor-assigned, non-sensitive suffix; leave the activity names
unchanged. In a shared workspace, identical workflow names in multiple active
deployments may lead to ambiguous routing or a `409` error. A unique
deployment name alone does not resolve that. Do not start multiple workers
for one participant's deployment: the local recording fixture needs a single
worker. The instructor will verify the names and routing before class.

Your editable file in VS Code is:

```text
day03/03-workflows/workspace/change-workflow/apps/worker/src/worker/workflows/change_request.py
```

The worker discovers workflow modules in that package. If the instructor
uses the solution, it replaces the starter file; the two must not be loaded
side by side.

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

In the container, from `/workspace/change-workflow`, start the worker:

```bash
mistral dev --no-open
```

Keep it running. In your Windows browser, open Mistral Console in the same
workspace, open **Workflows**, select **your unique workflow name**, start an
execution and provide this input:

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
Find the one JSON record in the generated project's
`apps/worker/src/worker/workflows/.lab_state/`;
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

Stop the worker with Ctrl+C. Restart it after editing the workflow, unless
you have verified that the development worker reloaded your changes. When
finished, run `exit` inside the container. The mounted
project and retry state remain on the VM; follow your instructor's
approved cleanup instructions. If the hosted service is unavailable, trace
the code and discuss the expected behavior; do not claim a live retry occurred.
See [workflow quickstart](https://docs.mistral.ai/studio/workflows/quickstarts/your-first-workflow)
and [activity retries](https://docs.mistral.ai/studio/workflows/building-workflows/activities/basics).
