"""Create a practice library and save its ID."""

from common import LIBRARY_ID_FILE, get_client


def create_library(client) -> None:
    # TODO 1 (Required): Call client.beta.libraries.create() with a name and
    # description for the Northstar Cloud practice library.
    # Print the returned ID before saving it, so it remains visible if writing
    # the local ID file fails. Save it to LIBRARY_ID_FILE using UTF-8.
    raise NotImplementedError("Complete TODO 1 in create_library()")


def main() -> None:
    if LIBRARY_ID_FILE.exists():
        raise FileExistsError(
            "library_id.txt already exists. Reuse that library or clean it up "
            "before creating another one."
        )
    create_library(get_client())


if __name__ == "__main__":
    main()
