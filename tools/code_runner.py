import subprocess
import os
from tools.file_manager import WORKSPACE_DIR, _ensure_safe_path

def is_safe_command(command: str) -> bool:
    """Check if a shell command is safe to execute."""
    dangerous = ["rm -rf", "rmdir /s", "del /s", "format ", "diskpart", "wget ", "curl "]
    command_lower = command.lower()
    for d in dangerous:
        if d in command_lower:
            return False
    return True

def run_command(command: str, cwd: str) -> dict:
    """Run a shell command inside the generated project directory."""
    if not is_safe_command(command):
        return {
            "stdout": "",
            "stderr": f"Command blocked by security policy: {command}",
            "exit_code": -1
        }
    safe_cwd = _ensure_safe_path(cwd)
    try:
        # Use shell=True for windows cross-compatibility with npm etc.
        result = subprocess.run(command, cwd=safe_cwd, shell=True, capture_output=True, text=True, timeout=60)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Command timed out after 60 seconds.",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }

import sys

def run_python(script_name: str, cwd: str) -> dict:
    """Run a python script inside the generated project directory."""
    return run_command(f'"{sys.executable}" {script_name}', cwd)

def run_npm(npm_args: str, cwd: str) -> dict:
    """Run an npm command inside the generated project directory."""
    return run_command(f"npm {npm_args}", cwd)

def run_tests(test_command: str, cwd: str) -> dict:
    """Run tests inside the generated project directory."""
    return run_command(test_command, cwd)
