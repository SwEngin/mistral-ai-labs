"""Delete only the explicitly confirmed practice library."""

from common import LIBRARY_ID_FILE, get_client, get_library_id


def main() -> None:
    library_id = get_library_id()
    print(f"This will permanently delete library {library_id} and its documents.")
    confirmed = input("Type the full library ID to confirm deletion: ").strip()
    if confirmed != library_id:
        print("Confirmation did not match; no deletion was requested.")
        return
    get_client().beta.libraries.delete(library_id=library_id)
    if LIBRARY_ID_FILE.read_text(encoding="utf-8").strip() == library_id:
        LIBRARY_ID_FILE.unlink()
    else:
        print("Local library ID changed during deletion; the file was not removed.")
    print(f"Deleted library {library_id}.")


if __name__ == "__main__":
    main()
