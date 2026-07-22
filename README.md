# path-content-json

A simple pair of Python utilities that 1. Encodes a project directory into a single JSON document.  2. Constructs or Reconstructs a project based on the JSON array describing the files and directories.

This tool makes it quick and easy to pass context to and from LLMs.  It is designed for AI-assisted development workflows where an LLM generates an entire project as structured JSON. The json-to-directory utility reads the JSON from **stdin** and recreates the corresponding directory structure and files on disk.  The directory-to-json reverses the process.  It creates a JSON file based on the contents of the starting directory and dives into the directory structure finding all files and stores them in a single JSON file.

## json-to-directory Features

- Creates directories and files from a JSON document
- Automatically creates parent directories as needed
- Uses UTF-8 encoding
- Writes files with Unix (LF) line endings
- Refuses to overwrite existing files by default
- Lists all conflicting files before making any changes
- Supports a `/f`, `-f`, or `--force` option to force overwriting existing files
- Simple, dependency-free implementation using the Python standard library

## directory-to-json Features

- Creates two types of JSON files based on a directory structure.
- Default format type 1 is JSON array of objects.  This is easiest for humans to read and easily handled by LLMs
- Option format type 2 is JSON array only.  This is still easy for LLMs to read but a bit harder for people.  Its advantage is it is minimal and conserves tokens.
- Both of these JSON formats are simple arrays and are only a single level deep.  Directory structure and depth is implied by the path elements.
- Supports a `/m`, `-m`, or `--minimize` option to create file that is minimally sized for best LLM token usage.
- writes to JSON to STDOUT.  Redirect as needed


## JSON Format

Example of JSON object format -- an array of JSON objects:

Each element contains:

- `path` – Relative path to a file or directory
- `content` – File contents (omitted or `null` for directories)
- `encoding` - Optional for identifying binary files.  Only valid entry is case-inensitive "base64".

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
  }.
  {
    "path": "assets/image.png",
    "encoding": "base64",
    "content": "iVBORw0KGgoAAAANSUhEUgAA..."
]
```

Example of minimized JSON array-only format:

```json
[
["README.md","# My Project\n"],
["src/",null],
["src/main.py","print('Hello, world!')\n"],
["assets/image.png", "base64", "iVBORw0KGgoAAAANSUhEUgAA..."]
]
```
Directories are identified by a trailing `/`.  Note that defining directories in this way is optional and only required for creating empty directories.

Use this to preface the minimized JSON array format to provide guidance for the LLM:
```
Project format:
["path","text"] = UTF-8 file
["path","base64","data"] = binary file
["dir/",null] = directory
Root is an array of entries.
```

## Usage

### Basic directory creation from a JSON using either JSON array of object format or JSON mimimzed array format

```bash
python json-to-directory.py < project.json
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
### As above but with force overwrite

```bash
python json-to-directory.py /f < project.json

(use switches /f, -f, --force as desired)
```

### Basic JSON creation from a directory structure

```bash
python directory-to-json.py > project.json
```

### Minimally-sized JSON format creation from a directory structure

```bash
python directory-to-json.py /m > MinProject.json

(use switches /m, -m, --minimize as desired)
```

## Why this exists

Large Language Models often require full directory context in order to assist you in updating existing projects.  However, it can be a pain to hunt down, cut and paste the several files needed for context. The directory-to-json.py helps you do that in one command.  Conversely, when creating new projects like web sites or docker-compose projects, Large Language Models will typically generate a lot of documents that are a pain to copy and paste each into the appropriate directory structure without taking time plus you risk making mistakes. By first requesting the LLM to put the generated files into JSON and then using the json-to-directory.py you can solve this problem with a single command. These utilities provides a safe and simple way to pack and unpack your projects with adequete protections that protect existing work from accidental overwrites. 

## Requirements

- Python 3.7 or later
- No third-party dependencies

## License

MIT License
