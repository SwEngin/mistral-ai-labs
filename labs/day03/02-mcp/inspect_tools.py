"""Discover and call inventory tools over MCP without a model."""

import argparse
import asyncio

from mcp import Client

MCP_URL = "http://127.0.0.1:8000/mcp"


async def inspect_and_call(item_id: str, quantity: int | None) -> None:
    # TODO 1 (Required): Open an async Client(MCP_URL) context. Call
    # list_tools(), then print each tool's name, description and input_schema
    # as readable JSON. Do not import server.py or its functions.
    #
    # TODO 2 (Required): Call get_inventory_item with {"item_id": item_id}
    # through client.call_tool(). Inspect structured_content, content and
    # is_error; report MCP errors rather than treating them as successful.
    #
    # TODO 5 (Exploration): When quantity is not None, call
    # check_stock_availability with item_id and requested_quantity. Report
    # the result and any MCP error.
    raise NotImplementedError("Complete TODOs 1–2 and 5 in the MCP client")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item", default="SKU-204")
    parser.add_argument("--quantity", type=int)
    args = parser.parse_args()
    asyncio.run(inspect_and_call(args.item, args.quantity))


if __name__ == "__main__":
    main()
