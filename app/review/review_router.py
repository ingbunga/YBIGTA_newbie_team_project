from fastapi import APIRouter, HTTPException, Depends, status
from pydantic_core import ValidationError
from app.review.review_schema import PreprocessedReview, SiteName
from app.review.review_service import ReviewService
from app.dependencies import get_review_service
from app.responses.base_response import BaseResponse

review = APIRouter(prefix="/review")


@review.post("/preprocess/{site_name}", response_model=BaseResponse[list[PreprocessedReview]], status_code=status.HTTP_200_OK)
def preprocess_reviews(site_name: str, service: ReviewService = Depends(get_review_service)) -> BaseResponse[list[PreprocessedReview]]:
    try:
        site_name = SiteName(site_name.lower())
        reviews = service.get_preprocessed_reviews(site_name)
        return BaseResponse(status="success", data=reviews, message="Preprocessing Success.")
    except ValidationError as exc:
        print(repr(exc.errors()))
        raise HTTPException(status_code=422, detail="Validation Error")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
