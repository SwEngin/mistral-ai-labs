"""Local, fictional inventory MCP server."""

from mcp.server import MCPServer

mcp = MCPServer("Inventory Service")

INVENTORY = {
    "SKU-204": {"name": "NVMe SSD 2TB", "available_quantity": 5},
    "SKU-310": {"name": "DDR5 Memory 32GB", "available_quantity": 14},
}


@mcp.tool()
def get_inventory_item(item_id: str) -> dict:
    """Look up a product and its available stock by item ID."""
    item = INVENTORY.get(item_id)
    if item is None:
        return {"item_id": item_id, "error": "Product not found"}
    return {"item_id": item_id, **item}


def check_stock_availability(item_id: str, requested_quantity: int) -> dict:
    """Check whether the requested quantity of a product is available."""
    # TODO 3 (Exploration): Reject quantities <= 0 with a clear error.
    # Handle unknown products. For known products, return item_id,
    # requested_quantity, available_quantity, can_fulfill and shortfall.
    # TODO 4 (Exploration): Register this function as an MCP tool with
    # @mcp.tool(), then restart the server to expose it.
    raise NotImplementedError("Complete TODOs 3–4: implement and register the stock tool")


app = mcp.streamable_http_app()
