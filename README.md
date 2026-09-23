# CS529 AI Engineering Course Materials

Lesson demos, sample code, and project materials for CS529 AI Engineering. The numbered folders follow the course sequence. Open the folder for the lesson you are working on and follow its instructions; the folders may use different packages and setup steps.

## Before you start

- Install Python (use the version required by the lesson project), [uv](https://docs.astral.sh/uv/getting-started/installation/), and Cursor or VS Code.
- Install Node.js only when a lesson specifically requires it, such as a Node-based MCP server.
- Follow the course setup materials and any instructions inside the lesson folder.

## Course folders

| Folder | Materials |
| --- | --- |
| [1_Pythonfoundations](1_Pythonfoundations) | Python foundations |
| [2_HelloLLMChat](2_HelloLLMChat) | LLM calls and chat examples |
| [3_HelloAgents](3_HelloAgents) | First agent examples |
| [4_AgenticPatterns](4_AgenticPatterns) | Agent workflow patterns |
| [5_PythonScripts](5_PythonScripts) | Supporting Python scripts |
| [6_meomorymgt](6_meomorymgt) | Session memory examples |
| [7_crewai_project](7_crewai_project) | CrewAI projects |
| [8_mcp_openai_crew](8_mcp_openai_crew) | MCP examples with OpenAI Agents SDK and CrewAI |
| [9_deployment](9_deployment) | Deployment examples |

Folder names above match the repository exactly, including `6_meomorymgt`.

## Set up a lesson project

1. Download the repository using **Code → Download ZIP** on GitHub, then extract it. If you already use Git, you may clone it instead.
2. Open the **specific lesson project folder** in your terminal and editor. Look for its `README.md`, `pyproject.toml`, or other setup instructions.
3. If that folder has a `pyproject.toml`, run `uv sync` **from that folder** to install its declared dependencies. Then run the example as directed in the lesson, for example `uv run python example.py` (replace `example.py` with the actual filename). [uv project guide](https://docs.astral.sh/uv/guides/projects/)
4. For notebooks, select that project's `.venv` Python interpreter or kernel in your editor. Follow the lesson instructions if a kernel package must be installed.

There is no single setup command for the entire repository. Some examples require extra services, packages, or a running MCP server; check the relevant lesson instructions.

## API keys and `.env` files

Some examples require API keys. In the relevant project folder, copy `.env.example` to `.env` **if an example file is provided**, then replace the placeholders with your own keys. Add only the variables that project actually uses. For example:

```dotenv
OPENAI_API_KEY=your_key_here
```

Never upload a real `.env` file or API key to GitHub. Keep `.env` excluded from Git. If an API key was uploaded accidentally, revoke it with its provider and create a new one.

## If an example does not run

- Confirm that your terminal is in the correct lesson project folder.
- Check the project's instructions and install its dependencies.
- Confirm required API keys are present and valid.
- For notebooks, check that the selected kernel belongs to the lesson project's environment.
- For MCP examples, check whether the server must be started separately.

These examples are intended for learning. Follow your instructor's directions for assignments and submissions.
