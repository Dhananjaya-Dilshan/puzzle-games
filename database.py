# database.py
import hashlib
import sqlite3

#databes connecting function
def connect_db():
    db = sqlite3.connect("banana_game.db")
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            best_time REAL DEFAULT 0,
            fruit_level INTEGER DEFAULT 0,
            animal_level INTEGER DEFAULT 0,
            vehicle_level INTEGER DEFAULT 0
        )
    """)
    db.commit()
    return db

def add_user(username, hashed_password):

    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO player (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        return "User registered successfully!"
    except sqlite3.IntegrityError:
        return "Username already exists. Please choose a different one."
    except sqlite3.Error as err:
        return f"Database Error: {err}"
    finally:
        cursor.close()
        db.close()

def verify_user(username, hashed_password):

    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM player WHERE username = ? AND password = ?", (username, hashed_password))
        result = cursor.fetchone()
        return result is not None  # Returns True if user exists, else False
    except sqlite3.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        db.close()

def get_leaderboard_data():

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT username, best_time FROM player WHERE best_time > 0 ORDER BY best_time ASC LIMIT 10")
    leaderboard_data = cursor.fetchall()
    cursor.close()
    db.close()
    return leaderboard_data


def hash_password(password):
    salt = "a_random_salt"
    return hashlib.sha256((salt + password).encode()).hexdigest()

#Get user details
def get_user_info(username):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT username, password FROM player WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result if result else (username, "")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error retrieving user info: {e}")
    finally:
        cursor.close()
        db.close()

def get_user_best_time(username):

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT best_time FROM player WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else "N/A"
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error retrieving best time: {e}")
    finally:
        cursor.close()
        db.close()

#update user details
def update_user_info(username, field_name, new_value):
    try:
        db = connect_db()
        cursor = db.cursor()
        if field_name == "password":
            new_value = hash_password(new_value)
        cursor.execute(f"UPDATE player SET {field_name} = ? WHERE username = ?", (new_value, username))
        db.commit()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error updating {field_name}: {e}")
    finally:
        cursor.close()
        db.close()

def delete_user(username):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM player WHERE username = ?", (username,))
        db.commit()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error deleting user: {e}")
    finally:
        cursor.close()
        db.close()

def get_user_level(username, category):
    connection = sqlite3.connect('banana_game.db')
    cursor = connection.cursor()
    column_name = f"{category}_level"

    cursor.execute(f"SELECT {column_name} FROM player WHERE username = ?", (username,))
    level = cursor.fetchone()
    connection.close()

    return level[0] if level else 0


def update_user_level(username, category, new_level):
    connection = sqlite3.connect('banana_game.db')
    cursor = connection.cursor()
    column_name = f"{category}_level"

    cursor.execute(f"UPDATE player SET {column_name} = ? WHERE username = ?", (new_level, username))
    connection.commit()
    connection.close()


def update_best_time(username, elapsed_time):
    connection = sqlite3.connect('banana_game.db')
    cursor = connection.cursor()

    cursor.execute("SELECT best_time FROM player WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and (result[0] is None or elapsed_time < result[0]):
        cursor.execute("UPDATE player SET best_time = ? WHERE username = ?", (elapsed_time, username))
        connection.commit()