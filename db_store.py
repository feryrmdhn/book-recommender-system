import pandas as pd
from sqlalchemy import create_engine
import os

load_dotenv()

PUBLIC_URL_POSTGRE = os.environ.get("PUBLIC_URL_POSTGRE")

# Store Data default to DB
df = pd.read_csv('./app/assets/book_with_genre.csv')

# Connect to PostgreSQL
engine = create_engine(PUBLIC_URL_POSTGRE) # Public network connection string

# Save data to PostgreSQL
df.to_sql('books', engine, if_exists='replace', index=False)

# Run python db_store.py in active venv terminal
# ========================================= #
print("Successed store data to PostgreSQL.")
