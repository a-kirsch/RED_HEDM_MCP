# argo_bridge custom base url:http://localhost:7285
import os

from mcp.server.fastmcp import FastMCP
from BYOL_training_server import run_training_script
from K_means_clustering_server import run_baseline_clustering
from REI_score_server import run_testing_scan

mcp = FastMCP("Full Workflow")

#Setting default directory for workspace
default_dir = os.environ.get("CLINE_WORKSPACE", "/home/beams/WZHENG/RareEventDetectionHEDM/example_dataset/raw/")


@mcp.tool()
def full_workflow(training_scan_file: str, training_dark_file: str, testing_scan: str, testing_dark: str, thold: int = 100, file_mode: int = 1, workspace_dir: str = default_dir, output_csv: str = "rei_score_260MPa.csv") -> str:
    """From scans to REI scores, without intermediate steps."""
    results = []
    results.append(run_training_script(training_scan_file, training_dark_file, thold, workspace_dir))
    results.append(run_baseline_clustering(training_scan_file, training_dark_file, file_mode, thold, workspace_dir))
    results.append(run_testing_scan(testing_scan, testing_dark, file_mode, thold, output_csv, workspace_dir))
    return "\n".join(results)

if __name__ == "__main__":
    mcp.run()