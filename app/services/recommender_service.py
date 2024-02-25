from fastapi import APIRouter, HTTPException, Depends, Query
from joblib import load
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import KeyedVectors
import json
from app.utils.api_utils import validate_api_key
from app.db.connection import postgreSQL_connection

router = APIRouter()

# Load saved model
model = KeyedVectors.load('./app/models/word2vec_model_recommender.joblib') # must include syn1neg.npy and wv.vectors.npy in folder models

@router.get("/v1/recommendations")
async def book_recommendations(
    title: str = Query(..., description="Book title"), 
    genre: str = Query(..., description="Book genre"),
    api_key: str = Depends(validate_api_key)
):
    try:
        # Query data from PostgreSQL
        cursor = postgreSQL_connection.get_cursor()
        cursor.execute("SELECT * FROM books ORDER BY RANDOM() LIMIT 10000;")
        data = [{key: value for key, value in zip([desc[0] for desc in cursor.description], row)} for row in cursor.fetchall()]
        cursor.close()

        def get_recommendations(title, genre, data, word2vec_model):
            # Combine title and genre into one text
            text = title + ' ' + genre
            
            # Tokenize text
            tokens = text.lower().split()
            
            # Get average vector for tokens
            vectors = [word2vec_model.wv[token] for token in tokens if token in word2vec_model.wv]
            if len(vectors) == 0:
                return None
            
            avg_vector = sum(vectors) / len(vectors)
            
            # Calculate cosine similarity with all other books
            similarities = []
            recommended_titles = set()  # Set to store titles of recommended books
            for book in data:
                other_vectors = [word2vec_model.wv[token] for token in book['Book-Title'].split() if token in word2vec_model.wv]
                if len(other_vectors) > 0:
                    other_avg_vector = sum(other_vectors) / len(other_vectors)
                    similarity = cosine_similarity([avg_vector], [other_avg_vector])[0][0]
                    similarities.append((book, similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top 10 unique recommendations
            recommendations = []
            for book, sim in similarities:
                if book['Book-Title'] not in recommended_titles and book['Book-Rating'] > 5:
                    recommendations.append(book)
                    recommended_titles.add(book['Book-Title'])
                if len(recommendations) >= 10:
                    break
            
            return {
                "status": "Success",
                "res_status": 200,
                "total": len(recommendations),
                "data": recommendations
            }

        return get_recommendations(title, genre, data, model)

    except Exception as e:
        cursor.execute("ROLLBACK;")
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))
