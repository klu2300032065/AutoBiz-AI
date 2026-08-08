import os
import shutil

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workspace', 'generated_projects'))

def _ensure_safe_path(path: str) -> str:
    """Ensure that the given path is within the designated workspace."""
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(WORKSPACE_DIR):
        raise PermissionError(f"Access denied: Cannot operate outside of {WORKSPACE_DIR}")
    return abs_path

def create_directory(dir_path: str):
    """Create a directory in the workspace."""
    safe_path = _ensure_safe_path(dir_path)
    os.makedirs(safe_path, exist_ok=True)
    return f"Created directory: {safe_path}"

def create_file(file_path: str, content: str):
    """Create a file in the workspace."""
    safe_path = _ensure_safe_path(file_path)
    os.makedirs(os.path.dirname(safe_path), exist_ok=True)
    with open(safe_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Created file: {safe_path}"

def read_file(file_path: str) -> str:
    """Read a file from the workspace."""
    safe_path = _ensure_safe_path(file_path)
    if not os.path.exists(safe_path):
        return "File not found."
    with open(safe_path, 'r', encoding='utf-8') as f:
        return f.read()

def update_file(file_path: str, content: str):
    """Update a file in the workspace."""
    safe_path = _ensure_safe_path(file_path)
    if not os.path.exists(safe_path):
        return "File not found."
    with open(safe_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Updated file: {safe_path}"

def delete_file(file_path: str):
    """Delete a file or directory from the workspace."""
    safe_path = _ensure_safe_path(file_path)
    if not os.path.exists(safe_path):
        return "Path not found."
    if os.path.isdir(safe_path):
        shutil.rmtree(safe_path)
    else:
        os.remove(safe_path)
    return f"Deleted: {safe_path}"

def list_directory(dir_path: str = WORKSPACE_DIR) -> str:
    """List contents of a directory in the workspace."""
    safe_path = _ensure_safe_path(dir_path)
    if not os.path.exists(safe_path):
        return "Directory not found."
    items = os.listdir(safe_path)
    return "\\n".join(items) if items else "Directory is empty."
