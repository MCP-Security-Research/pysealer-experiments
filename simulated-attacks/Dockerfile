# Dockerfile for setting up consistent versioning for experiments

# Python==3.14-slim
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Uv==1.2.3
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv==1.2.3

# Pysealer==1.0.0 and mcp-scan==0.4.2
RUN pip install --no-cache-dir pysealer==1.0.0 mcp-scan==0.4.2

COPY pyproject.toml .
RUN uv sync --no-dev

COPY . .

CMD ["uv", "run", "python", "-V"]