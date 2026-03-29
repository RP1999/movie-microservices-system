from fastapi import APIRouter
from app.schemas.review_schema import ReviewCreate, ReviewUpdate
from app.services import review_service

router = APIRouter()

@router.post("/", status_code=201)
def create_review(review: ReviewCreate):
    review_id = review_service.add_review(review.dict())
    return {"message": "Review added", "id": review_id}

@router.put("/{reviewId}")
def update_review(reviewId: str, review: ReviewUpdate):
    review_service.edit_review(reviewId, review.dict(exclude_unset=True))
    return {"message": "Review updated"}

@router.delete("/{reviewId}")
def remove_review(reviewId: str):
    review_service.delete_review(reviewId)
    return {"message": "Review deleted"}

@router.get("/movie/{movieId}")
def fetch_reviews(movieId: str):
    return review_service.get_reviews(movieId)

@router.get("/movie/{movieId}/average-rating")
def average_rating(movieId: str):
    return review_service.get_average_rating(movieId)

@router.post("/{reviewId}/like")
def like(reviewId: str):
    review_service.like_review(reviewId)
    return {"message": "Liked"}

@router.post("/{reviewId}/dislike")
def dislike(reviewId: str):
    review_service.dislike_review(reviewId)
    return {"message": "Disliked"}
