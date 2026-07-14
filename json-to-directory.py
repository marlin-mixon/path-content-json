import sys
import os
import json


def unpack_project():
    try:
        # Check for force option
        force = any(arg.lower() == "/f" for arg in sys.argv[1:])

        # Load all JSON data from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            print("Error: No data received via stdin.", file=sys.stderr)
            sys.exit(1)

        files_to_create = json.loads(input_data)

        if not isinstance(files_to_create, list):
            print("Error: Expected a JSON array at root.", file=sys.stderr)
            sys.exit(1)

        # ---------------------------------------------------------
        # First pass: Check for existing files
        # ---------------------------------------------------------
        conflicts = []

        for item in files_to_create:
            path = item.get("path")

            if not path:
                continue

            normalized_path = path.replace("\\", "/")

            # Only files are considered conflicts.
            # Existing directories are harmless because we use
            # os.makedirs(..., exist_ok=True).
            if not normalized_path.endswith("/") and os.path.exists(normalized_path):
                conflicts.append(normalized_path)

        if conflicts and not force:
            print(
                "\nERROR: The following files already exist:\n",
                file=sys.stderr,
            )

            for conflict in conflicts:
                print(f"  {conflict}", file=sys.stderr)

            print(
                "\nNothing has been written.",
                file=sys.stderr,
            )

            print(
                "\nRun again with /f to overwrite existing files.",
                file=sys.stderr,
            )

            sys.exit(1)

        # ---------------------------------------------------------
        # Second pass: Create directories and files
        # ---------------------------------------------------------
        for item in files_to_create:
            path = item.get("path")
            content = item.get("content")

            if not path:
                continue

            if path.endswith("/"):
                create_directory(path)
            else:
                write_file(path, content if content is not None else "")

        print("\nSuccessfully unpacked all project files!")

    except json.JSONDecodeError as je:
        print(
            f"JSON Parsing Error: Ensure input is valid JSON. Details: {je}",
            file=sys.stderr,
        )
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def create_directory(relative_path):
    """Create a directory from a path ending in '/'."""
    normalized_path = relative_path.replace("\\", "/").rstrip("/")

    if normalized_path:
        os.makedirs(normalized_path, exist_ok=True)
        print(f"Created directory: {normalized_path}/")


def write_file(relative_path, contents):
    """Create a file, creating parent directories if necessary."""

    normalized_path = relative_path.replace("\\", "/")

    directory = os.path.dirname(normalized_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    if contents is None:
        contents = ""

    # Force LF line endings
    with open(normalized_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(contents)

    print(f"Created file: {normalized_path}")


if __name__ == "__main__":
    unpack_project()
