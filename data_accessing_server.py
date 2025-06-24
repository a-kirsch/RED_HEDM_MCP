import os
import re
from mcp.server.fastmcp import FastMCP

print("Starting data_accessing_server...")
mcp = FastMCP("data accessing")
print("MCP server initialized.")

raw_data_dir = "/home/shared_data/raw"

def extract_id(filename: str) -> int | None:
    match = re.search(r'(\d{6})', filename)
    return int(match.group(1)) if match else None

def categorize_files(files: list[str]) -> tuple[list[str], list[str]]:
    dark_files = [f for f in files if f.startswith("dark")]
    park_files = [f for f in files if f.startswith("park_ss_ff")]
    return dark_files, park_files

@mcp.tool()
def list_files() -> list[str]:
    """
    List all files in the raw data directory.
    Returns:
        list[str]: Filenames found in the directory.
    """
    if not os.path.exists(raw_data_dir):
        return ["Error: Directory does not exist."]
    return sorted(os.listdir(raw_data_dir))

@mcp.tool()
def find_pairings(selected_file: str) -> dict:
    """
  File "/home/akirsch/.local/lib/python3.10/site-packages/mcp/server/fastmcp/server.py", line 217, in runnary containing the selected file, matching files, and their count.
    """
    try:
        all_files = os.listdir(raw_data_dir)
    except Exception as e:
        return {"error": f"Could not read directory: {str(e)}"}

    selected_id = extract_id(selected_file)
    if selected_id is None:
        return {"error": "Could not extract numeric ID from filename"}

    dark_files, park_files = categorize_files(all_files)

    if selected_file.startswith("dark"):
        matches = [f for f in park_files if abs(extract_id(f) - selected_id) <= 10]
    elif selected_file.startswith("park_ss_ff"):
        matches = [f for f in dark_files if abs(extract_id(f) - selected_id) <= 10]
    else:
        return {"error": "Filename must start with 'dark' or 'park_ss_ff'"}

    return {
        "selected_file": selected_file,
        "matching_files": matches,
        "count": len(matches),
    }


# @mcp.tool()
# def validate_pair_compatibility(training_scan_file: str, training_dark_file: str) -> dict:
#     """
#     Validates that the input contains one park_ss_ff file and one dark file, and that
#     the 6-digit numeric IDs differ by no more than 10.
#     Args:
#         training_scan_file (str): Path to the training scan file.
#         training_dark_file (str): Path to the training dark file.
#     Returns:
#         dict: A dictionary indicating compatibility, the files involved, their IDs, and the difference.
#     """
#     try:
#         # Use categorize_files to identify file types
#         darks, parks = categorize_files([training_scan_file, training_dark_file])

#         if len(darks):
#             File "/home/akirsch/.local/lib/python3.10/site-packages/mcp/server/fastmcp/server.py", line 217, in run != 1 or len(parks) != 1:
#             return {
#                 "compatible": False,
#                 "reason": "Inputs must include exactly one dark file (starting with 'dark') and one park file (starting with 'park_ss_ff')."
#             }

#         dark_file = darks[0]
#         park_file = parks[0]

#         dark_id = extract_id(dark_file)
#         park_id = extract_id(park_file)

#         if dark_id is None or park_id is None:
#             return {
#                 "compatible": False,
#                 "reason": "Could not extract 6-digit numeric ID from one or both filenames."
#             }

#         diff = abs(park_id - dark_id)
#         compatible = diff <= 10

#         return {
#             "compatible": compatible,
#             "dark_file": dark_file,
#             "park_file": park_file,
#             "dark_id": dark_id,
#             "park_id": park_id,
#             "difference": diff,
#             "reason": "Compatible" if compatible else f"Difference is {diff}, which exceeds threshold of 10."
#         }

#     except Exception as e:
#         return {"compatible": False, "error": str(e)}


if __name__ == "__main__":
    mcp.run()
    # print(list_files())
