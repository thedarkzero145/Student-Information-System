# Enchong Dee University — Student Information System

A desktop application built as our **CC3 Intermediate Programming Final Project**. This system was designed to give students and administrators a clean, intuitive way to manage and view student academic records.

---

## What is this?

This is a fully functional **Student Information System (SIS)** for Enchong Dee University. It supports two types of users — students and administrators — each with their own dedicated dashboard experience tailored to their role.

We built this from the ground up using Python, focusing on a clean UI, solid structure, and a smooth user experience that feels professional without being overly complicated.

---

## Features

### 🔐 Login System
- Secure login for both **students** and **administrators**
- Input validation with helpful inline error messages
- Automatically routes users to their respective dashboard based on role

### 🎓 Student Dashboard
- Personalized welcome banner with student name, program, and ID
- **Today's Schedule** — a live timeline view of the student's classes for the day
- **Motivational Quote** panel
- At-a-glance stat cards: Grade, Attendance, and Credits Earned
- Navigation tabs for Grades, Subjects, Announcements, Events, and Settings

### 🛠️ Admin Dashboard
- Overview of total, active, and inactive student counts
- Full **Students Table** — browse and search student records at a glance
- **Student Profile View** — detailed academic profile for any selected student, including major, advisor, CGPA, and credits
- Department load breakdown with visual progress bars
- Navigation tabs for adding, editing, and removing student records

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **Tkinter** | GUI framework (built into Python) |
| **ttkbootstrap** | Modern themed widget styling |
| **Pillow (PIL)** | Icon and image rendering |
| **SQLite** | Student data storage |

---

## How to Run

**1. Make sure Python 3.11+ is installed**

```bash
python --version
```

**2. Install dependencies**

```bash
pip install ttkbootstrap pillow
```

**3. Run the app from the project root**

```bash
python src/main.py
```

That's it. The login window will appear and you're good to go.

---

## Login Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin-0001` | `Admin@Pass12!` |
| Student | `25-0000` | `Demo@Admin12!` |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'ttkbootstrap'`**
Run `pip install ttkbootstrap pillow` and try again.

**The app closes immediately or doesn't open**
Make sure you're running from the project root directory: `python src/main.py`

**Icons aren't showing**
Ensure the `assets/` folder is present in the project root and contains the icon PNG files.

---

## The Team

Built with 💙 by the CC3 group for Enchong Dee University SIS — Final Project, AY 2025–2026.
