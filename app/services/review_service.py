from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from app.database import review_collection

def serialize(review):
    review["_id"] = str(review["_id"])
    return review

def add_review(data):
    data["likes"] = 0
    data["dislikes"] = 0
    data["createdAt"] = datetime.utcnow()
    data["updatedAt"] = datetime.utcnow()

    result = review_collection.insert_one(data)
    return str(result.inserted_id)

def edit_review(review_id, data):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    data["updatedAt"] = datetime.utcnow()

    result = review_collection.update_one(
        {"_id": ObjectId(review_id)},
        {"$set": data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")

def delete_review(review_id):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = review_collection.delete_one({"_id": ObjectId(review_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")

def get_reviews(movie_id):
    reviews = review_collection.find({"movieId": movie_id}).sort("createdAt", -1)
    return [serialize(r) for r in reviews]

def get_average_rating(movie_id):
    pipeline = [
        {"$match": {"movieId": movie_id}},
        {"$group": {"_id": "$movieId", "avgRating": {"$avg": "$rating"}}}
    ]

    result = list(review_collection.aggregate(pipeline))

    if not result:
        return {"averageRating": 0}

    return {"averageRating": round(result[0]["avgRating"], 2)}

def like_review(review_id):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = review_collection.update_one(
        {"_id": ObjectId(review_id)},
        {"$inc": {"likes": 1}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")

def dislike_review(review_id):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = review_collection.update_one(
        {"_id": ObjectId(review_id)},
        {"$inc": {"dislikes": 1}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
