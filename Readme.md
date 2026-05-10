
# Student Information System (SIS)

CC3 **Intermediate Programming** — Final Project

This repository contains a work-in-progress **Student Information System (SIS)** desktop application written in **Python** using **Tkinter/ttkbootstrap** for the UI.

The current implementation focuses on the initial **Login screen UI** and project scaffolding (frontend/backend separation). Additional SIS functionality (student records, searching, CRUD operations, persistence, etc.) is intended to be added as the project evolves.

---

## Table of contents

- [Project goals](#project-goals)
- [Current status](#current-status)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [How to run](#how-to-run)
- [How the app is organized](#how-the-app-is-organized)
- [Troubleshooting](#troubleshooting)
- [Roadmap (planned features)](#roadmap-planned-features)

---

## Project goals

As a CC3 Intermediate Programming final project, this app aims to demonstrate:

- **Modular project structure** (separating UI/logic/data concerns)
- **GUI development** (layout, theming, reusable views)
- **Basic application architecture** (an entry point that launches screens)
- **Input validation and user flow** (login, navigation, and error handling)
- **Foundations for data handling** (a backend layer that can later connect to a database/file storage)

---

## Current status

Implemented today:

- A themed desktop window using **ttkbootstrap** ("darkly" theme)
- A **Login window UI** with:
	- Left-side branding panel and logo image
	- Username + password fields
	- "Remember me" checkbox
	- Login button (UI only — login logic is not wired yet)

Not implemented yet (planned):

- Authentication logic (validating credentials)
- Student information views (list/detail)
- Data persistence (database/file)
- Backend services (actual logic beyond placeholders)

---

## Tech stack

- **Python** (tested with Python 3.11+)
- **Tkinter** (bundled with most Python installs)
- **ttkbootstrap** (modern themed widgets)

---

## Project structure

High-level layout:

```
Student-Information-System/
├─ Readme.md
└─ src/
	 ├─ main.py
	 ├─ backend/
	 │  └─ backend.py
	 └─ frontend/
			└─ login/
				 ├─ login.py
				 └─ assets/
						└─ plv-logo.png
```

What each part is for:

- `src/main.py`
	- App entry point.
	- Creates the root window, applies the theme, and opens the login UI.

- `src/frontend/login/login.py`
	- Defines `open_login_window(...)` which builds the login screen using ttkbootstrap widgets.
	- Loads the logo image from `src/frontend/login/assets/plv-logo.png`.

- `src/backend/backend.py`
	- Placeholder for backend logic (e.g., authentication, student record operations).
	- This file is intended to evolve as you add data access and business rules.

---

## How to run

### 1) Prerequisites

- Windows 10/11 (recommended for this project)
- Python **3.11+** installed
- `pip` available in your PATH

To confirm Python:

```bash
python --version
```

### 2) (Recommended) Create and activate a virtual environment

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3) Install dependencies

This project currently depends on `ttkbootstrap`:

```bash
pip install ttkbootstrap
```

### 4) Start the application

From the repository root, run the module entry point:

```bash
python -m src.main
```

This should open a login window.

---

## How the app is organized

### Startup flow

1. `src/main.py` creates the root `Window` and hides it (`withdraw`) so only the login UI is visible.
2. `open_login_window(root)` is called.
3. `open_login_window` creates a `Toplevel` window and builds the login layout.
4. The Tk event loop starts via `window.mainloop()`.

### UI notes

- The login screen uses a two-column layout:
	- Left: a fixed-width dark panel with branding and an image.
	- Right: the login form centered in the remaining space.

- Logo path:
	- `login.py` computes a `BASE_DIR` from its own file location and loads:
		`assets/plv-logo.png`
	- If you rename or move the image, update the path accordingly.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'ttkbootstrap'"

Install the dependency:

```bash
pip install ttkbootstrap
```

If you are using a virtual environment, ensure it is activated before running.

### The app doesn’t open or closes immediately

- Make sure you are running from the repository root using:

```bash
python -m src.main
```

- If you run `python src/main.py` directly, Python’s import paths may differ depending on your environment.

### "TclError" / Tkinter issues

Tkinter is usually bundled with Python on Windows. If you have a minimal Python install without Tk support, reinstall Python and ensure **tcl/tk** components are included.

---

## Roadmap (planned features)

These are reasonable next steps for a Student Information System project:

1. **Authentication**
	 - Validate username/password
	 - Display inline errors (using the existing error label widgets)
	 - Implement "Remember me" behavior (local config file)

2. **Student records**
	 - Student list view (search/sort)
	 - Student detail view
	 - Add/edit/delete student records

3. **Data persistence**
	 - Start simple with JSON/CSV
	 - Upgrade to SQLite for structured storage

4. **Backend layer**
	 - Move validation and data operations into `src/backend/`
	 - Keep the frontend focused on UI rendering and events

---

## Notes for submission

If this project is being submitted for CC3 Intermediate Programming, consider including:

- Short screen recording or screenshots of the running app
- A short write-up describing:
	- Architecture decisions
	- Planned features
	- Known limitations
	- How to run and test

