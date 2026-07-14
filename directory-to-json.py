import os
import json
import sys

def scan_directory(target_dir, base_dir=None):
    result = []

    ignored_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}

    if base_dir is None:
        base_dir = os.getcwd()

    for root, dirs, files in os.walk(target_dir):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        # Record empty directories
        if not dirs and not files:
            dir_path = os.path.relpath(root, base_dir).replace(os.sep, "/") + "/"
            result.append({
                "path": dir_path,
                "content": None      # becomes JSON null
            })

        # Record files
        for file in files:
            full_path = os.path.join(root, file)

            path = os.path.relpath(full_path, base_dir).replace(os.sep, "/")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                result.append({
                    "path": path,
                    "content": content
                })

            except (UnicodeDecodeError, PermissionError):
                continue

    return result    

if __name__ == "__main__":
    # Use current directory if no path is passed as an argument
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    if not os.path.exists(project_dir):
        print(f"Error: The directory '{project_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Scan and convert to JSON string
    file_data = scan_directory(project_dir, os.getcwd())
    json_output = json.dumps(file_data, indent=2)
    
    # Print to stdout (can be redirected to a file)
    print(json_output)
