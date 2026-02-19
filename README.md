# pysealer-experiments

Reproducible experiments for evaluating `pysealer` against MCP security attack patterns.

## What this runs

1. Create a Docker container.
2. Install Python 3.14.
3. Install:
	- `pysealer==1.0.0`
	- `mcp-scan==0.4.2` (Snyk Agent Scan)
4. Set up `uv` to run Python tooling.

docker build -t pysealer-experiments .
