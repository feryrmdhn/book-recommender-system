from fastapi import FastAPI
from dotenv import load_dotenv
from app.services import books_service, classification_service, recommender_service
from app.utils.api_utils import validate_api_key

load_dotenv()
app = FastAPI()

# api get books
app.include_router(books_service.router)

# api classification
app.include_router(classification_service.router)

# api recommendation
app.include_router(recommender_service.router)

