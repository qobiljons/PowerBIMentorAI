"""File discovery utilities for PowerBIMentor."""

from pathlib import Path
from typing import Optional


def get_file_by_type(directory: str, extension: str) -> Optional[str]:
    """Find the first file with the given extension in a directory.

    Args:
        directory: Path to the directory to search
        extension: File extension to search for (e.g., '.pbit', '.pdf')

    Returns:
        Filename if found, None otherwise

    Example:
        >>> get_file_by_type("submissions/student1", ".pbit")
        'assignment.pbit'
    """
    try:

        dir_path = Path(directory).resolve()


        if not dir_path.exists() or not dir_path.is_dir():
            return None


        extension_lower = extension.lower()
        for file in dir_path.iterdir():
            if file.is_file() and file.suffix.lower() == extension_lower:
                return file.name

        return None
    except (OSError, PermissionError):
        return None
