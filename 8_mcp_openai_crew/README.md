# CS529: MCP Demos with OpenAI Agents SDK and CrewAI

This folder contains classroom examples of the **Model Context Protocol (MCP)**. An MCP server provides tools; an OpenAI Agents SDK or CrewAI client connects to those tools and uses them to answer a question. Run the commands below **from this folder**, which contains `pyproject.toml`.

## 1. Requirements

- Python **3.12 or later** (required by this project's `pyproject.toml`).
- [uv](https://docs.astral.sh/uv/getting-started/installation/) to install dependencies and run the Python examples. The `uvx` command comes with uv.
- Your own OpenAI API key and an internet connection for the agent demos. API usage may incur charges.
- Node.js, including `npx`, **only for `crew_filemcp.py`**. That demo downloads and starts the filesystem MCP server through `npx`.

Check the installed tools in a terminal:

```text
python --version
uv --version
uvx --version
```

For the filesystem demo, also run `node --version` and `npx --version`. On a computer where `python` is unavailable but `python3` is installed, use `python3 --version` for the first check.

## 2. Install project dependencies

Open a terminal in `8_mcp_openai_crew` and run:

```bash
uv sync
```

This creates a local `.venv` and installs the packages declared in `pyproject.toml`, including `crewai-tools[mcp]` for the filesystem CrewAI demo. `uv.lock` records the resolved package versions; `uv sync` updates it if the project dependencies have changed. You do **not** need to run `uv init`, `uv add`, or create a second virtual environment.

## 3. Activate the environment (optional)

If you want to run commands as `python script.py`, activate `.venv` first:

| Terminal | Activation command |
| --- | --- |
| macOS / Linux | `source .venv/bin/activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |

You can skip activation by using **`uv run python script.py`**, as shown below. `uv run` selects the project environment automatically. To leave an activated environment, run `deactivate`.

## 4. Set your API key

Create a file named `.env` **inside `8_mcp_openai_crew`** with this line, replacing the placeholder with your own key:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

The scripts call `load_dotenv()` to read this file. Keep `.env` private; the repository's `.gitignore` excludes it. A separate key for each student is recommended. No AWS account key is specified by these remote server examples.

## 5. Run a demo

Run **one command at a time** from `8_mcp_openai_crew`. The client scripts launch and close their local MCP servers themselves; there is usually no need to start a server in another terminal.

| Script | What it demonstrates | Command | Extra requirement |
| --- | --- | --- | --- |
| `mymcpserver.py` | Defines `days_between` and `percentage_change` tools | Started by either client below | Keep this file beside the clients. |
| `mymcpclient.py` | OpenAI agent with the custom local MCP server | `uv run python mymcpclient.py` | The `mcp` CLI is supplied by `mcp[cli]` in this project. |
| `crewclient.py` | CrewAI agent with the same custom local MCP server | `uv run python crewclient.py` | Uses the project's Python environment. |
| `openai_inbuilt_mcps.py` | OpenAI agent with Time and Fetch MCP servers | `uv run python openai_inbuilt_mcps.py` | `uvx` and access to the webpage used by Fetch. |
| `crew_inbuilt_mcps.py` | CrewAI agent with Time and Fetch MCP servers | `uv run python crew_inbuilt_mcps.py` | `uvx` and access to the webpage used by Fetch. |
| `crew_filemcp.py` | CrewAI agent reads `course_info.txt` through a filesystem MCP server | `uv run python crew_filemcp.py` | Node.js/`npx`, `crewai-tools[mcp]`, and the included `course_info.txt`. |
| `remote_mcp_openai.py` | OpenAI agent connects to the remote DeepWiki MCP server | `uv run python remote_mcp_openai.py` | Internet access to `mcp.deepwiki.com`. |
| `remote_mcp_crew.py` | CrewAI agents connect to the remote AWS Knowledge MCP server | `uv run python remote_mcp_crew.py` | Internet access to `knowledge-mcp.global.api.aws`. |

The Time and Fetch examples start external tools through `uvx`. Their first run may take longer while uv downloads the MCP server packages. The remote examples connect to services on the internet and may fail if those services are unavailable or blocked by your network. The Time examples use `America/Chicago`; the example question converts a time to `Asia/Kolkata`.

### How the local server starts

- `mymcpclient.py` starts `mymcpserver.py` with the MCP CLI.
- `crewclient.py` starts `mymcpserver.py` with Python.
- The Time and Fetch examples start their servers with `uvx`.
- `crew_filemcp.py` starts the filesystem server with `npx` and limits its access to this project folder.

If you run `mymcpserver.py` by itself, it waits for a client over standard input/output; it does not display a chat interface. Stop it with **Ctrl+C**. Run either client to see the complete demonstration.

## If a demo fails

1. Confirm the terminal is in `8_mcp_openai_crew` and run `uv sync`.
2. Confirm `.env` contains a valid `OPENAI_API_KEY`. Do not paste your key into a shared screenshot or GitHub issue.
3. For `crew_filemcp.py`, check `npx --version` and keep `course_info.txt` beside the script.
4. For Time or Fetch, check `uvx --version` and network access. For remote demos, check access to the named remote MCP server.
5. If an IDE uses another Python interpreter, select `8_mcp_openai_crew/.venv` or run the command from the terminal with `uv run`.

**Note:** These are separate examples. You can change a demonstration question in its script, save it, and rerun that script. Do not upload your `.env`, local `.venv`, or API key to GitHub.
