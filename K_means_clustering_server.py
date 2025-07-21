import subprocess
import os
import re
import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("K_means_clustering")


# Define the directory and script for baseline clustering
BASELINE_SCRIPT_DIR = "/home/beams/AKIRSCH/rareevent/RareEventDetectionHEDM/code/EventDetection_code"
BASELINE_SCRIPT = os.path.join(BASELINE_SCRIPT_DIR, "baseline_pre.py")
PYTHON_EXEC = os.environ.get("PYTHON_EXEC", sys.executable)
workspace_dir = os.environ.get("CLINE_WORKSPACE", "/home/beams/WZHENG/RareEventDetectionHEDM/example_dataset/raw/")

@mcp.tool()
def run_baseline_clustering(baseline_scan: str, baseline_scan_dark: str, file_mode: int = 1, thold: int = 100, baseline_dir: str = workspace_dir) -> str:
    """
    Run the baseline_pre.py script to perform K means baseline clustering.
    Validates input files before execution.
    """
    print("Running baseline clustering with parameters:")
    print(f"File mode: {file_mode}, Baseline scan: {baseline_scan}, Dark scan: {baseline_scan_dark}, Threshold: {thold}")
    try:
        cmd = [
            PYTHON_EXEC, BASELINE_SCRIPT,
            "-file_mode", str(file_mode),
            "-baseline_scan", os.path.join(baseline_dir, baseline_scan),
            "-baseline_scan_dark", os.path.join(baseline_dir, baseline_scan_dark),
            "-thold", str(thold)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            # cwd=BASELINE_SCRIPT_DIR,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            text=True,
        )
        stdout = result.stdout.strip() if result.stdout else ""
        stderr = result.stderr.strip() if result.stderr else ""

        return (
            f"Command: {' '.join(cmd)}\n"
            f"Return Code: {result.returncode}\n"
            f"--- STDOUT ---\n{stdout}\n"
            f"--- STDERR ---\n{stderr}"
        )
    except Exception as e:
        return f"Error occurred while running the script:\nCommand: {' '.join(cmd)}\nError: {str(e)}"


if __name__ == "__main__":
    mcp.run()        
    # print("Starting K_means clustering server...")
    # print(run_baseline_clustering(
    #     file_mode = 1,baseline_scan = "park_ss_ff_0MPa_000315.edf.ge5",
    #     baseline_scan_dark = "dark_before_000320.edf.ge5",
    #     thold = 100
    #     ))