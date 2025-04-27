#!/bin/bash

# Function to wait for a port to be open
wait_for_port() {
  local port=$1
  local name=$2
  echo -n "Waiting for $name to be ready on port $port... "
  while ! nc -z localhost $port; do
    sleep 1
  done
  echo "done."
}

# Start the webui (run silently, output to log)
./sd-webui/webui.sh --listen --xformers --share --api > webui.log 2>&1 &
WEBUI_PID=$!
echo "Started webui (PID $WEBUI_PID, output in webui.log)"

wait_for_port 7860 "webui"

# Start Flask RESTful service (show output)
echo "Starting Flask RESTful service..."
python3 -m service &
FLASK_PID=$!
wait_for_port 5000 "Flask RESTful service"
echo "Flask RESTful service started (PID $FLASK_PID)"

# Start Streamlit frontend app (show output)
echo "Starting Streamlit frontend app..."
python3 -m streamlit run streamlit_app.py &
STREAMLIT_PID=$!
wait_for_port 8501 "Streamlit frontend app"
echo "Streamlit frontend app started (PID $STREAMLIT_PID)"

# Optionally, wait for all to finish (Ctrl+C to stop all)
wait $WEBUI_PID $FLASK_PID $STREAMLIT_PID 