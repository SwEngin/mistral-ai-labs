"""Copy this module into the scaffolded worker's workflows package."""

import hashlib
import json
import os
from datetime import timedelta
from pathlib import Path
from typing import Literal

import mistralai.workflows as workflows
from mistralai.workflows import Depends
from mistralai.workflows.client import get_mistral_client
from pydantic import BaseModel, Field


class ChangeRequest(BaseModel):
    request_id: str
    service: str
    environment: Literal["development", "staging", "production"]
    description: str = Field(min_length=15)
    simulate_failure: bool = False


class RiskAssessment(BaseModel):
    risk: Literal["low", "medium", "high"]
    justification: str = Field(min_length=1)


STATE_DIR = Path(__file__).parent / ".lab_state"


@workflows.activity(start_to_close_timeout=timedelta(seconds=10), retry_policy_max_attempts=1)
async def validate_request(data: dict) -> dict:
    # TODO 1 (Required): Validate data with ChangeRequest.model_validate.
    # Reject whitespace-only request_id and service, and a description whose
    # trimmed content is shorter than 15 characters. Return model_dump().
    raise NotImplementedError("Implement request validation")


@workflows.activity(start_to_close_timeout=timedelta(seconds=75), retry_policy_max_attempts=2)
async def assess_risk(change: dict, client=Depends(get_mistral_client)) -> dict:
    response = await client.chat.complete_async(
        model=os.environ["MISTRAL_MODEL"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a software change risk assessor. Return a JSON object "
                    "with risk (low, medium or high) and justification (a short "
                    "explanation). Consider availability, security and operational "
                    "impact. Do not invent information."
                ),
            },
            {"role": "user", "content": f"Evaluate this change request:\n{json.dumps(change)}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    if not response.choices:
        raise ValueError("The model returned no choices")
    content = response.choices[0].message.content
    if not isinstance(content, str):
        raise ValueError("Expected JSON text from the model")
    return RiskAssessment.model_validate_json(content).model_dump()


@workflows.activity(
    start_to_close_timeout=timedelta(seconds=20),
    retry_policy_max_attempts=3,
    retry_policy_backoff_coefficient=2.0,
)
async def record_decision(request_id: str, decision: dict, simulate_failure: bool) -> str:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    record_id = hashlib.sha256(request_id.encode("utf-8")).hexdigest()
    record_path = STATE_DIR / f"{record_id}.json"
    marker_path = STATE_DIR / f"{record_id}.retry"
    content = json.dumps(decision, indent=2, sort_keys=True)
    if record_path.exists() and record_path.read_text(encoding="utf-8") != content:
        raise ValueError("Request ID already has a different decision; use a new ID")
    record_path.write_text(content, encoding="utf-8")
    if simulate_failure and not marker_path.exists():
        marker_path.write_text("first attempt failed", encoding="utf-8")
        raise RuntimeError("Simulated failure after recording the decision")
    return record_id


@workflows.workflow.define(
    name="software-change-review", workflow_display_name="Software Change Review"
)
class SoftwareChangeWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: ChangeRequest) -> dict:
        # TODO 2 (Required): Await validate_request(input.model_dump()), then
        # assess_risk(validated). Production OR high risk requires approval.
        # Otherwise the request is eligible for automatic processing.
        # TODO 3 (Required): Build a decision with request_id, risk_assessment,
        # and status; await record_decision for BOTH branches. Return the
        # decision and record_id. No change is deployed or approved here.
        raise NotImplementedError("Implement workflow orchestration")
