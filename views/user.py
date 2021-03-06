import sqlite3
import json
from datetime import datetime
from models import User

def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, profile_image_url, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['profile_image'],
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })
        
def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM users u
        ORDER BY username
        """)

        # Initialize an empty list to hold all user representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
    for row in dataset:

        # Create a user instance from the current row
        user = User(row['id'], row['first_name'],row['last_name'],
                    row['email'],row['bio'],row['username'],
                    row['password'],row['profile_image_url'],
                    row['created_on'],row['active'])

        # Add the dictionary representation of the user to the list
        users.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)

def get_single_user(id):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on
        FROM users u
        WHERE u.id = ?
        """, (id,))

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        user = {
                "id": data['id'], 
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "bio": data['bio'],
                "username": data['username'],
                "image_url":data['profile_image_url'],
                "created_on": data['created_on']
                }

    # Use `json` package to properly serialize list as JSON
    return json.dumps(user)
