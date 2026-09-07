import os
import re
import shutil

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workspace', 'generated_projects'))

def sanitize_project_name(name: str) -> str:
    """Sanitize project name to snake_case and reject unsafe path components."""
    if not name or not isinstance(name, str):
        raise ValueError("Invalid project name: Name must be a non-empty string.")
        
    # Check for null bytes, UNC paths, drive letters, slashes, or path traversal elements
    if "\0" in name:
        raise ValueError("Invalid project name: Contains null bytes.")
    if name.startswith("\\\\") or name.startswith("//"):
        raise ValueError(f"Invalid project name '{name}': UNC paths are strictly forbidden.")
    if re.search(r'^[a-zA-Z]:', name):
        raise ValueError(f"Invalid project name '{name}': Drive-letter absolute paths are strictly forbidden.")
    if ".." in name or "/" in name or "\\" in name:
        raise ValueError(f"Invalid project name '{name}': Path traversal and slashes are strictly forbidden.")
        
    # Strip prefixes like 'Run QA on ', 'Build the product: ', etc.
    clean_name = re.sub(r'^(Run QA on |Build the product: |Product:\s*)', '', name, flags=re.IGNORECASE).strip()
    
    # Replace non-alphanumeric characters with underscores
    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', clean_name)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    
    if not clean_name:
        clean_name = "generated_project"
        
    return clean_name.lower()

def get_project_path(project_name: str) -> str:
    """Return safe absolute path for a project inside WORKSPACE_DIR."""
    sanitized = sanitize_project_name(project_name)
    target_path = os.path.join(WORKSPACE_DIR, sanitized)
    return _ensure_safe_path(target_path)

def _ensure_safe_path(path: str) -> str:
    """Ensure that the given path is within the designated workspace."""
    abs_path = os.path.abspath(path)
    if not os.path.normcase(abs_path).startswith(os.path.normcase(WORKSPACE_DIR)):
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
    return "\n".join(items) if items else "Directory is empty."

