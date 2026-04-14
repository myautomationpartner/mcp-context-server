FROM python:3.12-slim

# cache-bust: 2026-04-14
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py /app/server.py

ENV CONTEXT_DIR=/context

CMD ["python", "/app/server.py"]