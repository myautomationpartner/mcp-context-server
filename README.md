<<<<<<< HEAD
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

### Prerequisites
- Coolify running on your Hetzner VPS
- SSH access to the VPS
- A GitHub repo (or Coolify can use a local compose file)

---

### Option A — Deploy via GitHub repo (recommended)

**Step 1 — Push this folder to a GitHub repo**

```bash
# From your local machine
cd context-mcp-server
git init
git add .
git commit -m "initial context mcp server"
git remote add origin https://github.com/YOUR_USERNAME/context-mcp-server.git
git push -u origin main
```

**Step 2 — Add a new service in Coolify**

1. Open Coolify dashboard → **Projects** → your project → **+ New Resource**
2. Choose **Docker Compose**
3. Choose **GitHub** as source → select your repo → branch `main`
4. Set the **Docker Compose location** to `docker-compose.yml`
5. Click **Save**

**Step 3 — Set up the context volume**

The `./context` path in docker-compose.yml is relative to the repo root. Coolify will create it automatically on first deploy. You need to populate it with your markdown files.

SSH into the VPS and find where Coolify checked out your repo:

```bash
# Usually under /data/coolify/services/ or the path shown in Coolify UI
# Check: Coolify → your service → Configuration → show paths
ls /data/coolify/services/YOUR_SERVICE_ID/
```

Then copy your files there:

```bash
scp context/*.md root@YOUR_VPS_IP:/data/coolify/services/YOUR_SERVICE_ID/context/
```

**Step 4 — Deploy**

Click **Deploy** in Coolify. Watch the build log — should take ~60 seconds.

---

### Option B — Deploy via direct SSH (no GitHub)

**Step 1 — Copy files to VPS**

```bash
# From your local machine — copy the whole folder
scp -r context-mcp-server root@YOUR_VPS_IP:/opt/context-mcp/
```

**Step 2 — Add service in Coolify**

1. Coolify → **Projects** → **+ New Resource** → **Docker Compose**
2. Choose **Raw / Manual** compose input
3. Paste the contents of `docker-compose.yml`
4. Under **Volumes**, set the host path for `./context` to `/opt/context-mcp/context`
5. Deploy

---

### Verifying the deployment

```bash
# SSH into VPS
ssh root@YOUR_VPS_IP

# Check container is running
docker ps | grep context-mcp

# Tail logs
docker logs context-mcp -f

# You should see:
# INFO Context Portfolio MCP Server starting
# INFO Context directory: /context
# INFO Files present: ['identity', 'role-and-responsibilities', ...]
```

---

## Connecting Claude Desktop

MCP over stdio requires Claude Desktop to be able to run the server process directly or connect via a proxy. Since your server is on a remote VPS, you have two options:

### Option 1 — SSH stdio proxy (simplest, no open port)

Claude Desktop spawns an SSH command that runs the server inside Docker on the VPS. No ports exposed.

Add this to your `claude_desktop_config.json` (see `claude_desktop_config.json` in this repo):

```json
{
  "mcpServers": {
    "context-portfolio": {
      "command": "ssh",
      "args": [
        "-o", "StrictHostKeyChecking=no",
        "root@YOUR_VPS_IP",
        "docker exec -i context-mcp python /app/server.py"
      ]
    }
  }
}
```

**Requirements:** Your local SSH key must be authorized on the VPS (`~/.ssh/authorized_keys`).

### Option 2 — mcp-proxy with HTTP/SSE transport (if you want a persistent URL)

Install `mcp-proxy` on the VPS, run it in front of the server, and expose it via Coolify's reverse proxy on a subdomain. See: https://github.com/sparfenyuk/mcp-proxy

---

## Updating a context file (no restart needed)

Files are read from disk on every tool call. Just replace the file:

```bash
# From your local machine
scp context/current-projects.md root@YOUR_VPS_IP:/path/to/context/current-projects.md
```

Or edit directly on the VPS:

```bash
ssh root@YOUR_VPS_IP
nano /path/to/context/current-projects.md
```

That's it. The next LLM call will get the updated content.

---

## Rebuilding the container

Only needed if you change `server.py`, `Dockerfile`, or `requirements.txt`:

```bash
# In Coolify: click Redeploy
# Or via SSH:
cd /opt/context-mcp
docker compose build --no-cache
docker compose up -d
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `CONTEXT_DIR` | `/context` | Path inside container where markdown files live |

---

## Troubleshooting

**Container exits immediately**
- Check logs: `docker logs context-mcp`
- Usually a missing dependency — run `docker compose build --no-cache`

**`list_files` shows files as missing**
- Volume not mounted correctly
- Verify: `docker exec context-mcp ls /context`

**Claude Desktop can't connect**
- Test SSH manually: `ssh root@YOUR_VPS_IP "docker exec -i context-mcp python /app/server.py"`
- Check SSH key is in `~/.ssh/authorized_keys` on the VPS

**File changes not reflected**
- The volume must be mounted read-write (not `:ro`) if editing from inside the container
- Default mount in docker-compose.yml is `:ro` (read-only from container side) — files are updated from host, which is correct
=======
# mcp-context-server
MCP server for personal context portfolio
>>>>>>> bc26c7c00cc7c08af8875e3377e92bfef9358bd6
