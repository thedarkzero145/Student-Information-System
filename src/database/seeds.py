courses = (
    ('BSIT',),
    ('BSCS',),
    ('BSHM',),
    ('BSED',),
    ('BSBA',)
)


admin = [('admin', 'Admin@Admin123')]
student = [('25-0000', "Cleven", "Castillo", 'Demo@Cleven12!', 1)]
subjects = [('Introduction to Intermediate Programming', 'CC3', 'John Christian Lorr', 1, 0.00, 3)]


def pre_seed_db(conn):
    print("Seeding Started...")
    try:
        print("Seeding..")
        with conn:
            # courses
            cursor = conn.cursor()
            query = """
                INSERT OR IGNORE  INTO COURSES (course_name) VALUES (?)
            """
            cursor.executemany(query, courses)
            conn.commit()

            # admin
            query = """
                        INSERT  OR IGNORE  INTO ADMIN (username, password) VALUES (?, ?)
                    """
            cursor.executemany(query, admin)
            conn.commit()

            # students
            query = """
                INSERT  OR IGNORE  INTO STUDENTS(student_id, first_name, last_name, password, course_id ) VALUES (?, ?, ?, ?, ?)
            """
            cursor.executemany(query, student)
            conn.commit()

            #  subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            #  subject_name TEXT NOT NULL,
            #  subject_code TEXT NOT NULL,
            #  teacher TEXT NOT NULL,
            #  course_id TEXT NOT NULL
            #  gwa REAL,
            #  units REAL,

            # subjects
            query = """
                INSERT  OR IGNORE  INTO SUBJECTS(subject_name, subject_code, teacher, course_id, gwa, units) VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.executemany(query, subjects)
            conn.commit()
    finally:
        print("Seeding Sucessfully.")