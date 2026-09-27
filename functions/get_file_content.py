import os
from functions.utils import target_inside_working_dir

MAX_CHARS = 10000

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

    



