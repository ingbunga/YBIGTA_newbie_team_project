from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum

class SiteName(str, Enum):
    LETTERBOXD = "letterboxd"
    NAVER = "naver"
    ROTTENTOMATOES = "rottentomatoes"

# TODO: refactor this later
class Review(BaseModel):
    rating: int | float
    date: str | datetime
    review: str | int | None = None

class PreprocessedReview(BaseModel):
    date: str | datetime
    rating: int
    review: str
    review_length: int
    review_z: float
    keywords: str