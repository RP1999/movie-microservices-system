#!/bin/bash
# Stop script on Ctrl+C and kill background processes
trap "kill 0" SIGINT

echo "=========================================="
echo "    Starting Movie Booking Microservices  "
echo "=========================================="

# Helper function to start a service
start_service() {
    local name=$1
    local dir=$2
    local port=$3
    local module=$4

    echo ""
    echo ">>> Starting $name on port $port..."
    cd "$dir"

    # Always create a fresh venv to avoid stale broken installs
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    source venv/bin/activate
    pip install -r requirements.txt -q --upgrade

    # Run uvicorn using the venv's python to avoid "command not found" issues
    venv/bin/uvicorn "$module" --port "$port" &

    cd ..
    deactivate 2>/dev/null || true
}

# Start all services
start_service "Streaming Service (Ranidu)"  streaming-service  8003  "main:app"
start_service "Watchlist Service (Siluni)"  watchlist-service  8004  "app.main:app"
start_service "Review Service (Piyumi)"     review-service     8005  "app.main:app"
start_service "User Service (Lashan)"       user-service       8001  "main:app"
start_service "API Gateway"                 api-gateway        8000  "main:app"

echo ""
echo "=========================================="
echo "    Services are successfully running!    "
echo "=========================================="
echo "Streaming Service Swagger : http://localhost:8003/docs"
echo "Watchlist Service Swagger : http://localhost:8004/docs"
echo "Review Service Swagger    : http://localhost:8005/docs"
echo "User Service Swagger      : http://localhost:8001/docs"
echo "API Gateway Swagger       : http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services."
wait
