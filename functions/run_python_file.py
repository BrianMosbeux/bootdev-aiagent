import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute the specified python file relative to the working directory with an optional list of arguments and return an output string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path of the python file to execute, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "description": "Optional list of arguments that will be passed to the python script",
                },
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:

        work_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(work_dir, file_path))
        if os.path.commonpath([work_dir, target_path]) != work_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_path]
        if args:
            command.extend(args)
        response = subprocess.run(command, cwd=work_dir, text=True, timeout=30, capture_output=True)
        stdout = response.stdout
        stderr = response.stderr
        output_string = ""
        if response.returncode != 0:
            output_string += f"Process exited with code {response.returncode}"
        if not stdout and not stderr:
            output_string += "No output produced"
        if stdout:
            output_string += f"STDOUT: {stdout}" 
        if stderr:
            output_string += f"STDERR: {stderr}"
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"




