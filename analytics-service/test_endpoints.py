import httpx
import json

base_url = "http://localhost:8006"

def test_endpoints():
    print("Testing API Endpoints on http://localhost:8006")
    try:
        # 1. POST /analytics/movies
        print("\n--- 1. Testing POST /analytics/movies ---")
        payload = {
            "movie_id": "movie_001",
            "title": "Inception",
            "genre": "Sci-Fi",
            "watch_count": 1,
            "total_watch_time_minutes": 140
        }
        r = httpx.post(f"{base_url}/analytics/movies", json=payload)
        print(f"Status: {r.status_code}")
        print(r.json())
        assert r.status_code == 201, "POST failed"
        movie_record_id = r.json()["data"]["id"]
        
        # 2. GET /analytics/movies
        print("\n--- 2. Testing GET /analytics/movies ---")
        r = httpx.get(f"{base_url}/analytics/movies?limit=5")
        print(f"Status: {r.status_code}")
        print(r.json())
        assert r.status_code == 200, "GET movies failed"
        
        # 3. GET /analytics/dashboard
        print("\n--- 3. Testing GET /analytics/dashboard ---")
        r = httpx.get(f"{base_url}/analytics/dashboard")
        print(f"Status: {r.status_code}")
        print(r.json())
        assert r.status_code == 200, "GET dashboard failed"
        
        # 4. PUT /analytics/movies/{id}
        print(f"\n--- 4. Testing PUT /analytics/movies/{movie_record_id} ---")
        update_payload = {"watch_count": 5}
        r = httpx.put(f"{base_url}/analytics/movies/{movie_record_id}", json=update_payload)
        print(f"Status: {r.status_code}")
        print(r.json())
        assert r.status_code == 200, "PUT failed"
        
        # 5. DELETE /analytics/movies/{id}
        print(f"\n--- 5. Testing DELETE /analytics/movies/{movie_record_id} ---")
        r = httpx.delete(f"{base_url}/analytics/movies/{movie_record_id}")
        print(f"Status: {r.status_code}")
        print(r.json())
        assert r.status_code == 200, "DELETE failed"

        print("\n✅ All 5 endpoints tested fully and working perfectly!")
        
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")

if __name__ == "__main__":
    test_endpoints()
