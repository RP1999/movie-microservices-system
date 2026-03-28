#!/bin/bash
# Stop script on Ctrl+C and kill background processes
trap "kill 0" SIGINT

echo "=========================================="
echo "    Starting Movie Booking Microservices  "
echo "=========================================="

# Start Streaming Service
echo "Installing and Starting Streaming Service..."
cd streaming-service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8003 &
cd ..

# Start API Gateway
echo "Installing and Starting API Gateway..."
cd api-gateway
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000 &
cd ..

echo ""
echo "=========================================="
echo "    Services are successfully running!    "
echo "=========================================="
echo "Streaming Service Swagger: http://localhost:8003/docs"
echo "API Gateway Swagger       : http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services."
wait
