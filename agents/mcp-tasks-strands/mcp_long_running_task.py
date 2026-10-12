import asyncio
from fastmcp import FastMCP
from fastmcp_tasks import TasksExtension

# Initialize FastMCP server
mcp = FastMCP("TaskServer")

# Register the background tasks extension
mcp.add_extension(TasksExtension())

@mcp.tool(task=True)
async def slow_computation(duration: int) -> str:
    """A long-running background operation."""
    for i in range(duration):
        await asyncio.sleep(1)
    return f"Completed in {duration} seconds"

if __name__ == "__main__":
    mcp.run()
