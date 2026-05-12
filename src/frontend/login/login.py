import os
import re
import tkinter as tk
from PIL import Image, ImageTk
from ttkbootstrap.constants import LEFT

from constants import FONT_DEFAULT_NAME, CUSTOM_BACKGROUND_COLOR, CUSTOM_BACKGROUND_NAME

DEMO_USERNAME = "25-0000"
DEMO_PASSWORD = "Demo@Admin12!"


def open_login_window(window, on_success=None):

    # ── Validation ────────────────────────────────────────────────────────────

    def user_validation(user):
        pattern = r"^25-\d{4}$"
        if re.fullmatch(pattern, user):
            user_error_label.config(text="")
            return True
        else:
            user_error_label.config(text="Username must start at 25- ex. [25-2751]")
            return False

    def pass_validation(password):
        if len(password) < 12:
            password_error_label.config(text="Password must have at least 12 characters!")
            return False
        if not any(c.isupper() for c in password):
            password_error_label.config(text="Password must have at least 1 uppercase letter!")
            return False
        if not any(c.islower() for c in password):
            password_error_label.config(text="Password must have at least 1 lowercase letter!")
            return False
        if not any(c.isdigit() for c in password):
            password_error_label.config(text="Password must have at least 1 number!")
            return False
        if not any(c in {"!", "@", "#", "$", "%", "^", "&", "*"} for c in password):
            password_error_label.config(text="Password must have at least 1 symbol (! @ # $ % ^ & *)")
            return False
        password_error_label.config(text="")
        return True

    def on_submit():
        username = user_input.get()
        password = password_input.get()

        if not user_validation(username) or not pass_validation(password):
            return

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            auth_error_label.config(text="")
            if on_success:
                on_success(win)
        else:
            auth_error_label.config(text="Invalid username or password.")

    # ── Window ────────────────────────────────────────────────────────────────

    win = tk.Toplevel(window)
    win.title("Login")
    win.geometry("1000x600")
    win.configure(bg=CUSTOM_BACKGROUND_COLOR)
    win.resizable(False, False)

    # ── LEFT PANEL (navy blue) ────────────────────────────────────────────────

    left_frame = tk.Frame(win, bg=CUSTOM_BACKGROUND_COLOR)
    left_frame.place(relx=0, rely=0, relwidth=0.45, relheight=1.0)

    left_center = tk.Frame(left_frame, bg=CUSTOM_BACKGROUND_COLOR)
    left_center.place(relx=0.5, rely=0.5, anchor="center")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(BASE_DIR, "..", "..", "..", "assets")

    logo_path = os.path.join(assets_dir, "login-logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(assets_dir, "edu1.png")

    pil_logo = Image.open(logo_path).resize((260, 260), Image.LANCZOS)
    tk_logo = ImageTk.PhotoImage(pil_logo)

    logo_img_label = tk.Label(left_center, image=tk_logo, bg=CUSTOM_BACKGROUND_COLOR)
    logo_img_label.image = tk_logo
    logo_img_label.pack(pady=(0, 14))

    tk.Label(
        left_center,
        text="ENCHONG DEE UNIVERSITY",
        font=(FONT_DEFAULT_NAME, 22, "bold"),
        fg="white",
        bg=CUSTOM_BACKGROUND_COLOR,
        wraplength=330,
        justify="center",
    ).pack()

    tk.Label(
        left_center,
        text="STUDENT INFORMATION SYSTEM",
        font=(FONT_DEFAULT_NAME, 10),
        fg="white",
        bg=CUSTOM_BACKGROUND_COLOR,
    ).pack(pady=(6, 0))

    # ── RIGHT PANEL (white card) ──────────────────────────────────────────────

    right_frame = tk.Frame(win, bg="white")
    right_frame.place(relx=0.45, rely=0, relwidth=0.55, relheight=1.0)

    form = tk.Frame(right_frame, bg="white")
    form.place(relx=0.5, rely=0.5, anchor="center", width=340)

    # Welcome heading
    tk.Label(
        form,
        text="Welcome!",
        font=("SF Pro", 28, "bold"),
        fg="black",
        bg="white",
    ).pack(anchor="w")

    tk.Label(
        form,
        text="Login to your Workspace",
        font=("SF Pro", 13),
        fg="#666666",
        bg="white",
    ).pack(anchor="w", pady=(2, 26))

    # ── Username field ────────────────────────────────────────────────────────

    tk.Label(form, text="Username", font=(FONT_DEFAULT_NAME, 11),
             fg="black", bg="white").pack(anchor="w")

    user_input = tk.Entry(form, font=(FONT_DEFAULT_NAME, 11),
                          bg="#f5f5f5", fg="black", relief="flat", bd=0,
                          insertbackground="black")
    user_input.pack(fill="x", ipady=10, pady=(4, 0))
    user_input.bind("<FocusOut>", lambda e: user_validation(user_input.get()))

    user_error_label = tk.Label(form, text="", font=(FONT_DEFAULT_NAME, 8),
                                fg="#dc3545", bg="white", anchor="w")
    user_error_label.pack(fill="x", pady=(2, 10))

    # ── Password field ────────────────────────────────────────────────────────

    tk.Label(form, text="Password", font=(FONT_DEFAULT_NAME, 11),
             fg="black", bg="white").pack(anchor="w")

    password_input = tk.Entry(form, show="•", font=(FONT_DEFAULT_NAME, 11),
                              bg="#f5f5f5", fg="black", relief="flat", bd=0,
                              insertbackground="black")
    password_input.pack(fill="x", ipady=10, pady=(4, 0))
    password_input.bind("<FocusOut>", lambda e: pass_validation(password_input.get()))

    password_error_label = tk.Label(form, text="", font=(FONT_DEFAULT_NAME, 8),
                                    fg="#dc3545", bg="white", anchor="w")
    password_error_label.pack(fill="x", pady=(2, 10))

    # ── Remember me ───────────────────────────────────────────────────────────

    remember_var = tk.BooleanVar()
    remember_row = tk.Frame(form, bg="white")
    remember_row.pack(anchor="w", pady=(0, 10))

    tk.Checkbutton(
        remember_row,
        variable=remember_var,
        bg="white",
        activebackground="white",
        cursor="hand2",
    ).pack(side=LEFT)

    tk.Label(
        remember_row,
        text="Remember me",
        font=(FONT_DEFAULT_NAME, 10),
        fg="black",
        bg="white",
    ).pack(side=LEFT)

    # ── Auth error (wrong credentials) ───────────────────────────────────────

    auth_error_label = tk.Label(form, text="", font=(FONT_DEFAULT_NAME, 9),
                                fg="#dc3545", bg="white", anchor="w")
    auth_error_label.pack(fill="x", pady=(0, 8))

    # ── Login button ──────────────────────────────────────────────────────────

    login_btn = tk.Button(
        form,
        text="LOGIN",
        font=(FONT_DEFAULT_NAME, 12, "bold"),
        fg="white",
        bg="black",
        activebackground="#333333",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=on_submit,
    )
    login_btn.pack(fill="x", ipady=10)

    # ── Demo hint ─────────────────────────────────────────────────────────────

    tk.Label(
        form,
        text=f"Demo — user: {DEMO_USERNAME}  |  pass: {DEMO_PASSWORD}",
        font=(FONT_DEFAULT_NAME, 8),
        fg="#aaaaaa",
        bg="white",
    ).pack(pady=(10, 0))
