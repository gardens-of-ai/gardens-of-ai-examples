# The agent starts the job, does other work, and checks back when it chooses.
from mcp import stdio_client, StdioServerParameters
from strands import Agent, tool
from strands.tools.mcp import MCPClient

# Create MCP client with stdio transport
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uv", args=["run", "./mcp_long_running_task.py"])),
    tasks_config={})

@tool
def start_slow_computation(duration: int) -> str:
    """Start a slow computation in the background. Returns a task_id at once.
    The job keeps running. Use check_task with the task_id to get the result later.

    Args:
        duration: How many seconds the job runs.
    """
    handle = stdio_mcp_client.submit_tool_sync("slow_computation", {"duration": duration})
    return f"Task started. task_id={handle.task_id}"

@tool
def check_task(task_id: str) -> str:
    """Check a background task. Returns 'working' if it is not done,
    or the final result if it is done.

    Args:
        task_id: The id that start_slow_computation returned.
    """
    status = stdio_mcp_client.get_task_sync(task_id)
    if status.status == "working":
        return "Still working. Do other useful work, then check again."
    if status.status == "completed":
        return f"Done: {status.result.content[0].text}"
    return f"Task ended with status {status.status}: {status.status_message}"


# The agent gets ONLY the two wrapper tools. The client is not passed to the
# agent, so we keep it open ourselves with `with`.
with stdio_mcp_client:
    agent = Agent(tools=[start_slow_computation, check_task])
    agent(
        "Start the slow computation for 30 seconds. "
        "While it runs, explain AWS Lambda. "
        "Then check the task and tell me the result. "
        "If you end up finished but waiting for the slow task then make up funny things to tell me until it returns"
    )
