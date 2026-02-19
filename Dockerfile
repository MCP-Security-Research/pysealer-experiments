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

# Uv==0.10.4
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv==0.10.4

# Pysealer==1.0.0
RUN pip install --no-cache-dir pysealer==1.0.0

COPY pyproject.toml .
RUN uv sync --no-dev

COPY . .

COPY ./simulated-attacks /app/simulated-attacks
WORKDIR /app/simulated-attacks

RUN chmod +x /app/simulated-attacks/run_experiments.py

CMD ["uv", "run", "python", "simulated-attacks/run_experiments.py"]