FROM python:3.12-slim

# No interactive prompts during build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

    WORKDIR /app

    # Install dependencies first (layer cache)
    COPY requirements.txt /app/requirements.txt
    RUN pip install --no-cache-dir -r /app/requirements.txt

    # Copy server code
    COPY server.py /app/server.py

    # Context files are mounted at runtime — don't COPY them here
    # Mount a volume at /context when running the container
    RUN mkdir -p /context

    # MCP servers communicate over stdio — no exposed port needed.
    # If you need HTTP transport in the future, expose 8000.

    CMD ["python", "/app/server.py"]
