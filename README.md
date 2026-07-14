# path-content-json

A simple Python utility that reconstructs a project from a JSON array of files and directories.

This tool is designed for AI-assisted development workflows where an LLM generates an entire project as structured JSON. The utility reads the JSON from **stdin** and recreates the corresponding directory structure and files on disk.

## Features

- Creates directories and files from a JSON document
- Automatically creates parent directories as needed
- Uses UTF-8 encoding
- Writes files with Unix (LF) line endings
- Refuses to overwrite existing files by default
- Lists all conflicting files before making any changes
- Supports a `/f` option to force overwriting existing files
- Simple, dependency-free implementation using the Python standard library

## JSON Format

The input must be a JSON array.

Each element contains:

- `path` – Relative path to a file or directory
- `content` – File contents (omitted or `null` for directories)

Example:

```json
[
  {
    "path": "README.md",
    "content": "# My Project\n"
  },
  {
    "path": "src/",
    "content": null
  },
  {
    "path": "src/main.py",
    "content": "print('Hello, world!')\n"
  }
]
```

Directories are identified by a trailing `/`.

## Usage

### Basic

```bash
python unpack_project.py < project.json
```

### Force overwrite

```bash
python unpack_project.py /f < project.json
```

If existing files are found, the utility will stop before writing anything and display a list of conflicts.

Example:

```
ERROR: 4 existing files would be overwritten:

  README.md
  src/main.py
  src/utils.py
  requirements.txt

Nothing has been written.

Run again with /f to overwrite these files.
```

## Why this exists

Large Language Models frequently generate software projects as structured JSON because it is easier to validate and transport than archive formats. This utility provides a safe way to unpack those projects while protecting existing work from accidental overwrites.

## Requirements

- Python 3.7 or later
- No third-party dependencies

## License

MIT License
