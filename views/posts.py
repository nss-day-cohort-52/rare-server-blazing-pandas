import sqlite3
import json
from models import Post


def get_all_posts():
    with sqlite3.connect(".db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            p.id,
            p.title,
            p.author,
            p.category,
            p.date 
        FROM Post p
        """)
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['title'], row['author'], row['category'], row['date'])
            posts.append(post.__dict__)
    return json.dumps(posts)

def get_single_post(id):
    with sqlite3.connect(".db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            p.id,
            p.title,
            p.author,
            p.category,
            p.date 
        FROM Post p
        WHERE p.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        post = Post(data['id'], data['title'], data['author'], data['category'], data['date'])
        return json.dumps(post.__dict__)