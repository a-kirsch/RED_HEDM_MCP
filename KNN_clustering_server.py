import subprocess
import os
import re
import sys
from mcp.server.fastmcp import FastMCP

print("Starting KNN_clustering_server...")
mcp = FastMCP("KNN_clustering")
print("MCP server initialized.")


# Define the directory and script for baseline clustering
BASELINE_SCRIPT_DIR = "/home/akirsch/RareEventDetectionHEDM/RareEventDetectionHEDM/code/EventDetection_code"
BASELINE_SCRIPT = os.path.join(BASELINE_SCRIPT_DIR, "baseline_pre.py")
PYTHON_EXEC = "/home/akirsch/miniconda3/envs/event_detection/bin/python"
workspace_dir = os.environ.get("CLINE_WORKSPACE", "/home/shared_data/raw")


# # Helper functions
# def extract_id(filename: str) -> int | None:
#     match = re.search(r"(\d{6})", filename)
#     return int(match.group(1)) if match else None

# def categorize_files(files: list[str]) -> tuple[list[str], list[str]]:
#     dark_files = [f for f in files if f.startswith("dark")]
#     park_files = [f for f in files if f.startswith("park_ss_ff")]
#     return dark_files, park_files

# def validate_pair_compatibility(scan_file: str, dark_file: str) -> tuple[bool, str]:
#     dark_files, park_files = categorize_files([scan_file, dark_file])
#     if len(dark_files) != 1 or len(park_files) != 1:
#         return False, "Input must include exactly one dark file and one park_ss_ff file."

#     scan_id = extract_id(scan_file)
#     dark_id = extract_id(dark_file)

#     if scan_id is None or dark_id is None:
#         return False, "Could not extract numerical ID from one or both filenames."

#     if abs(scan_id - dark_id) > 10:
#         return False, f"Scan and dark file IDs are too far apart (difference is {abs(scan_id - dark_id)})."

#     return True, "Files are compatible."

@mcp.tool()
def run_baseline_clustering(file_mode: int, baseline_scan: str, baseline_scan_dark: str, thold: int) -> str:
    """
    Run the baseline_pre.py script to perform KNN baseline clustering.
    Validates input files before execution.
    """
    # is_valid, message = validate_pair_compatibility(baseline_scan, baseline_scan_dark)
    # if not is_valid:
    #     return f"[ERROR] Validation failed: {message}"
    print("Running baseline clustering with parameters:")
    print(f"File mode: {file_mode}, Baseline scan: {baseline_scan}, Dark scan: {baseline_scan_dark}, Threshold: {thold}")
    try:
        cmd = [
            # sys.executable, BASELINE_SCRIPT,
            PYTHON_EXEC, BASELINE_SCRIPT,
            "-file_mode", str(file_mode),
            "-baseline_scan", "/home/shared_data/raw/"+baseline_scan,
            "-baseline_scan_dark", "/home/shared_data/raw/"+baseline_scan_dark,
            "-thold", str(thold)
        ]

        # Lock environment to conda env explicitly
        env = os.environ.copy()
        env["PATH"] = "/home/akirsch/miniconda3/envs/event_detection/bin:" + env["PATH"]
        env["CONDA_DEFAULT_ENV"] = "event_detection"
        env["PYTHONNOUSERSITE"] = "1"


        result = subprocess.run(
            cmd,
            capture_output=True,
            cwd=BASELINE_SCRIPT_DIR,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return f"[SUCCESS] Script completed successfully:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"[ERROR] Script failed:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"


if __name__ == "__main__":
    mcp.run()        
    # print("Starting KNN")
    # print(run_baseline_clustering(
    #     file_mode = 1,baseline_scan = "park_ss_ff_0MPa_000315.edf.ge5",
    #     baseline_scan_dark = "dark_before_000320.edf.ge5",
    #     thold = 100
    #     ))