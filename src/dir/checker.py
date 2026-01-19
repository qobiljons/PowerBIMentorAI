from pathlib import Path

def get_file_by_type(directory: str, extension: str):
    for file in Path(directory).glob(f"*{extension}"):
        return file.name
    return None
