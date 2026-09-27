import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(work_path, directory))
        if os.path.commonpath([work_path, target_path]) != work_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        items_info = []

        dir_name = None
        if directory == ".":
            dir_name = "current"
        else: 
            dir_name = f"'{directory}'"
        items_info.append(f"Result for {dir_name} directory:")
        for item in os.listdir(target_path):
            item_path = os.path.join(target_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            items_info.append(f"  - {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(items_info)

    except Exception as e:
        return f"Error: {e}"

