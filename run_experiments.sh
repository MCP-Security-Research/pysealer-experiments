docker build -t pysealer-experiments .
docker run --env-file .env -it pysealer-experiments bash -c "uv run run_experiments.py"