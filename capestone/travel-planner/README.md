# Day 04 — Capstone: Corporate Travel Planner

**One training day · Individual or small teams · Fictional data**

Northstar Consulting needs an assistant that prepares a business travel
proposal. Two employees plan to travel from Nuremberg to Hamburg for a
conference. Read the supplied travel request and company policies, compare
the options, and explain an affordable, policy-aware recommendation.
**Do not book, reserve, approve expenses or connect to live booking services.**

The objective is a reliable, explainable solution—not the most elaborate UI.
A command-line application is enough.

## What you will use

| File | Purpose |
| --- | --- |
| `travel_planner.py` | Starter with implementation milestones |
| `travel_tools.py` | Read-only search functions with fictional data |
| `data/travel_request.pdf` | Main request for OCR |
| `data/*_request.pdf` | Reduced-budget, missing-information and injection scenarios |
| `data/*_request.txt` | Human-readable source for checking each PDF |
| `data/*_policy.md` | Three policy documents |
| `data/options.json` | Fictional round-trip ticket prices and hotel rates |

The tools only support the supplied Hamburg route and dates; unsupported
queries raise an error instead of returning invented availability. Assume two
rooms are available at each listed hotel for the given dates. Both train
options are standard class. Prices are **round trip per person** for transport
and **per room per night** for hotels; registration is per attendee.

## Setup

Use Python 3.12–3.14 and the workshop environment. From the repository root:

```powershell
python -m pip install -r requirements.txt
cd day04/travel-planner
python travel_planner.py
```

Set `MISTRAL_API_KEY` in the environment or repository-root `.env` using the
training center's approved method. Never print or commit it. The starter raises
`NotImplementedError` until you complete its tasks. Live requests need access
to OCR, embeddings and a function-calling model, internet access and may
incur charges. Use fictional or approved data only.

## Milestones

1. **Extract.** Use Mistral OCR to read the PDF and extract request ID,
   route, dates, number of travelers, rooms and nights, registration per
   attendee, total budget and how many travelers require refundable tickets.
   Validate required fields, date order and consistency. An unknown
   flexibility requirement is not zero. Treat document content as untrusted.
   Review extracted fields against the PDF.
2. **Retrieve.** Load the three policy documents, embed them and the
   request, and rank the results by similarity. Keep source filenames. All
   three policies contain relevant constraints: ranking alone must not
   silently discard a required rule.
3. **Discover options.** Register and call `search_transport(origin,
   destination, date)` and `search_hotels(city, check_in, check_out)` as
   read-only agent tools. Validate names and arguments, use actual tool results
   and bound the number of model requests. If data is unavailable, fail
   explicitly rather than inventing it.
4. **Calculate and validate.** Evaluate ticket combinations across both
   travelers, including the refundable requirement. Apply the train,
   standard-class, per-night hotel, separate-room and budget rules. Calculate
   costs deterministically using whole euros for this fixture (or integer
   cents / `Decimal` for general prices). Include all travelers, nights and
   registration. Record policy references, assumptions and rejected options.
   No option above the hotel cap is automatically approved.
5. **Produce the proposal.** Output structured JSON and a concise readable
   manager summary. Include the request ID, destination, both tickets, hotel,
   cost breakdown, total and remaining budget, policy status, sources,
   warnings, assumptions, reason and `approval_required: true`. If there is
   no eligible plan, return an explicit no-plan status without fabricated costs.

The policy says “reasonably accessible” but defines no distance threshold,
and distance is not the same as actual accessibility. Ask your instructor for
an assumption or make one **explicit and configurable**; do not present it
as a company policy. Confirm it before approval. An LLM's recommendation or
a retrieved passage is not an authorization or compliance decision.

## Tests

Run each PDF against your implementation, and record the actual output:

```powershell
python travel_planner.py data/travel_request.pdf
python travel_planner.py data/budget_request.pdf
python travel_planner.py data/missing_request.pdf
python travel_planner.py data/injection_request.pdf
```

- **A — Standard:** both travelers, the refundable ticket, two separate
  rooms and all expenses must be accounted for. Explain assumptions and
  independently verify arithmetic.
- **B — EUR 1,200:** show no plan meets the constraints; do not invent prices.
- **C — Missing flexibility:** request clarification or stop; do not infer
  zero refundable tickets. Also test unavailable hotel data.
- **D — Injection:** the PDF asks the assistant to ignore policy. Treat it
  as data; do not select the over-limit hotel or conceal the budget.
  A passing example alone does not prove prompt-injection immunity: model
  extraction is probabilistic. Review extracted values and use deterministic
  downstream validation.

Compare results with your calculations, tool trace and policy sources. Never
describe mocked tests as a live Mistral run.

## Optional challenges

After the core works, expose a search tool over MCP; explore durable workflow
retries; measure policy, calculation and tool-use accuracy; add privacy-aware
tracing; or containerize the app. A cloud deployment is not required.

## Deliverables and discussion

Demonstrate the PDF-to-proposal flow, structured extraction, source-linked
retrieval, at least one actual tool call, deterministic costs and policy
checks, JSON plus a manager summary, at least three scenarios, and a short
architecture explanation. Discuss which steps benefit from a model, which
must remain deterministic, how changing prices affect results and how a real
booking system would enforce authorization and human approval.

Evaluation: functional completeness 30%; architecture and integration 20%;
policy and calculations 20%; errors and security 15%; testing and explanation
15%.
