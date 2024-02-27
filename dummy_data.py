import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

PUBLIC_URL_POSTGRE = os.getenv("PUBLIC_URL_POSTGRE")

# Store Data default to DB
dummy = {'ISBN': ['04410072YY', '04L10071XZ', '44410072LN', '84S100F252', '044KK07259', '0441Z072J7', '0441XV7L52', '74410072ZZ', '044FX0725Q', 'AT4100725V', '0G4FXZ425Q', '2X4FZ072UQ', '2X4FZ072UW', 'QV4FZ072N9', 'QV4FZ072D5'],
        'Book-Title': ['The Angel Sword', 'Love Me', 'Save Me', 'Aurora', 'The Litle Mermaid', 'Art of Legend', 'Samurai X', 'Kungfu Panda', 'My Journey in Toronto', 'Electric', 'Space Earth', 'Econometrics', 'The Stone', 'Barbie', 'James Cook'],
        'Book-Author': ['Fery', 'John Legend', 'Bryan Jole', 'Fery', 'Nicholas Cage', 'Fery', 'Clarissa', 'Fery', 'Petra Shawn', 'Fery', 'Leo Smith', 'Fery', 'Michelle Autsin', 'Said', 'Francisca Laurent'],
        'Year-Of-Publication': [2010, 2005, 2002, 2011, 2010, 2008, 2015, 2011, 2009, 2015, 2013, 2008, 2004, 2016, 2012],
        'Publisher': ['Erlangga', 'Publisher', 'Erlangga', 'Erlangga', 'Erlangga', 'Publisher', 'Publisher', 'Erlangga', 'Panorama Book', 'Erlangga', 'Panorama Book', 'Panorama Book', 'Publisher', 'Erlangga', 'Erlangga'],
        'Image-URL-S': [
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg',
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg',
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg',
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg'
        ],
        'Image-URL-M': [
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg', 
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg',
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg',
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg',
            'https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg'
        ],
        'User-ID': [123, 2554, 3254, 4155, 5345, 33763, 7260, 84665, 9332, 10331, 28911, 2091, 212, 8182, 937],
        'Book-Rating': [8, 6, 3, 2, 2, 5, 7, 10, 3, 10, 10, 7, 4, 7, 9],
        'Age': [20, 32, 40, 47, 60, 25, 35, 45, 28, 50, 29, 43, 34, 26, 30],
        'Genre': [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    }

df = pd.DataFrame(dummy)

# Connect to PostgreSQL
engine = create_engine(PUBLIC_URL_POSTGRE) # Public network connection string

# Save data to PostgreSQL
df.to_sql('books', engine, if_exists='append', index=False)

# Run python dummy_data.py in active venv terminal
# ========================================= #
print("Successed store dataFrame to PostgreSQL.")
