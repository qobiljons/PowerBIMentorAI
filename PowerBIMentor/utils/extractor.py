"""ZIP extraction utilities for PowerBIMentor."""

import zipfile
import tempfile
from pathlib import Path


def extract_zip_to_temp(zip_path: str) -> str:
    """Extract a ZIP file to a temporary directory.

    Args:
        zip_path: Path to the ZIP file

    Returns:
        Path to the temporary directory containing extracted files

    Raises:
        ValueError: If the path doesn't exist or is not a valid ZIP file

    Example:
        >>> temp_dir = extract_zip_to_temp("submission.zip")
        >>> # Process files in temp_dir
        >>> # Temp directory will be cleaned up automatically
    """

    zip_path_obj = Path(zip_path).resolve()


    if not zip_path_obj.exists():
        raise FileNotFoundError(
            f"ZIP file not found: {zip_path}\n"
            f"Resolved to: {zip_path_obj}\n"
            f"Current working directory: {Path.cwd()}"
        )


    if not zip_path_obj.is_file():
        raise ValueError(
            f"Path is not a file: {zip_path}\n"
            f"Expected a ZIP file, but got a directory or other type."
        )


    if not zipfile.is_zipfile(zip_path_obj):
        raise ValueError(
            f"Invalid ZIP file: {zip_path}\n"
            f"The file exists but is not a valid ZIP archive.\n"
            f"File size: {zip_path_obj.stat().st_size} bytes"
        )


    temp_dir = tempfile.mkdtemp(prefix="powerbi_submission_")


    try:
        with zipfile.ZipFile(zip_path_obj, "r") as z:
            z.extractall(temp_dir)
    except zipfile.BadZipFile as e:

        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise ValueError(
            f"Corrupted ZIP file: {zip_path}\n"
            f"Error: {e}"
        )

    return temp_dir
