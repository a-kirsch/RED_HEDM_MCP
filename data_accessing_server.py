import os
import re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("data accessing")

DEFAULT_RAW_DATA_DIR = os.environ.get("CLINE_WORKSPACE", "/home/beams/WZHENG/RareEventDetectionHEDM/example_dataset/raw")

# Function to extract the ID from a filename
def extract_id(filename: str) -> int | None:
    match = re.search(r'(\d{6})', filename)
    return int(match.group(1)) if match else None

# Function to categorize files into dark and park files
def categorize_files(files: list[str]) -> tuple[list[str], list[str]]:
    dark_files = [f for f in files if f.startswith("dark")]
    park_files = [f for f in files if f.startswith("park_ss_ff")]
    return dark_files, park_files

#Extract the load, i.e. number immediately preceding 'MPa' in a filename.
def extract_mpa(filename: str) -> int | None:
    match = re.search(r'(\d+)MPa', filename)
    return int(match.group(1)) if match else None


@mcp.tool()
def list_files(base_dir: str = DEFAULT_RAW_DATA_DIR) -> list[str]:
    """
    List all .ge#, .h5, and .hd5 files in base_dir and its subdirectories.
    
    Args:
        base_dir (str): Directory to search (optional — defaults to DEFAULT_RAW_DATA_DIR)
    
    Returns:
        list[str]: Filenames found in the directory.
    """
    if not os.path.exists(base_dir):
        return [f"Error: Directory '{base_dir}' does not exist."]
    
    relevant_files = []

    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith((".ge1", ".ge2", ".ge3", ".ge4", ".ge5", ".h5", ".hd5")):
                rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                relevant_files.append(rel_path)

    return sorted(relevant_files)


@mcp.tool()
def match_dark_and_park_files(base_dir: str = DEFAULT_RAW_DATA_DIR) -> dict[str, str] | str:
    """
    Match park and dark .ge5 files by sorted ID.
    Returns a dictionary mapping each park file to the corresponding dark file.
    The files are matched by order after sorting by the 6-digit ID in filenames.
    """
    all_files = list_files(base_dir)
    if isinstance(all_files, str) or any(f.startswith("Error:") for f in all_files):
        return "Error retrieving file list."

    dark_files, park_files = categorize_files(all_files)

    # Extract IDs and filter out files without valid IDs
    dark_files_with_ids = [(f, extract_id(f)) for f in dark_files if extract_id(f) is not None]
    park_files_with_ids = [(f, extract_id(f)) for f in park_files if extract_id(f) is not None]

    # Sort by ID
    dark_files_sorted = sorted(dark_files_with_ids, key=lambda x: x[1])
    park_files_sorted = sorted(park_files_with_ids, key=lambda x: x[1])

    # Match lowest park to lowest dark by index
    matched = {
        park[0]: dark[0]
        for park, dark in zip(park_files_sorted, dark_files_sorted)
    }

    return matched


if __name__ == "__main__":
    mcp.run()
    # local version for testing
    # print(list_files())
