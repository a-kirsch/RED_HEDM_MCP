import subprocess
import os
import re
import sys
from mcp.server.fastmcp import FastMCP

print("[DEBUG] Python executable:", sys.executable)
print("[DEBUG] sys.path:", sys.path)

mcp = FastMCP("KNN_clustering")


# Define the directory and script for baseline clustering
BASELINE_SCRIPT_DIR = "/home/akirsch/RareEventDetectionHEDM/RareEventDetectionHEDM/code/EventDetection_code"
BASELINE_SCRIPT = os.path.join(BASELINE_SCRIPT_DIR, "baseline_pre.py")
PYTHON_EXEC = "/home/akirsch/miniconda3/envs/event_detection/bin/python"
workspace_dir = os.environ.get("CLINE_WORKSPACE", "/home/shared_data/raw")

@mcp.tool()
def run_baseline_clustering(file_mode: int, baseline_scan: str, baseline_scan_dark: str, thold: int) -> str:
    """
    Run the baseline_pre.py script to perform KNN baseline clustering.
    Validates input files before execution.
    """
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
        )
        stdout = result.stdout.strip() if result.stdout else ""
        stderr = result.stderr.strip() if result.stderr else ""

        return {
            "command": " ".join(cmd),
            "stdout": stdout,
            "stderr": stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "command": " ".join(cmd),
            "error": str(e)
        }



    #     return f"[SUCCESS] Script completed successfully:\n{result.stdout}"
    # except subprocess.CalledProcessError as e:
    #     return f"[ERROR] Script failed:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"


if __name__ == "__main__":
    mcp.run()        
    # print("Starting KNN")
    # print(run_baseline_clustering(
    #     file_mode = 1,baseline_scan = "park_ss_ff_0MPa_000315.edf.ge5",
    #     baseline_scan_dark = "dark_before_000320.edf.ge5",
    #     thold = 100
    #     ))