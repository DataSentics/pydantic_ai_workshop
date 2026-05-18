# Pydantic AI workshop

Four self-contained notebooks walking through `pydantic-ai`'s feature surface:

| Notebook | Theme |
|---|---|
| `01_intro.ipynb` | Schemas, `Agent`, output modes, run methods. |
| `02_capabilities.ipynb` | Tools, capabilities, builtin tools, MCP, RAG, multimodal. |
| `03_workflows.ipynb` | Multi-agent, graphs, message history, compaction, memory. |
| `04_production.ipynb` | Tests, observability, evals, hooks, fallback, deferred tools, deployment. |

## Setup

1. **Install [`uv`](https://docs.astral.sh/uv/).** macOS/Linux:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Windows (PowerShell):

   Execution policy bypass is required, cf. [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone and sync dependencies.** Open the repo in VS Code, then in the integrated terminal:

   ```bash
   uv sync
   ```

   This creates a `.venv/`, installs everything in `pyproject.toml`, and registers an `ipykernel` for the notebooks.

3. **Add your Anthropic API key.** Copy `.env.example` to `.env` and fill in your key:

   ```bash
   cp .env.example .env
   ```

   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   ```

   Optional: `LOGFIRE_TOKEN=...` to ship traces to the Logfire dashboard instead of stdout (only used in `04_production`).

## Run

### VS Code
1. Open `pydantic_ai_workshop/notebooks/01_intro.ipynb` in VS Code. (Requires [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter))
2. Click **Select Kernel** in the top-right and pick the `.venv` Python (`uv` registered it during `uv sync`).  If you do not see pydantic-ai-workshop kernel right away you might need to restart VS Code and run `uv sync` again.
3. Run cells top-to-bottom.

### Jupyter Lab
If you prefer Jupyter Lab you can
1. In terminal run jupyter server using `uv run --with jupyter jupyter lab` (cf. [Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)).
2. Copy the URL with token and paste into your favorite browser.
3. Run cells top-to-bottom.

Each notebook is independent — start anywhere. Cells inside a notebook do build on each other, so run them in order.

## Costs

Most cells make 1–2 Anthropic API calls. Two cells in `04_production` are marked **💰** because they're heavier (the eval suite runs ~16 model requests; the deferred-tools demo runs 2). Skip them if you're cost-conscious.
