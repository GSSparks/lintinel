import os

def is_file_in_changed_list(full_path, repo_path, changed_files):
    """
    Check if a file should be included based on the changed_files list.

    Args:
        full_path (str): Absolute or relative path to the file.
        repo_path (str): Base path of the repo.
        changed_files (set or list): Set of relative paths to check against.

    Returns:
        bool: True if file should be processed.
    """
    if not changed_files:
        return True

    rel_path = os.path.relpath(full_path, repo_path)
    return rel_path in changed_files
