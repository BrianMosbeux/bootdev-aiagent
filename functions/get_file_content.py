import os
from functions.utils import target_inside_working_dir

MAX_CHARS = 10000

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Return the first {MAX_CHARS} characters of the specified file within the working directory. If the file is more then 10000 characters it will be truncated.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to return the first 10000 characters of, relative to the working directory (default is the working directory itself)",
                },
            },
        },
        "required": ["file_path"],
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        if not target_inside_working_dir(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(file_path) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    
    except Exception as e:
        return f"Error: {e}"

    



