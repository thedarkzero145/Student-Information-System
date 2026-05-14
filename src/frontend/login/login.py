import os
import re
import tkinter as tk
from PIL import Image, ImageTk
from ttkbootstrap import Frame, Label, Button, Entry, Checkbutton, Toplevel
from ttkbootstrap.constants import LEFT, DARK

from constants import FONT_DEFAULT_NAME, CUSTOM_BACKGROUND_COLOR, CUSTOM_BACKGROUND_NAME, CUSTOM_LABEL_NAME
from icon_utils import apply_window_icon

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
        print("clicked")
        username = user_input.get()
        password = password_input.get()

        is_user_validate = user_validation(username)
        is_password_validate = pass_validation(password)

        if not is_user_validate or not is_password_validate:
            return

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            if on_success:
                on_success(win)


    # ── Window ────────────────────────────────────────────────────────────────

    win = Toplevel(window)
    win.title("Login")
    win.geometry("1000x600")
    win.resizable(False, False)

    user_validation_func = win.register(user_validation)
    password_validation_func = win.register(pass_validation)

    apply_window_icon(win, calling_file=__file__)

    # ── LEFT PANEL (navy blue) — use ttkbootstrap styled Frame ────────────────

    left_frame = Frame(win, style=CUSTOM_BACKGROUND_NAME)
    left_frame.place(relx=0, rely=0, relwidth=0.45, relheight=1.0)

    left_center = Frame(left_frame, style=CUSTOM_BACKGROUND_NAME)
    left_center.place(relx=0.5, rely=0.5, anchor="center")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(BASE_DIR, "..", "..", "..", "assets")

    logo_path = os.path.join(assets_dir, "edu-icon.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(assets_dir, "edu1.png")

    pil_logo = Image.open(logo_path).resize((240, 240), Image.LANCZOS)
    tk_logo = ImageTk.PhotoImage(pil_logo)

    logo_img_label = Label(left_center, image=tk_logo, style=CUSTOM_LABEL_NAME)
    logo_img_label.image = tk_logo
    logo_img_label.pack(pady=(0, 14))

    Label(
        left_center,
        text="ENCHONG DEE UNIVERSITY",
        font=(FONT_DEFAULT_NAME, 22, "bold"),
        style=CUSTOM_LABEL_NAME,
        wraplength=330,
        justify="center",
        anchor="center",
    ).pack()

    Label(
        left_center,
        text="STUDENT INFORMATION SYSTEM",
        font=(FONT_DEFAULT_NAME, 10),
        style=CUSTOM_LABEL_NAME,
    ).pack(pady=(6, 0))

    # ── RIGHT PANEL (white) ───────────────────────────────────────────────────
    right_frame = Frame(win)
    right_frame.place(relx=0.45, rely=0, relwidth=0.55, relheight=1.0)

    form = Frame(right_frame)
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

    user_input = Entry(form, validate="focus", validatecommand=(user_validation_func, '%P'), font=(FONT_DEFAULT_NAME, 11))
    user_input.pack(fill="x", ipady=4, pady=(4, 8))

    user_error_label =  Label(form, font=(FONT_DEFAULT_NAME, 8), bootstyle="danger")
    user_error_label.pack(anchor="w")

    # ── Password field ────────────────────────────────────────────────────────
    tk.Label(form, text="Password", font=(FONT_DEFAULT_NAME, 11),
             fg="black", bg="white").pack(anchor="w")

    password_input = Entry(form, validate="focus", validatecommand=(password_validation_func, '%P'), show="•", font=(FONT_DEFAULT_NAME, 11))
    password_input.pack(fill="x", ipady=4, pady=(4, 8))

    password_error_label = Label(form, font=(FONT_DEFAULT_NAME, 8), bootstyle="danger")
    password_error_label.pack(anchor="w")

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

    # ── Login button — ttkbootstrap dark style ────────────────────────────────

    login_btn = Button(
        form,
        text="LOGIN",
        bootstyle=DARK,
        cursor="hand2",
        command=on_submit,
    )
    login_btn.pack(fill="x", ipady=6)

    # ── Demo hint ─────────────────────────────────────────────────────────────

    tk.Label(
        form,
        text=f"Demo — user: {DEMO_USERNAME}  |  pass: {DEMO_PASSWORD}",
        font=(FONT_DEFAULT_NAME, 8),
        fg="#aaaaaa",
        bg="white",
    ).pack(pady=(10, 0))
