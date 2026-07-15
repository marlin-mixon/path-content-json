import sys
import os
import json
import base64


def unpack_project():
    try:
        # Load all JSON data from stdin
        input_data = sys.stdin.read()

        if not input_data.strip():
            print("Error: No data received via stdin.", file=sys.stderr)
            sys.exit(1)

        files_to_create = json.loads(input_data)

        if not isinstance(files_to_create, list):
            print("Error: Expected a JSON array at root.", file=sys.stderr)
            sys.exit(1)

        for file_info in files_to_create:

            if not isinstance(file_info, dict):
                print("Warning: Skipping non-object entry.", file=sys.stderr)
                continue

            path = file_info.get("path")

            if not path:
                print("Warning: Skipping entry with no path.", file=sys.stderr)
                continue

            content = file_info.get("content")
            encoding = (encoding or "text").strip().lower()

            write_entry(path, content, encoding)

        print("\nSuccessfully unpacked all project files!")

    except json.JSONDecodeError as je:
        print(f"JSON Parsing Error: {je}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def write_entry(relative_path, contents, encoding=None):

    # Normalize path separators
    normalized_path = relative_path.replace("\\", "/")

    # Directory entry
    if contents is None:
        os.makedirs(normalized_path.rstrip("/"), exist_ok=True)
        print(f"Created directory: {normalized_path}")
        return

    directory = os.path.dirname(normalized_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    # Default to text if encoding omitted
    if encoding is None or encoding.lower() == "text":

        with open(
            normalized_path,
            "w",
            encoding="utf-8",
            newline="\n"
        ) as f:
            f.write(contents)

    elif encoding.lower() == "base64":

        try:
            binary = base64.b64decode(contents)
        except Exception as ex:
            raise ValueError(
                f"Invalid base64 content for '{normalized_path}': {ex}"
            )

        with open(normalized_path, "wb") as f:
            f.write(binary)

    else:
        raise ValueError(
            f"Unsupported encoding '{encoding}' for '{normalized_path}'"
        )

    print(f"Created: {normalized_path}")


if __name__ == "__main__":
    unpack_project()
