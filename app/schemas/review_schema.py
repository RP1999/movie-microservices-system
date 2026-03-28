from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    userId: str
    movieId: str
    reviewText: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)

class ReviewUpdate(BaseModel):
    reviewText: Optional[str]
    rating: Optional[int] = Field(None, ge=1, le=5)
