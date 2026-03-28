from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI(
    title="API Gateway",
    description="Main entry point for all microservices in the Movie recommendation system. Fulfills the assignment criteria for port-hiding.",
    version="1.0.0"
)

# Configuration for underlying services
SERVICES = {
    "streaming": "http://localhost:8003",
    # Other services can be added here
    # "user": "http://localhost:8001",
    # "movie": "http://localhost:8002",
}

@app.get("/", tags=["Gateway Info"])
def gateway_home():
    """Health check for the API Gateway."""
    return {"message": "API Gateway is running. Use /streaming/docs to view streaming endpoints."}

async def handle_proxy(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")

    target_url = f"{SERVICES[service_name]}/{path}"
    headers = dict(request.headers)
    if "host" in headers:
        del headers["host"]
        
    client = httpx.AsyncClient()
    try:
        target_request = client.build_request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=await request.body(),
            params=request.query_params
        )
        response = await client.send(target_request, stream=True)
        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Communication error with {service_name}: {exc}")

# We split the methods out individually below to fix a known bug in Swagger UI 
# where overlapping proxy paths cause the UI to only open the DELETE box.

@app.get("/{service_name}/{path:path}", tags=["Reverse Proxy"])
async def proxy_get(service_name: str, path: str, request: Request):
    return await handle_proxy(service_name, path, request)

@app.post("/{service_name}/{path:path}", tags=["Reverse Proxy"])
async def proxy_post(service_name: str, path: str, request: Request):
    return await handle_proxy(service_name, path, request)

@app.put("/{service_name}/{path:path}", tags=["Reverse Proxy"])
async def proxy_put(service_name: str, path: str, request: Request):
    return await handle_proxy(service_name, path, request)

@app.delete("/{service_name}/{path:path}", tags=["Reverse Proxy"])
async def proxy_delete(service_name: str, path: str, request: Request):
    return await handle_proxy(service_name, path, request)
