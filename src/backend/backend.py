from src.backend.login_state import load_login_credentials, save_login_credentials
import sqlite3

def validate_auth(conn, username: str, password: str):
    try:
        with conn:
            cursor = conn.cursor()
            query = """
                   SELECT * FROM ADMIN
                   WHERE username = ? AND password = ?
               """

            cursor.execute(query, (username, password))

            row: list = cursor.fetchone()

            if row is not None:
                return [row[0], "admin"]


            query = """
                SELECT * FROM STUDENTS
                WHERE student_id = ? AND password = ?
            """

            cursor.execute(query, (username, password))

            row: list = cursor.fetchone()

            if row is not None:
                return [row[0], "student"]

            return None

    except sqlite3.Error as e:
        print("Error:", e)


# ---- REMEMBER ME -----
def get_credentials(fields):
    data = load_login_credentials()
    if not data:
        return None

    return data.get(fields)

def save_credentials_state(username: str, password: str):
    print("Saving data...")
    save_login_credentials(username, password)
    print("Saving completed...")


