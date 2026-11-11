"""Delete only the explicitly confirmed practice connector."""

from common import CONNECTOR_ID_FILE, get_client, get_connector_id


def main() -> None:
    connector_id = get_connector_id()
    print(f"This will permanently delete connector {connector_id} and its connection.")
    if input("Type the full connector ID to confirm deletion: ").strip() != connector_id:
        print("Confirmation did not match; no deletion was requested.")
        return
    get_client().beta.connectors.delete(connector_id=connector_id)
    if CONNECTOR_ID_FILE.read_text(encoding="utf-8").strip() == connector_id:
        CONNECTOR_ID_FILE.unlink()
    else:
        print("Local connector ID changed during deletion; the file was not removed.")
    print(f"Deleted connector {connector_id}.")


if __name__ == "__main__":
    main()
