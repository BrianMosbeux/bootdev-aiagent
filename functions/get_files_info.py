import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(work_path, directory))
        valid_target_dir = os.path.commonpath([work_path, target_path]) == work_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        else:
            return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {e}"
