#!/usr/bin/env python3
"""
Context Portfolio MCP Server
Serves personal context markdown files as MCP resources and tools.
Files are read from /context directory on every request — no restart needed to update.
"""

import asyncio
import json
import logging
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# ── Configuration ────────────────────────────────────────────────────────────

CONTEXT_DIR = Path(os.environ.get("CONTEXT_DIR", "/context"))

# Ordered list of (key, description) pairs
FILES: list[tuple[str, str]] = [
    ("identity",                "Who Kenny is — background, expertise, and how he works"),
    ("role-and-responsibilities", "Day job and MAP responsibilities, typical work session"),
    ("current-projects",        "Active projects, status, and priorities"),
    ("team-and-relationships",  "Key people — wife, Dancescapes, day-job colleagues"),
    ("tools-and-systems",       "Full tech stack — infra, core stack, integrations, dev tools"),
    ("communication-style",     "How Kenny writes, formats, and prefers to communicate"),
    ("goals-and-priorities",    "Primary goals, milestones, active problems, success criteria"),
    ("preferences-and-constraints", "Time, budget, AI, and infrastructure constraints"),
    ("domain-knowledge",        "Areas of expertise and mental models"),
    ("decision-log",            "How decisions are made and recent decisions taken"),
]

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("context-mcp")

# ── Helpers ───────────────────────────────────────────────────────────────────

def file_path(key: str) -> Path:
    return CONTEXT_DIR / f"{key}.md"


def read_file(key: str) -> str:
    """Read a context file by key. Raises FileNotFoundError if missing."""
    path = file_path(key)
    if not path.exists():
        raise FileNotFoundError(f"Context file not found: {path}")
    return path.read_text(encoding="utf-8")


def valid_keys() -> list[str]:
    return [k for k, _ in FILES]


# ── Server setup ──────────────────────────────────────────────────────────────

server = Server("context-portfolio")


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """Expose each context file as a named MCP resource."""
    resources = []
    for key, description in FILES:
        resources.append(
            types.Resource(
                uri=f"context://{key}",
                name=key,
                description=description,
                mimeType="text/markdown",
            )
        )
    return resources


@server.read_resource()
async def handle_read_resource(uri: types.AnyUrl) -> str:
    """Return the content of a context resource by URI."""
    uri_str = str(uri)
    if not uri_str.startswith("context://"):
        raise ValueError(f"Unknown URI scheme: {uri_str}")
    key = uri_str.removeprefix("context://")
    if key not in valid_keys():
        raise ValueError(f"Unknown context key: {key}")
    try:
        return read_file(key)
    except FileNotFoundError as e:
        return f"[File not found: {e}]"


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_files",
            description="List all available context file keys and their descriptions.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get_context",
            description=(
                "Return the content of a single context file by key. "
                "Use list_files first if you're unsure of available keys."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": (
                            "The context file key, e.g. 'identity', "
                            "'current-projects', 'tools-and-systems'."
                        ),
                    }
                },
                "required": ["key"],
            },
        ),
        types.Tool(
            name="get_all_context",
            description=(
                "Return ALL 10 context files concatenated in order. "
                "Use this to fully load Kenny's portfolio into context."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent]:

    if name == "list_files":
        lines = ["## Available Context Files\n"]
        for key, description in FILES:
            exists = file_path(key).exists()
            status = "" if exists else " ⚠️ file missing"
            lines.append(f"- **{key}**: {description}{status}")
        return [types.TextContent(type="text", text="\n".join(lines))]

    elif name == "get_context":
        key = arguments.get("key", "").strip()
        if not key:
            return [types.TextContent(type="text", text="Error: 'key' argument is required.")]
        if key not in valid_keys():
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown key '{key}'. Valid keys: {', '.join(valid_keys())}",
            )]
        try:
            content = read_file(key)
            return [types.TextContent(type="text", text=content)]
        except FileNotFoundError:
            return [types.TextContent(
                type="text",
                text=f"Error: File for key '{key}' not found in {CONTEXT_DIR}.",
            )]

    elif name == "get_all_context":
        parts = []
        for key, description in FILES:
            parts.append(f"\n\n---\n## [{key}] {description}\n")
            try:
                parts.append(read_file(key))
            except FileNotFoundError:
                parts.append(f"_File not found: {file_path(key)}_")
        return [types.TextContent(type="text", text="".join(parts))]

    else:
        return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'.")]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    log.info("Context Portfolio MCP Server starting")
    log.info("Context directory: %s", CONTEXT_DIR)
    if not CONTEXT_DIR.exists():
        log.warning("Context directory does not exist: %s", CONTEXT_DIR)
    else:
        present = [k for k in valid_keys() if file_path(k).exists()]
        missing = [k for k in valid_keys() if not file_path(k).exists()]
        log.info("Files present: %s", present)
        if missing:
            log.warning("Files missing: %s", missing)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="context-portfolio",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
