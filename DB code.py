
import sqlite3
import os


# DATABASE PATH

DB_FILE = r"C:\Users\jvang\OneDrive\Documents\StudentSystem DB.db"



# CONNECT DATABASE

def connect_db():
    if not os.path.exists(DB_FILE):
        print("Database file not found!")
        return None

    return sqlite3.connect(DB_FILE)



# CREATE

def add_student():
    conn = connect_db()

    if conn is None:
        return

    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    section = input("Enter Section: ")
    student_id = input("Enter ID: ")
    course = input("Enter Course: ")

    query = """
    INSERT INTO STUDENTS (USERNAME, PASSWORD, SECTION, ID, COURSE)
    VALUES (?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(query, (
            username,
            password,
            section,
            student_id,
            course
        ))

        conn.commit()
        print("Student added successfully!")

    except sqlite3.Error as e:
        print("Error:", e)

    conn.close()



# READ

def show_students():
    conn = connect_db()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM STUDENTS")

        rows = cursor.fetchall()

        print("\n===== STUDENT LIST =====")

        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print("Error:", e)

    conn.close()



# UPDATE

def update_student():
    conn = connect_db()

    if conn is None:
        return

    cursor = conn.cursor()

    student_id = input("Enter Student ID to Update: ")

    new_username = input("New Username: ")
    new_password = input("New Password: ")
    new_section = input("New Section: ")
    new_course = input("New Course: ")

    query = """
    UPDATE STUDENTS
    SET USERNAME = ?,
        PASSWORD = ?,
        SECTION = ?,
        COURSE = ?
    WHERE ID = ?
    """

    try:
        cursor.execute(query, (
            new_username,
            new_password,
            new_section,
            new_course,
            student_id
        ))

        conn.commit()

        if cursor.rowcount > 0:
            print("Student updated successfully!")
        else:
            print("Student ID not found!")

    except sqlite3.Error as e:
        print("Error:", e)

    conn.close()



# DELETE

def delete_student():
    conn = connect_db()

    if conn is None:
        return

    cursor = conn.cursor()

    student_id = input("Enter Student ID to Delete: ")

    query = "DELETE FROM STUDENTS WHERE ID = ?"

    try:
        cursor.execute(query, (student_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student ID not found!")

    except sqlite3.Error as e:
        print("Error:", e)

    conn.close()



# MAIN MENU

while True:
    print("\n===== STUDENT SYSTEM =====")
    print("1. Add Student")
    print("2. Show Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        show_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("Program Closed.")
        break

    else:
        print("Invalid Choice!")