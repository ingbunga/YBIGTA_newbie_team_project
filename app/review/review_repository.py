import json

from typing import Dict, Optional

from app.review.review_schema import Review, SiteName
from app.config import USER_DATA
from database.mongodb_connection import mongo_db

class ReviewRepository:
    def __init__(self) -> None:
        pass

    def get_reviews_by_site_name(self, site_name: SiteName) -> Optional[list[Review]]:
        reviews = mongo_db['reviews_' + site_name.value].find()
        return [Review(**review) for review in reviews] if reviews else None
    
    def save_reviews(self, site_name: SiteName, reviews: list[Review]) -> None:
        collection_name = 'preprocessed_reviews_' + site_name.value
        if collection_name not in mongo_db.list_collection_names():
            mongo_db.create_collection(collection_name)
        mongo_db[collection_name].delete_many({})
        preprocessed_reviews = mongo_db[collection_name]
        preprocessed_reviews.insert_many([review.model_dump() for review in reviews])
