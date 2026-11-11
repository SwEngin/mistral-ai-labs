"""Upload the fictional policies and wait for ingestion."""

import time
from pathlib import Path

from common import LAB_DIR, get_client, get_library_id

DOCUMENTS = ("support_policy.md", "release_policy.md", "backup_policy.md")
TIMEOUT_SECONDS = 300


def upload_and_wait(client, library_id: str, path: Path) -> None:
    # TODO 2 (Required): Open path in binary mode and upload it with
    # client.beta.libraries.documents.upload(). Keep the returned document ID.
    # TODO 3 (Required): Poll documents.status() for that ID. A "done" status
    # means searchable; "todo", "in_progress" and "waiting_for_capacity" are
    # pending. Raise an error for any other status. Use time.monotonic() to
    # stop after TIMEOUT_SECONDS and sleep briefly between checks.
    # Print the document ID immediately so a failed run can be investigated.
    raise NotImplementedError("Complete TODOs 2 and 3 in upload_and_wait()")


def main() -> None:
    library_id = get_library_id()
    client = get_client()
    for filename in DOCUMENTS:
        upload_and_wait(client, library_id, LAB_DIR / "data" / filename)
    print("All documents are ready.")


if __name__ == "__main__":
    main()
