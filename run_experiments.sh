docker build -t pysealer-experiments .
docker run -it pysealer-experiments bash -c "uv run run_experiments.py"