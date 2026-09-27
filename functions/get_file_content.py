import os

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_dir = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([full_file_path, work_dir]) != work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_file_path) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    
    except Exception as e:
        return f"Error: {e}"

    



