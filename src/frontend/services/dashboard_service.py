import os
from dotenv import load_dotenv

load_dotenv()

class DashboardService:
    def __init__(self):
        self.mock_mode = True #Change to False when we implement the database

    def get_campus_stats(self):
        if not self.mock_mode:
            # SQL: SELECT name, subtitle FROM campus_info LIMIT 1
            pass
        return {
            "name": os.getenv("CAMPUS_NAME", ""),
            "subtitle": os.getenv("CAMPUS_SUBTITLE", "")
        }

    def get_student_stats(self):
        if not self.mock_mode:
            # SQL: SELECT total, active, inactive FROM student_stats
            pass
        return {
            "total": os.getenv("ADMIN_TOTAL_STUDENTS", "0"),
            "active": os.getenv("ADMIN_ACTIVE_STUDENTS", "0"),
            "inactive": os.getenv("ADMIN_INACTIVE_STUDENTS", "0")
        }

    def get_recent_enrollments(self):
        if not self.mock_mode:
            # SQL: SELECT id, name, course, year FROM students ORDER BY enrolled_date DESC LIMIT 10
            pass
        students = []
        for i in range(1, 11):
            env_key = f"STUDENT_TABLE_{i}"
            env_val = os.getenv(env_key, "")
            if not env_val: continue
            parts = env_val.split("|")
            if len(parts) == 4:
                students.append(tuple(parts))
        return students

    def get_department_load(self):
        if not self.mock_mode:
            # SQL: SELECT dept_name, count FROM departments
            pass
        return {
            "total": int(os.getenv("ADMIN_TOTAL_FOR_DEPTS", "0").replace(",", "")),
            "departments": [
                {
                    "name": os.getenv("ADMIN_DEPT_NAME_1", ""),
                    "count": int(os.getenv("ADMIN_DEPT_STEM", "0").replace(",", ""))
                },
                {
                    "name": os.getenv("ADMIN_DEPT_NAME_2", ""),
                    "count": int(os.getenv("ADMIN_DEPT_MEDICAL", "0").replace(",", ""))
                },
                {
                    "name": os.getenv("ADMIN_DEPT_NAME_3", ""),
                    "count": int(os.getenv("ADMIN_DEPT_LIBERAL", "0").replace(",", ""))
                }
            ]
        }

    def get_student_profile(self):
        if not self.mock_mode:
            # SQL: SELECT name, program, id, grade, credits FROM students WHERE id = ?
            pass
        return {
            "name": os.getenv("STUDENT_NAME", ""),
            "program": os.getenv("STUDENT_PROGRAM", ""),
            "id": os.getenv("STUDENT_ID", ""),
            "grade": os.getenv("STUDENT_GRADE", ""),
            "credits": os.getenv("STUDENT_CREDITS", "")
        }

    def get_report_data(self):
        if not self.mock_mode:
            # SQL: SELECT * FROM report_stats
            pass
        return {
            "total_students": os.getenv("ADMIN_TOTAL_STUDENTS", "0"),
            "active_students": os.getenv("ADMIN_ACTIVE_STUDENTS", "0"),
            "inactive_students": os.getenv("ADMIN_INACTIVE_STUDENTS", "0"),
            "recent_enrollments": self.get_recent_enrollments()
        }
