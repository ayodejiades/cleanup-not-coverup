# Run the experiment on Kaggle by hand

Use this when the `kaggle` CLI is not set up.

1. Open kaggle.com/code, then New Notebook, then File, then Import `run.ipynb` (this folder).
2. Set Accelerator to GPU T4 x2, and turn Internet on.
3. Run All. The notebook installs Ollama, runs the grid, the report and the analyses, and writes
   `rops-output.tar.gz`.
4. Download `rops-output.tar.gz` from the notebook's output.
5. Back in the project, run: `rops-kaggle pull <dir> --from <file>`
