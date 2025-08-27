#! /bin/bash

set -e

echo ">>> Starting ollama serve ..." 
/bin/ollama serve &

sleep 5

echo ">>> Running Phi3 model ..."
/bin/ollama run phi3 &

wait