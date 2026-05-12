from ttkbootstrap import  Frame, Toplevel, Label, Entry, Button, Checkbutton
import tkinter as tk
from constants import FONT_DEFAULT_NAME, CUSTOM_BACKGROUND_COLOR, CUSTOM_BACKGROUND_NAME
import os
import re

from ttkbootstrap.constants import LEFT


# initialize login
def open_login_window(window):
    # user validation
    def user_validation(user):
        pattern = r"^25-\d{4,4}$"
        if re.fullmatch(pattern, user):
            user_error_label.config(text="")
            return True
        else:
            user_error_label.config(text="Username must start at 25- ex. [25-2751]")  # ← show error
            return False

    # password validation
    def pass_validation(password):
        if len(password) < 12:
            password_error_label.config(text="Password must have at least 12 characters!")
            return False
        if not any(char.isupper() for char in password):
            password_error_label.config(text="Password must have at least 1 uppercase letter!")
            return False
        if not any(char.islower() for char in password):
            password_error_label.config(text="Password must have at least 1 lowercase letter!")
            return False
        if not any(char.isdigit() for char in password):
            password_error_label.config(text="Password must have at least 1 number!")
            return False
        symbol = {"!", "@", "#", "$", "%", "^", "&", "*"}
        if not any(char in symbol for char in password):
            password_error_label.config(text="Password must have at least 1 symbol (! @ # $ % ^ & *)")
            return False

        password_error_label.config(text="")
        return True

    def onSubmit():
        username = user_input.get()
        password = password_input.get()

        is_user_validation = user_validation(username)
        is_password_validation = pass_validation(password)
        if is_user_validation and is_password_validation:
            # logic here...
            print("valid inputs")
            pass

    window = Toplevel(window)
    window.title("Login")
    window.geometry("1000x600")

    # Side Frame of Login
    side_frame = Frame(window, style=CUSTOM_BACKGROUND_NAME)
    side_frame.place(relx=0, rely=0, relwidth=0.45, relheight=1.0)

    side_center_frame = Frame(side_frame, style=CUSTOM_BACKGROUND_NAME)
    side_center_frame.pack(expand=True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    bg_logo = tk.PhotoImage(file=os.path.join(BASE_DIR, "assets", "edu1.png"))

    bg_label_image =  Label(side_center_frame, image=bg_logo, style="BG_LABEL.TLabel")
    bg_label_image.image = bg_logo

    bg_label_image.pack(expand=True)


    (Label(side_center_frame,
          text="ENCHONG DEE UNIVERSITY",
          font=(FONT_DEFAULT_NAME, 30),
          wraplength=350,
          style="BG_LABEL.TLabel")
    .pack(fill="both"))

    Label(side_center_frame,
          text="STUDENT INFORMATION SYSTEM",
          font=(FONT_DEFAULT_NAME, 10), style="BG_LABEL.TLabel").pack(fill="both")

    main_frame = Frame(window)
    main_frame.place(relx=0.45, rely=0, relwidth=0.55, relheight=1.0)

    center_content = Frame(main_frame)
    center_content.place(relx=0.5, rely=0.5, relwidth=0.5, anchor="center")

    label = Label(center_content,
                  text="Welcome!",
                  font=("SF Pro", 25, "bold"),
                  )
    label.pack()

    label = Label(center_content, text="Log in to your workspace",)
    label.pack(pady=(0, 48))

    # registers validation callback
    user_func = window.register(user_validation)
    pass_func = window.register(pass_validation)

    # User Label
    user_label = Label(center_content, text="Username")
    user_label.pack(anchor="w")

    # User Input
    user_input = Entry(center_content, width=200,
                       validate="focus",
                       validatecommand=(user_func, "%P"),
                       )
    user_input.pack(ipady=8, pady=(4, 0))

    user_error_label = Label(center_content, bootstyle="danger")
    user_error_label.pack(anchor="w")

    # Password Label
    password_label = Label(center_content, text="Password")
    password_label.pack(anchor="w")

    # Password Input
    password_input = Entry(center_content, width=200, show="•",
                           validate="focus",
                           validatecommand=(pass_func, "%P"))
    password_input.pack(ipady=8, pady=(4, 1))

    password_error_label = Label(center_content, bootstyle="danger")
    password_error_label.pack(anchor="w")

    remember_me_frame = Frame(center_content)
    remember_me_frame.pack(anchor="w", pady=8)


    remember_me_checkbox = Checkbutton(remember_me_frame, bootstyle="darkly")
    remember_me_checkbox.pack(side=LEFT)

    remember_me_label = Label(remember_me_frame, text="Remember me")
    remember_me_label.pack(side=LEFT)

    button = Button(center_content, bootstyle="darkly",
                    text="Login")
    button.config(command=onSubmit)
    button.pack(fill="x", pady=(12, 16), ipady=4)

