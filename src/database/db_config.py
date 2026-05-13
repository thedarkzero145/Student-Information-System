import sqlite3
import os
from typing import IO

from database.seeds import pre_seed_db

# DATABASE PATH

def find_db_filepath(path_name: str) -> str:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    DATABASE_FILE_PATH = os.path.join(CURRENT_DIR, "..", "database", path_name)

    return DATABASE_FILE_PATH


# CONNECT DATABASE
def connect_db():
    db_file_path = find_db_filepath("StudentInformationDB.db")

    if not db_file_path:
        print("No database found, creating new one...")

    conn = sqlite3.connect(db_file_path)
    conn.execute("PRAGMA foreign_keys = ON")
    create_tables(conn)
    pre_seed_db(conn)
    return conn

def create_tables(conn):
    cursor = conn.cursor()

    # ===== ADMIN TABLE =====
    cursor.execute("""
                      CREATE TABLE IF NOT EXISTS ADMIN(
                          admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT NOT NULL,
                          password TEXT NOT NULL
                      )
                      """
                   )

    # ==== COURSE TABLE ====
    cursor.execute("""
                          CREATE TABLE IF NOT EXISTS COURSES(
                              course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              course_name TEXT NOT NULL
                          )
                          """
                   )

    # ==== STUDENTS TABLE ====
    cursor.execute("""
                       CREATE TABLE IF NOT EXISTS STUDENTS(
                           student_id TEXT PRIMARY KEY NOT NULL,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL,
                           password TEXT NOT NULL,
                           course_id INTEGER NOT NULL,
                           
                           FOREIGN KEY (course_id) REFERENCES COURSES(course_id)
                       )
                       """
                   )

    # ==== SUBJECTS TABLE ====
    cursor.execute("""
                       CREATE TABLE IF NOT EXISTS SUBJECTS(
                           subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           subject_name TEXT NOT NULL,
                           subject_code TEXT NOT NULL,
                           teacher TEXT NOT NULL,
                           course_id TEXT NOT NULL,
                           gwa REAL,
                           units REAL,
                           
                           FOREIGN KEY (course_id) REFERENCES COURSES(course_id)
                       )
                       """
                   )

    conn.commit()
