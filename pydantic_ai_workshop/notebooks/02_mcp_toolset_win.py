"""
This is just standalone cell from 02_capabilities.ipynb, the MCPServerStdio does
not work on Win platform inside Jupyter notebook due to issue with interprocess
communication.
"""
import asyncio
import sys
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print as rprint
from rich import print as rprint
from rich.markdown import Markdown

PROJECT_ROOT_PATH = Path.cwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str = Field(
        ...,
        description="Workshop-allocated Anthropic API key. Required.",
    )
    model_id: str = Field(
        default="claude-haiku-4-5-20251001",
        description="Default model id. Haiku is cheap and fast for the demos.",
    )
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"


settings = Settings()  # type: ignore[call-arg]

model = AnthropicModel(
    settings.model_id,
    provider=AnthropicProvider(api_key=settings.anthropic_api_key),
)

rprint(Markdown("# Capabilities"))
rprint("model_id  :", settings.model_id)


_MCP_SERVER_SCRIPT = """
from mcp.server.fastmcp import FastMCP

_CATALOGUE = {
    "basic_plan": {"price_usd": 9.99, "users": 1, "storage_gb": 5, "support": "email"},
    "pro_plan": {"price_usd": 29.99, "users": 10, "storage_gb": 100, "support": "priority"},
    "enterprise_plan": {"price_usd": 99.99, "users": "unlimited", "storage_gb": 1000, "support": "dedicated"},
}

mcp = FastMCP("catalogue")

@mcp.tool()
def get_product_info(item_name: str) -> dict:
    \"\"\"Return full product info for a catalogue item, or an error if not found.\"\"\"
    key = item_name.strip().lower()
    if key not in _CATALOGUE:
        return {"error": "unknown item", "known": sorted(_CATALOGUE)}
    return {"item_name": key, **_CATALOGUE[key]}

if __name__ == "__main__":
    mcp.run()
"""

_MCP_SERVER_PATH = Path("notebook_capabilities_mcp.py")
_MCP_SERVER_PATH.write_text(_MCP_SERVER_SCRIPT)

mcp_server = MCPServerStdio(sys.executable, args=[str(_MCP_SERVER_PATH)], timeout=15)

mcp_agent = Agent(
    model,
    toolsets=[mcp_server],
    instructions=(
        "You are a helpful assistant. Use the catalogue tools to look up "
        "product details when the user asks about a specific plan."
    ),
)


async def run_agent():
    async with mcp_server:
        result = await mcp_agent.run()
        rprint(result.output)

asyncio.run(run_agent())
