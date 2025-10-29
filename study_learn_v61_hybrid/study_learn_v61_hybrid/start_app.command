#!/bin/bash
set -e

# Create venv
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

# Find free port
PORT=8501
for p in $(seq 8501 8510); do
  if ! lsof -i :$p -sTCP:LISTEN >/dev/null 2>&1; then
    PORT=$p
    break
  fi
done

exec streamlit run streamlit_app.py --server.port $PORT
