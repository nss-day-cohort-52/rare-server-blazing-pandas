import sqlite3
import json
from models import Category

def get_all_categories():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        """)

        # Initialize an empty list to hold all category representations
        categories = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
    for row in dataset:

        # Create a category instance from the current row
        category = Category(row['id'], row['label'])

        # Add the dictionary representation of the category to the list
        categories.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)