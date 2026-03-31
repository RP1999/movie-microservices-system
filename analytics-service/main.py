import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from bson import ObjectId
from database import movies_collection
from models import MovieWatchData, UpdateMovieWatchData

app = FastAPI(
    title="Analytics Service API",
    description="Analytics Microservice for tracking system usage, user activities, and generating reports.",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

def item_helper(item) -> dict:
    return {"id": str(item["_id"]), **{k: v for k, v in item.items() if k != "_id"}}

@app.post("/analytics/movies", status_code=201, tags=["Analytics"])
async def create_movie_record(data: MovieWatchData):
    new_data = await movies_collection.insert_one(data.dict())
    created_data = await movies_collection.find_one({"_id": new_data.inserted_id})
    return {"status": "success", "message": "Watch activity tracked", "data": item_helper(created_data)}

@app.get("/analytics/movies", tags=["Analytics"])
async def get_movies_analytics(limit: int = 10):
    movies = await movies_collection.find().sort("watch_count", -1).limit(limit).to_list(100)
    return {"status": "success", "most_watched": [item_helper(movie) for movie in movies]}

@app.get("/analytics/dashboard", tags=["Dashboard"])
async def get_dashboard_reports():
    pipeline = [{"$group": {"_id": "$genre", "total_views": {"$sum": "$watch_count"}}}]
    genres = await movies_collection.aggregate(pipeline).to_list(10)
    return {
        "report_type": "Live System Dashboard",
        "systemHealth": "99.9% Operational",
        "total_watch_time_hours": 340,
        "popular_genres": [{"genre": g["_id"], "views": g["total_views"]} for g in genres if g["_id"]]
    }

@app.put("/analytics/movies/{id}", tags=["Analytics"])
async def update_movie_record(id: str, data: UpdateMovieWatchData):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if update_data:
        update_result = await movies_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if update_result.matched_count == 1:
            return {"status": "success", "message": "Analytics Record successfully updated"}
    raise HTTPException(status_code=404, detail="Data not found")

@app.delete("/analytics/movies/{id}", tags=["Analytics"])
async def delete_movie_record(id: str):
    delete_result = await movies_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"status": "success", "message": "Analytics Record permanently deleted"}
    raise HTTPException(status_code=404, detail="Data not found")

if __name__ == "__main__":
    uvicorn.run("analytics_service.main:app", host="0.0.0.0", port=8006, reload=True)
