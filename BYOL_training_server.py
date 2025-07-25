#imports: runs python script, path maniuplation, regex, mcp server
import subprocess
import os
import re
from mcp.server.fastmcp import FastMCP
import sys

# Ensure the MCP server is running
mcp = FastMCP("BYOL_training")


# Define the path to the main.py script and the Python executable
SCRIPT_PATH = "/home/beams/AKIRSCH/rareevent/RareEventDetectionHEDM/code/BraggEmb_code/main.py"
PYTHON_EXEC = os.environ.get("PYTHON_EXEC", sys.executable)
default_dir = os.environ.get("CLINE_WORKSPACE", "/home/beams/WZHENG/RareEventDetectionHEDM/example_dataset/raw/")



@mcp.tool()
def run_training_script(training_scan_file: str, training_dark_file: str, thold: int = 100, workspace_dir: str = default_dir) -> dict:
    """
    Runs main.py with user-provided scan file, dark file, and threshold.
    Args:
        training_scan_file (str): Path to the training scan file.
        training_dark_file (str): Path to the training dark file.
        thold (int): Threshold value for the training.
    Returns:
        dict: A dictionary containing the command executed, return code, stdout, and stderr.
    """
    
    try:
        # Build the command
        cmd = [
            PYTHON_EXEC, SCRIPT_PATH,
            "-training_scan_file", os.path.join(workspace_dir, training_scan_file),
            "-training_dark_file", os.path.join(workspace_dir, training_dark_file),
            "-thold", str(thold),
            "-gpus", "0",  # default to GPU 0, change if needed
            "-expName", "mcp_run",
            "-verbose", "1"
        ]


        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True, 
            cwd=os.path.dirname(SCRIPT_PATH), 
            timeout=60 * 30  # 30-minute timeout
        )

        stdout = result.stdout.strip() if result.stdout is not None else None
        stderr = result.stderr.strip() if result.stderr is not None else None

        return {
            "command": " ".join(cmd),
            "stdout": stdout,
            "stderr": stderr,
            "returncode": result.returncode
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
    # local version for testing
    # print(run_training_script(
    #     training_scan_file = "park_ss_ff_0MPa_000315.edf.ge5",
    #     training_dark_file = "dark_before_000320.edf.ge5",
    #     thold = 100
    #     ))
