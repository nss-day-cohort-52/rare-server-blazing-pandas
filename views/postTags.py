import json
import sqlite3

def create_postTag(new_postTag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO postTags
            ( post_id, tag_id )
        VALUES
            ( ?, ? );
        """, (new_postTag['post_id'],new_postTag['tag_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the postTag dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_postTag['id'] = id


    return json.dumps(new_postTag)