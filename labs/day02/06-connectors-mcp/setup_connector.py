"""Register, connect and discover a public documentation MCP server."""

import asyncio
from uuid import uuid4

from common import CONNECTOR_ID_FILE, get_client

SERVER = "https://mcp.deepwiki.com/mcp"


async def register_connector(client, name: str) -> str:
    # TODO 1 (Required): Call client.beta.connectors.create_async with a
    # private MCP connector request using name, SERVER and a description.
    # Return the ID from the response. Print the ID before returning it.
    raise NotImplementedError("Complete TODO 1: register a connector")


async def connect_and_discover(client, connector_id: str) -> None:
    # TODO 2 (Required): Create default user-scoped credentials with empty
    # headers, then list tools using connector_id_or_name=connector_id.
    # Print each tool's name, description and input schema.
    raise NotImplementedError("Complete TODO 2: connect and list tools")


async def main() -> None:
    if CONNECTOR_ID_FILE.exists():
        raise FileExistsError("connector_id.txt exists; reuse or clean up that connector first.")
    client = get_client()
    connector_id = await register_connector(client, f"workshop_deepwiki_{uuid4().hex[:12]}")
    with CONNECTOR_ID_FILE.open("x", encoding="utf-8") as file:
        file.write(connector_id + "\n")
    print(f"Saved connector ID in {CONNECTOR_ID_FILE}", flush=True)
    await connect_and_discover(client, connector_id)


if __name__ == "__main__":
    asyncio.run(main())
