# Non-blocking MCP Tasks with Strands Agents

Code for the technical note: https://gardens-of-ai.co.uk/posts/non-blocking-mcp-tasks-with-strands/

A Strands agent starts a long-running MCP tool, does other work while it runs, and collects the result later.

MCP Tasks is experimental in the MCP specification and in the Strands SDK. The APIs can change.

## Files

| File | What it does |
|---|---|
| `mcp_long_running_task.py` | FastMCP server with one task tool, `slow_computation`. |
| `agent_non_blocking.py` | The agent gets two wrapper tools, start and check, and works while the job runs. |

## Run

You need [uv](https://docs.astral.sh/uv/) and Python 3.13. Strands uses Amazon Bedrock by default, so you need
AWS credentials with Bedrock model access, from the normal AWS credential chain (for example `aws configure`
or `AWS_PROFILE`). Nothing in this folder holds credentials.

    uv sync
    uv run agent_non_blocking.py

The agent starts the server for you, as a subprocess over stdio.
