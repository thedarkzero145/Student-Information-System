import sqlite3
from datetime import datetime, date

#create a new event with date and time
def add_event(conn,title, date, description=""):
    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO events (Title, description) VALUES (?, ?)",
            ("Event", datetime.now()))

        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print("Error:", e)
# list for searching events
def search_event(conn, search_term="", date_filter=None):
    try:
        with conn:
            cursor = conn.cursor()
            event = "SELECT * FROM events WHERE 1=1"
            params = []

            if search_term:
                event += "AND (title LIKE ? OR description LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            if date_filter:
                event += "AND date = ?"
                params.append(date_filter)

            event += "ORDER BY date ASC"

            cursor.execute(event, params)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error:", e)
        return []

def update_event(conn, event_id, title=None, description=None):
    try:
        cursor = conn.cursor()
        updates = []
        params = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if not updates:
            return False
        event = "UPDATE events SET title = ?, description = ? WHERE id = ?"
        params.append(event_id)

        cursor.execute(event, params)
        conn.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as e:
        print("Error:", e)
        return False

def delete_event(conn, event_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print("Error:", e)
        return False
