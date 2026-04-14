# Context Portfolio MCP Server

A lightweight MCP (Model Context Protocol) server that serves your 10 personal context markdown files to any connected LLM client. Files are read from disk on every request — update them anytime without restarting.

---

## Files in this repo

| File | Purpose |
|---|---|
| `server.py` | MCP server (single file, all logic) |
| `Dockerfile` | Container build |
| `docker-compose.yml` | Coolify-compatible compose file |
| `requirements.txt` | Python deps (`mcp` only) |
| `context/` | Your 10 markdown files live here |

---

## The 10 context files

| Key | File |
|---|---|
| `identity` | `context/identity.md` |
| `role-and-responsibilities` | `context/role-and-responsibilities.md` |
| `current-projects` | `context/current-projects.md` |
| `team-and-relationships` | `context/team-and-relationships.md` |
| `tools-and-systems` | `context/tools-and-systems.md` |
| `communication-style` | `context/communication-style.md` |
| `goals-and-priorities` | `context/goals-and-priorities.md` |
| `preferences-and-constraints` | `context/preferences-and-constraints.md` |
| `domain-knowledge` | `context/domain-knowledge.md` |
| `decision-log` | `context/decision-log.md` |

---

## MCP Tools exposed

| Tool | What it does |
|---|---|
| `list_files` | Returns all keys + descriptions |
| `get_context` | Returns one file by key |
| `get_all_context` | Returns all 10 files concatenated |

---

## Deploying to Coolify (step-by-step)

(keep the rest EXACTLY as you already pasted)