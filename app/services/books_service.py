from fastapi import APIRouter, HTTPException, Query, Depends
from app.utils.api_utils import validate_api_key
from app.db.connection import postgreSQL_connection

router = APIRouter()

@router.get("/v1/books")
async def get_books(genre: str = Query(None, alias="genre"), api_key: str = Depends(validate_api_key)):
    try:
        cursor = postgreSQL_connection.get_cursor()

        # Query data from PostgreSQL
        if not genre:
            cursor.execute("SELECT * FROM books ORDER BY RANDOM() LIMIT 100;")
        else:
            cursor.execute("SELECT * FROM books WHERE \"Genre\" ILIKE %s LIMIT 100;", (f"%{genre}%",))

        data = [{key: value for key, value in zip([desc[0] for desc in cursor.description], row)} for row in cursor.fetchall()]

        cursor.close()

        return {
            "status": "Success",
            "res_status": 200,
            "total": len(data),
            "data": data
        }

    except Exception as e:
        cursor.execute("ROLLBACK;")
        cursor.close()
        raise HTTPException(status_code=500, detail=str(e))