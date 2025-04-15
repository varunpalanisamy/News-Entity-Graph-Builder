import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def insert_article(cursor, title, date, content, url):
    cursor.execute(
        "INSERT INTO articles (title, date, content, url) VALUES (%s, %s, %s, %s) RETURNING id",
        (title, date, content, url)
    )
    return cursor.fetchone()[0]

def insert_entity(cursor, article_id, entity, label):
    cursor.execute(
        "INSERT INTO entities (article_id, entity, label) VALUES (%s, %s, %s)",
        (article_id, entity, label)
    )

def insert_relationship(cursor, article_id, entity_1, relationship, entity_2):
    cursor.execute(
        "INSERT INTO relationships (article_id, entity_1, relationship, entity_2) VALUES (%s, %s, %s, %s)",
        (article_id, entity_1, relationship, entity_2)
    )
