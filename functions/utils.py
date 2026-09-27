import os


def target_inside_working_dir(working_directory: str, target_dir: str) -> bool:
    work_dir = os.path.abspath(working_directory)
    full_file_path = os.path.normpath(os.path.join(work_dir, target_dir))
    return os.path.commonpath([full_file_path, work_dir]) == work_dir
