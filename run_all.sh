#!/bin/bash
# Stop script on Ctrl+C and kill background processes
trap "kill 0" SIGINT

echo "=========================================="
echo "    Starting Movie Booking Microservices  "
echo "=========================================="

# Start Streaming Service (Ranidu) - Port 8003
echo "Installing and Starting Streaming Service..."
cd streaming-service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
uvicorn main:app --port 8003 &
cd ..

# Start Watchlist Service (Siluni) - Port 8004
echo "Installing and Starting Watchlist Service..."
cd watchlist-service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
uvicorn app.main:app --port 8004 &
cd ..

# Start Review Service (Piyumi) - Port 8005
echo "Installing and Starting Review Service..."
cd review-service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
uvicorn app.main:app --port 8005 &
cd ..

# Start API Gateway - Port 8000
echo "Installing and Starting API Gateway..."
cd api-gateway
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
uvicorn main:app --port 8000 &
cd ..

echo ""
echo "=========================================="
echo "    Services are successfully running!    "
echo "=========================================="
echo "Streaming Service Swagger : http://localhost:8003/docs"
echo "Watchlist Service Swagger : http://localhost:8004/docs"
echo "Review Service Swagger    : http://localhost:8005/docs"
echo "API Gateway Swagger       : http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services."
wait
