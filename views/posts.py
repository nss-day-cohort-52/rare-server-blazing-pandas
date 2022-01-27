import sqlite3
import json
from models import Post, User, Category
from models.tag import Tag


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.username users_username,
            c.label categories_label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        ORDER BY publication_date DESC
        """)

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                    row['title'], row['publication_date'],
                    row['image_url'], row['content'], row['approved'])
            user =  {"username": row['users_username']}
            category = Category(row['category_id'], row['categories_label'])
            post.user = user
            post.category = category.__dict__
            posts.append(post.__dict__)
            db_cursor.execute("""
                select t.id, t.label
                from PostTags pt
                join Tags t on t.id = pt.tag_id
                where pt.post_id = ?
                order by t.id
            """, (post.id, ))
            tags = []
            tags_dataset = db_cursor.fetchall()
            
            for tag_row in tags_dataset:
                tag = Tag(tag_row['id'], tag_row['label'])
                tags.append(tag.__dict__)
            
            post.tags = tags
    return json.dumps(posts)

def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            (?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'],
              new_post['category_id'], new_post['title'],
              new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the post dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id
    return json.dumps(new_post)

def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.username users_username,
            c.label categories_label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        JOIN Categories c
            ON c.id = p.category_id
        WHERE p.id = ?
        """, (id, ))
        
        posts = []
        data = db_cursor.fetchone()
        post = Post(data['id'], data['user_id'], data['category_id'],
                data['title'], data['publication_date'], data['image_url'],
                data['content'], data['approved'])
        user =  {"username": data['users_username']}
        category = Category(data['category_id'], data['categories_label'])
        post.user = user
        post.category = category.__dict__
        posts.append(post.__dict__)
    return json.dumps(post.__dict__)

