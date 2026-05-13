import sqlite3

# CREATE
def add_student(conn, student_data):
    try:
        with conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO STUDENTS (student_id, first_name, last_name, password, course_id) VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, student_data)
            conn.commit()
    except sqlite3.IntegrityError:
        # Specifically catch duplicate IDs
        print(f"Error: Student ID '{student_data[0]}' already exists!")
        return False
    except sqlite3.Error as e:
        print("Error:", e)

def search_student(conn, student_id):
    try:
        with conn:
            cursor = conn.cursor()

            if student_id:
                query = """
                    SELECT * FROM STUDENTS
                """
                cursor.execute(query)
                result = cursor.fetchall()

                return result
            else:
                query = """
                    SELECT * FROM STUDENTS WHERE student_id = ?
                """
                cursor.execute(query, (student_id,))
                result = cursor.fetchone()

                return result
    except sqlite3.Error as e:
        print("Error:", e)

def update_student(conn, student_id, data: dict):
    try:
        with conn:
            cursor = conn.cursor()

            # builds only the fields you pass in!
            fields = ", ".join([f"{key} = ?" for key in data.keys()])
            values = list(data.values())
            values.append(student_id)

            query = f"""
                    UPDATE STUDENTS
                    SET {fields}
                    WHERE student_id = ?
                """
            cursor.execute(query, values)
            conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)

def delete_student(conn, student_id):
    try:
        with conn:
            cursor = conn.cursor()

            query = """
                DELETE FROM STUDENTS
                WHERE student_id = ?
            """
            cursor.execute(query, (student_id,))
            conn.commit()
    except sqlite3.Error as e:
        print("Error:", e)