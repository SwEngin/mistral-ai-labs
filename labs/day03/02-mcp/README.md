# Day 03, Lab 02: Build an MCP Inventory Service

**60 minutes · Hands-on exercise**

Expose fictional inventory functions as an independent MCP service. A Python
client discovers and invokes its tools over Streamable HTTP, without an LLM.
Then use the same service with a prepared Mistral agent. Neither client
imports the inventory functions.


## Setup and safety

Use Python **3.12–3.14** and the workshop's root requirements. Internet
access is needed for installation and agent calls.
The direct MCP exercises do **not** require a Mistral key.

From the repository root:

```bash
python -m pip install -r requirements.txt
cd labs/day03/02-mcp
python -c "from mcp import Client; from mistralai import agents; print('MCP and Agents SDK imports OK')"
```

The server is unauthenticated and must bind **only to 127.0.0.1**. Never
expose it to a network or use real inventory or credentials in tool data.
Server and clients run on the same machine. Stop the server with Ctrl+C
when finished.

## Required — start, discover and call without a model

Read `server.py`: `@mcp.tool()` exposes `get_inventory_item`, including a
schema derived from its type annotations. The provided
`check_stock_availability` stub is **not registered** initially.

In one terminal, from this lab directory:

```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

The endpoint is `http://127.0.0.1:8000/mcp`. In a second terminal, complete
TODOs 1–2 in `inspect_tools.py`: open `Client(MCP_URL)`, list tools and print
their names, descriptions and input schemas, then call `get_inventory_item`
with the CLI's item ID. Display structured output and inspect `is_error`.
The starter raises `NotImplementedError` until completed.

```bash
python inspect_tools.py
python inspect_tools.py --item SKU-999
```

For `SKU-204`, the business result has name `NVMe SSD 2TB` and quantity 5.
The unknown item returns a business error object. Compare the discovered
schema with the Python function signature. These are source facts; no model
is involved. If the port is occupied, stop and resolve the conflict rather
than connecting to an unknown service.

## Exploration — add a tool and discover it

Complete TODOs 3–5: implement and register `check_stock_availability(item_id,
requested_quantity)`, then extend the client to call it with `--quantity`.
Reject non-positive quantities as an MCP error (for example with
`mcp.server.mcpserver.exceptions.ToolError`); handle an unknown item as a
business error object. For known items return `item_id`,
`requested_quantity`, `available_quantity`, `can_fulfill`, and `shortfall`.
The service—not the model—must enforce the rule.

Restart the server after changing it. The same client should discover the
additional tool and its string/integer input schema without importing the
server. Check these cases:

| Item | Quantity | Expected |
| --- | ---: | --- |
| SKU-204 | 3 | Can fulfill, shortfall 0 |
| SKU-204 | 8 | Cannot fulfill, shortfall 3 |
| SKU-310 | 8 | Can fulfill, shortfall 0 |
| SKU-999 | 2 | Product not found |
| SKU-204 | -1 | MCP tool error |

```bash
python inspect_tools.py --item SKU-204 --quantity 8
python inspect_tools.py --item SKU-204 --quantity -1
```

Distinguish a returned business error from an MCP `is_error` response.
Inspect both `structured_content` and content blocks where appropriate.
With MCP SDK 2.3.0, these `dict`-annotated tools return JSON in a text
content block and `structured_content` is `None`; do not assume every tool
provides structured content.

## Bonus — connect and evaluate the agent

After implementing and registering the new tool, leave the same server
running. Set `MISTRAL_API_KEY` through the approved method or copy
`.env.example` to `.env` and add it locally. Set `MISTRAL_AGENT_MODEL` to an
accessible function-calling model if the default `mistral-large-4` is not
available. Never print or commit the key. Agent calls may incur charges.

```bash
python agent.py
```

The prepared Agents SDK example connects directly through `RemoteMCP`; no
Mistral Studio connector is created. Inspect its actual tool calls and final
answer. The model may not call a tool or may make mistakes; check the result
against server data. If the server is unavailable, the SDK may continue
without its tools and emit a notice—do not treat that as a successful lookup.

Compare: who selects the operation in the direct client versus the agent?
Where do the inventory rules run? How did the new tool become discoverable?
What authentication, authorization and network controls would be needed in
production? Review [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/),
its [client guide](https://py.sdk.modelcontextprotocol.io/client/), and
[Mistral Agents MCP](https://docs.mistral.ai/studio/agents/learn/agent/connectors).
