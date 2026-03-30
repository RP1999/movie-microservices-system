from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Value cannot be empty.")
    return cleaned


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=160)
    category: str = Field(..., min_length=1, max_length=80)

    @field_validator("title", "category", mode="before")
    @classmethod
    def clean_required_text(cls, value: str | None) -> str | None:
        return _clean_text(value)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, min_length=1, max_length=80)

    @field_validator("title", "category", mode="before")
    @classmethod
    def clean_optional_text(cls, value: str | None) -> str | None:
        return _clean_text(value)


class MovieResponse(BaseModel):
    id: str
    title: str
    category: str
    thumbnail_url: str | None = None
    video_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    message: str
