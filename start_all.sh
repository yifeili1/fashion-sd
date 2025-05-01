#!/bin/bash

# Function to check if a port is in use
is_port_in_use() {
  local port=$1
  if nc -z localhost $port >/dev/null 2>&1; then
    return 0  # Port is in use
  else
    return 1  # Port is not in use
  fi
}

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

# Check if webui is already running
if is_port_in_use 7860; then
  echo "WebUI is already running on port 7860, skipping startup..."
  WEBUI_PID=""
else
  # Start the webui (run silently, output to log)
  ./sd-webui/webui.sh --listen --xformers --share --api > webui.log 2>&1 &
  WEBUI_PID=$!
  echo "Started webui (PID $WEBUI_PID, output in webui.log)"
  wait_for_port 7860 "webui"
fi

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
if [ -n "$WEBUI_PID" ]; then
  wait $WEBUI_PID $FLASK_PID $STREAMLIT_PID
else
  wait $FLASK_PID $STREAMLIT_PID 