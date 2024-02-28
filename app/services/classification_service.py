import os
from fastapi import HTTPException, APIRouter, Depends, Form, UploadFile, File
from app.utils.api_utils import validate_api_key
import random
import string
import boto3
from dotenv import load_dotenv
from joblib import load
from app.db.connection import postgreSQL_connection

load_dotenv()

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")

router = APIRouter()

# Configure Spaces connection
spaces_endpoint_url = S3_ENDPOINT
spaces_access_key = S3_ACCESS_KEY
spaces_secret_key = S3_SECRET_KEY
spaces_bucket_name = 'bucketfiles'

s3 = boto3.client('s3', endpoint_url=spaces_endpoint_url,
                  aws_access_key_id=spaces_access_key,
                  aws_secret_access_key=spaces_secret_key)

# Load classifier model
classifier_model_path = "./app/models/best_nb_classifier.joblib"
classifier_model = load(classifier_model_path)

# Load TF-IDF vectorizer
vectorizer_path = "./app/models/tfidf_vectorizer.joblib"
vectorizer = load(vectorizer_path)

@router.post("/v1/classify")
async def classify_book(
    book_title: str = Form(...),
    book_author: str = Form(...),
    publisher: str = Form(...),
    year_of_publication: int = Form(...),
    image_url_s: UploadFile = File(...),
    image_url_m: UploadFile = File(...),
    user_id: int = Form(...),
    book_rating: int = Form(...),
    age: int = Form(...),
    api_key: str = Depends(validate_api_key)
):
    cursor = None
  
    try:
        cursor = postgreSQL_connection.get_cursor()
        # Generate ISBN random string
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Upload images to DigitalOcean Spaces
        image_url_s_key = f'image-url-s/{random_string}_{image_url_m.filename}'
        image_url_m_key = f'image-url-m/{random_string}_{image_url_m.filename}'

        s3.upload_fileobj(image_url_s.file, spaces_bucket_name, image_url_s_key)
        s3.upload_fileobj(image_url_m.file, spaces_bucket_name, image_url_m_key)

        # Construct URLs for the uploaded images
        image_url_s_path_spaces = f'{spaces_endpoint_url}/{spaces_bucket_name}/{image_url_s_key}'
        image_url_m_path_spaces = f'{spaces_endpoint_url}/{spaces_bucket_name}/{image_url_m_key}'

        book_data = {
            "ISBN": random_string,
            "Book_Title": book_title,
            "Book_Author": book_author,
            "Publisher": publisher,
            "Year_Of_Publication": year_of_publication,
            "Image_URL_S": image_url_s_path_spaces,
            "Image_URL_M": image_url_m_path_spaces,
            "User_ID": user_id,
            "Book_Rating": book_rating,
            "Age": age
        }

        # Vectorize the cleaned title
        title_features = vectorizer.transform([book_data["Book_Title"]])

        # Combine features into one array
        input_features = title_features

        # Predict genre using the model classifier
        predicted_genre = classifier_model.predict(input_features)

        # Insert book data into PostgreSQL
        insert_query = """INSERT INTO books ("ISBN", "Book-Title", "Book-Author", "Publisher", "Year-Of-Publication", "Image-URL-S", "Image-URL-M", "User-ID", "Book-Rating", "Age", "Genre") 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        insert_data = (
            book_data["ISBN"], 
            book_data["Book_Title"], 
            book_data["Book_Author"], 
            book_data["Publisher"], 
            book_data["Year_Of_Publication"], 
            book_data["Image_URL_S"], 
            book_data["Image_URL_M"],
            book_data["User_ID"], 
            book_data["Book_Rating"], 
            book_data["Age"], 
            predicted_genre[0]
        )
        cursor.execute(insert_query, insert_data)
        postgreSQL_connection.connection.commit()

        cursor.close()

        response = {
            "status": "Success",
            "res_status": 200,
            "data": {
                "ISBN": random_string,
                "Book_Title": book_data["Book_Title"],
                "Book_Author": book_data["Book_Author"],
                "Publisher": book_data["Publisher"],
                "Year_Of_Publication": book_data["Year_Of_Publication"],
                "Image_URL_S": image_url_s_path_spaces,
                "Image_URL_M": image_url_m_path_spaces,
                "User_ID": book_data["User_ID"],
                "Book_Rating": book_data["Book_Rating"],
                "Age": book_data["Age"],
                "Genre": predicted_genre[0]
            }
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



