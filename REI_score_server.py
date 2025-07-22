#imports: runs python script, path manipulation, mcp server
import subprocess
import os
import sys
from mcp.server.fastmcp import FastMCP

#initialize the MCP server
mcp = FastMCP("REI_score")

# Define the directory and script for testing scan
SCRIPT_DIR = "/home/beams/AKIRSCH/rareevent/RareEventDetectionHEDM/code/EventDetection_code"
SCRIPT_PATH = "/home/beams/AKIRSCH/rareevent/RareEventDetectionHEDM/code/EventDetection_code/testing_scan.py"
PYTHON_EXEC = os.environ.get("PYTHON_EXEC", sys.executable)
workspace_dir = os.environ.get("CLINE_WORKSPACE", "/home/beams/WZHENG/RareEventDetectionHEDM/example_dataset/raw/")

@mcp.tool()
def run_testing_scan(
    testing_scan: str,
    testing_scan_dark: str,
    thold: int = 100,
    file_mode: int = 1,
    output_csv: str = "rei_score_260MPa.csv",
    trained_encoder: str = "../BraggEmb_code/model_save-itrOut/script-ep00100.pth",
    trained_centers: str = "kmeans_model.pkl",
    ncluster: int = 40,
    uqthr: float = 0.4,
    cluster: str = "Kmeans",
    degs: int = 360,
    seed: int = 0,
    degs_mode: int = 1,
    workspace_dir: str = workspace_dir
) -> str:
    """
    Run the testing scan step of the Rare Event Detection HEDM workflow.

    This executes testing_scan.py with the provided parameters to analyze a new scan 
    against the trained encoder and clustering model.
    Args:
        file_mode (int): Mode of the file (0 for .edf, 1 for .edf.ge5).
        testing_scan (str): Path to the testing scan file.
        testing_scan_dark (str): Path to the dark file for the testing scan.
        thold (int): Threshold value for the analysis.
        output_csv (str): Path to save the output CSV file.
        trained_encoder (str): Path to the trained encoder model.
        trained_centers (str): Path to the trained clustering centers model.
        ncluster (int): Number of clusters for KMeans.
        uqthr (float): Uncertainty threshold.
        cluster (str): Clustering method to use ("Kmeans" or "DBSCAN").
        degs (int): Number of degrees in the scan.
        seed (int): Random seed for reproducibility.
        degs_mode (int): Degree mode (0 for 180, 1 for 360).
    """

    try:
        cmd = [
            PYTHON_EXEC, "testing_scan.py",
            "-file_mode", str(file_mode),
            "-testing_scan", os.path.join(workspace_dir, testing_scan),
            "-testing_scan_dark", os.path.join(workspace_dir, testing_scan_dark),
            "-thold", str(thold),
            "-output_csv", output_csv,
            "-trained_encoder", trained_encoder,
            "-trained_centers", trained_centers,
            "-ncluster", str(ncluster),
            "-uqthr", str(uqthr),
            "-cluster", cluster,
            "-degs", str(degs),
            "-seed", str(seed),
            "-degs_mode", str(degs_mode)
        ]


        result = subprocess.run(
            cmd,
            cwd=SCRIPT_DIR,  # Set working directory to the script's directory
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        return f"[SUCCESS] Script completed successfully:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"[ERROR] Script failed:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"


if __name__ == "__main__":
    mcp.run()
    # local version for testing
    # print(run_testing_scan(
    #     file_mode=1,
    #     testing_scan = "park_ss_ff_260MPa_000497.edf.ge5",
    #     testing_scan_dark = "dark_before_000502.edf.ge5",
    #     thold = 100,
    #     output_csv = "rei_score_260MPa.csv"
    # ))
