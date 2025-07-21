import os
import re
from mcp.server.fastmcp import FastMCP

print("Starting data_accessing_server...")
mcp = FastMCP("data accessing")
print("MCP server initialized.")

DEFAULT_RAW_DATA_DIR = os.environ.get("CLINE_WORKSPACE", "/home/beams/WZHENG/RareEventDetectionHEDM/example_dataset/raw")

def extract_id(filename: str) -> int | None:
    match = re.search(r'(\d{6})', filename)
    return int(match.group(1)) if match else None

def categorize_files(files: list[str]) -> tuple[list[str], list[str]]:
    dark_files = [f for f in files if f.startswith("dark")]
    park_files = [f for f in files if f.startswith("park_ss_ff")]
    return dark_files, park_files

@mcp.tool()
def list_files(base_dir: str = DEFAULT_RAW_DATA_DIR) -> list[str]:
    """
    List all .ge5 files in base_dir and its subdirectories.
    
    Args:
        base_dir (str): Directory to search (optional — defaults to DEFAULT_RAW_DATA_DIR)
    
    Returns:
        list[str]: Filenames found in the directory.
    """
    if not os.path.exists(base_dir):
        return [f"Error: Directory '{base_dir}' does not exist."]
    
    ge5_files = []

    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".ge5"):
                rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                ge5_files.append(rel_path)

    return sorted(ge5_files)


if __name__ == "__main__":
    mcp.run()
    # print(list_files())
