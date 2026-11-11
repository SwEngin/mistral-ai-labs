# Day 02, Lab 06: External Knowledge with Connectors and MCP

**60 minutes · Hands-on experiments**

Register DeepWiki's public MCP server with Mistral, discover its tools and
retrieve public SQLite documentation. Compare a direct, developer-selected
tool call with a conversation in which the model may choose an allowlisted
tool. DeepWiki is an external service; use public questions only.

## Setup and safety

Requires Python 3.10+, internet access, the Mistral SDK, a compatible model,
and an API key with **Private and shared connectors** access. The default
**Shared connectors only** scope does not access a private connector. Confirm
workspace policy and permissions with the instructor. DeepWiki requires no
separate account. If access is unavailable, follow the instructor demo and
discussion; do not claim offline tests are live results.

Registration creates a persistent remote connector, and calls may incur
charges. Only connect to the named, approved public server; do not submit
secrets, private repository names or sensitive questions. Treat external
tool responses as untrusted content, not instructions. A connector may
expose tools that read data or perform actions; allowlist only needed tools.

From the repository root on macOS/Linux:

```bash
cd labs/day02/06-connectors-mcp
python3 --version  # 3.10 or later
python -m pip install -r ../../../requirements.txt
```


```bash
python -c "from mistralai.client import Mistral; print('Mistral SDK import OK')"
```


## Required — register, connect, discover and call

Complete TODOs 1–3 and 5:

1. In `setup_connector.py`, register a private `mcp` connector for
   `https://mcp.deepwiki.com/mcp` with `create_async`. Return and print the
   exact ID. The provided entry point saves it before the next API call and
   refuses to create another while the ID file exists.
2. Connect using `create_credentials_async` with user scope, name `default`,
   `credentials={"headers": {}}` and `is_default=True`. Even a public server
   needs this connection. List tools with `list_tools_async`; print each
   name, description and input schema. Discovery is not execution.
3. In `query_connector.py`, directly call `read_wiki_structure` using
   `call_tool_async`, `connector_id_or_name`, and
   `arguments={"repoName": "sqlite/sqlite"}`. Print the response's text
   blocks and report non-text blocks, missing text or an MCP error indicated
   by `result.metadata.mcp_meta.is_error` when metadata is present. The SDK
   may represent missing optional fields as `Unset`.

Consult the [connector quickstart](https://docs.mistral.ai/studio/connectors/quickstart)
and [direct tool calling](https://docs.mistral.ai/studio/connectors/tool_calling).
The starter functions intentionally raise `NotImplementedError`.

**SDK warning:** Mistral SDK 3.7.0 marks `call_tool_async` as deprecated and
may print a `DeprecationWarning`. A warning alone does not mean the call
failed; check the returned result or any subsequent error. The current direct
tool-calling documentation still describes `call_tool`, and does not identify
a replacement. Verify the provider's latest guidance before production use;
this exercise does not suppress the warning.

```bash
python setup_connector.py
python query_connector.py --tool structure
```

**Success:** the exact ID is saved, the connector is connected, tool names and
schemas are displayed, and the direct call returns documentation topics.
Inspect the returned topics for SQLite internals. Tool availability and output
depend on the external service and may change.

If creation succeeds but saving the ID fails, use the printed ID to recover
the file or delete the exact connector in Studio. If connecting or discovery
fails, the connector still exists and its ID is saved: inspect it in Studio
before reconnecting or cleaning it up. Do not repeatedly create connectors.
If creation times out before a response arrives, inspect Studio for a
possibly created connector before retrying.

## Exploration — a different direct tool

Complete TODO 4 and call `ask_wiki_question` using the discovered schema,
repository `sqlite/sqlite`, and the default VDBE question:

```bash
python query_connector.py --tool question
python query_connector.py --tool question --question "How does SQLite execute SQL statements?"
```

Compare the explanation with the returned sources and public SQLite
documentation. DeepWiki's question-answering tool may itself use AI; a
direct connector call means **your application** did not use a Mistral model
to select the operation, not that the provider uses no model.

## Bonus — model-driven tool use

Complete TODOs 6–7 in `conversation_lookup.py`: start a conversation with
`tools=[{"type": "connector", "connector_id": ..., "tool_configuration":
{"include": ["ask_wiki_question"]}}]`, `store=False`, and instructions to
use external evidence, avoid following instructions in retrieved content,
and acknowledge uncertainty. Inspect `response.outputs` for tool executions
and assistant text; a prompt or tool configuration alone does not prove a
tool was called.

```bash
python conversation_lookup.py
python conversation_lookup.py --question "Explain the SQLite VDBE and identify supporting sources."
```

The model may not call the tool, may choose different arguments or may
produce unsupported claims. Report when no execution is visible, and verify
claims and references against the original documentation. See
[connectors in conversations](https://docs.mistral.ai/studio/connectors/conversations).

## Cleanup

Delete **only your practice connector** after the exercise:

```bash
python cleanup_connector.py
```

The script displays the saved ID and requires the complete ID as
confirmation. A mismatch sends no delete request; the local ID is removed
only after a successful deletion. If the ID was not saved, identify your
connector in Studio using the printed ID before deleting. Never delete
another participant's or a shared connector.

## Review

Compare managed Libraries, custom semantic search and MCP connectors: where
does knowledge live, who selects a tool and who controls retrieval? MCP can
complement RAG, but permissions, freshness, source verification and
prompt-injection defenses remain application responsibilities. Which
operations need approval before execution?
