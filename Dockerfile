FROM python:3.12-slim

# All app files live here
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MCP server code
COPY server.py /app/server.py

# Environment variable for context directory
ENV CONTEXT_DIR=/context

# Default command (used by proxy via docker exec)
CMD ["python", "/app/server.py"]