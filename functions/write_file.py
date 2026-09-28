import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write the specified content to the specified file_path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path of the file to write to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "the new content to write to the provided file",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([work_dir, full_file_path]) != work_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_file_path):
            print(full_file_path)
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        with open(full_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
