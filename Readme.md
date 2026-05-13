# Enchong Dee University Student Information System

A desktop application for managing student academic records. Built as a CC3 Intermediate Programming Final Project.

This system is for universities that need a simple way for students to view their grades, schedule, and announcements, and for administrators to manage student data, subjects, events, and reports.

---

## Features

### Login System

- Separate login flow for students and administrators.
- Input validation shows inline error messages before submission.
- After login, users are sent to the correct dashboard for their role.

### Student Dashboard

- Shows your name, student ID, and program at the top.
- View your classes for the day on a schedule timeline.
- See your current grade average, attendance, and credits earned.
- Tabs for Grades, Subjects, Announcements, Events, and Settings.

### Admin Dashboard

- Overview cards showing total students, active students, and inactive students.
- A full students table with search and filter by course, year level, and status.
- Add, edit, and remove student records.
- Manage subjects, campus events, and announcements.
- Generate and export a system report as a PDF from the Reports tab.
- Department load breakdown with visual progress bars.
- System settings for academic year and semester configuration.

---

## How to Run

**Step 1. Check that Python 3.11 or newer is installed.**

```bash
python --version
```

If the output shows a version below 3.11, download the latest Python from https://python.org before continuing.

**Step 2. Open a terminal in the project root folder.** This is the folder that contains `src/` and `assets/`. If you are inside `src/`, go one level up.

**Step 3. Install the required packages.**

```bash
pip install ttkbootstrap pillow fpdf
```

**Step 4. Run the application.**

```bash
python src/main.py
```

The login window will appear in the center of your screen.

---

## Login Credentials

> [!WARNING]
> The credentials below are for development and testing only. They will be removed before the final release.

| Role | Username | Password |
|---|---|---|
| Admin | `1` | `1` |
| Student | `2` | `2` |

---

## Project Structure

```
Student-Information-System/
  assets/           # Icons and images used by the app
  src/
    main.py         # Entry point. Run this file to start the app.
    constants.py    # Shared color and font constants
    icon_utils.py   # Window icon helper
    frontend/
      login/
        login.py    # Login screen
      dashboard/
        dashboard.py            # Student dashboard
        admin_dashboard.py      # Admin dashboard and navigation
        admin_dashboard_home.py # Admin overview with charts
        admin_subjects.py       # Subject list and add form
        admin_events.py         # Events list and add form
        admin_announcements.py  # Announcements list and add form
        settings.py             # Settings tab (student)
        grade.py                # Grades tab
        subjects.py             # Subjects tab
        announcements.py        # Announcements tab
        events.py               # Events tab
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'ttkbootstrap'`**

You skipped Step 3. Run the install command and try again.

```bash
pip install ttkbootstrap pillow fpdf
```

**`ModuleNotFoundError: No module named 'constants'`**

You are running the app from inside the `src/` folder. Go back to the project root and run it as `python src/main.py`, not `python main.py`.

**The app closes immediately after opening**

Same as above. Make sure your terminal is in the project root, not inside `src/`.

**Icons are not showing**

The `assets/` folder must be present in the project root. If you deleted or moved it, the app will still run but icons will fall back to text characters. Restore the folder from the repository.

**`pip` is not recognized**

On some Windows installs, you need to use the full Python path:

```bash
C:/Users/YourName/AppData/Local/Programs/Python/Python311/python.exe -m pip install ttkbootstrap pillow fpdf
```

Replace `YourName` with your Windows username.

**The PDF export button does nothing**

Make sure `fpdf` is installed. Run `pip install fpdf` and restart the app.

---

## Project Info

CC3 Intermediate Programming Final Project, AY 2025-2026.
