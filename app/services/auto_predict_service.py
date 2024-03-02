from fastapi import HTTPException, Depends
from app.utils.api_utils import validate_api_key
from joblib import load
import psycopg2
import os

print("Current working directory:", os.getcwd())

# Adjust the import path based on the current working directory
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.connection import postgreSQL_connection

# Load classifier model
classifier_model_path = "./app/models/best_nb_classifier.joblib"
classifier_model = load(classifier_model_path)

# Load TF-IDF vectorizer
vectorizer_path = "./app/models/tfidf_vectorizer.joblib"
vectorizer = load(vectorizer_path)

def predict_genre(api_key: str = Depends(validate_api_key)):
    cursor = None

    try:
        cursor = postgreSQL_connection.get_cursor()
        
        # Select and lock the first 3 rows with NULL Genre
        query = """SELECT "ISBN", "Book-Title", "Book-Author", "Publisher", "Year-Of-Publication", "Image-URL-S", "Image-URL-M", "User-ID", "Book-Rating", "Age"
                   FROM books
                   WHERE "Genre" IS NULL
                   ORDER BY "ISBN"
                   FOR UPDATE
                   LIMIT 3;"""
        cursor.execute(query)
        data = cursor.fetchall()
        
        # Predict genre for each data
        predictions = []
        for row in data:
            book_title = row[1]
            title_features = vectorizer.transform([book_title])
            input_features = title_features
            predicted_genre = classifier_model.predict(input_features)[0]
            predictions.append({
                "ISBN": row[0],
                "Book_Title": book_title,
                "Book_Author": row[2],
                "Publisher": row[3],
                "Year_Of_Publication": row[4],
                "Image_URL_S": row[5],
                "Image_URL_M": row[6],
                "User_ID": row[7],
                "Book_Rating": row[8],
                "Age": row[9],
                "Predicted_Genre": predicted_genre
            })
        
        # Update the first 3 rows with predicted Genre
        for pred in predictions:
            update_query = """UPDATE books
                              SET "Genre" = %s
                              WHERE "ISBN" = %s;"""
            update_data = (pred["Predicted_Genre"], pred["ISBN"])
            cursor.execute(update_query, update_data)
            postgreSQL_connection.connection.commit()

        cursor.close()

        response = {
            "status": "Success",
            "res_status": 200,
            "data": predictions
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run function
if __name__ == "__main__":
    predict_genre()
