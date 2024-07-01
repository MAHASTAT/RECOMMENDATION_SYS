import psycopg2
import pandas as pd 


# Connection to the PostgreSQL database local
conn = psycopg2.connect(
    host="localhost",
    database="book_management",
    user="postgres",
    password="kdhjw"
)

cur = conn.cursor()

# Fetch the data from the books table in 'book_management' database
cur.execute("SELECT id, title, author, jenre, year_published, average_rating FROM books")
books = pd.DataFrame(cur.fetchall(), columns=['id', 'title', 'author', 'jenre', 'year_published', 'average_rating'])

books.head(10)

books.describe()
