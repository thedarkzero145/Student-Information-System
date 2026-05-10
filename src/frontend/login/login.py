from ttkbootstrap import Frame, Toplevel, Label, Entry, Button, Checkbutton
from tkinter import PhotoImage

import os

from ttkbootstrap.constants import LEFT


# initialize login
def open_login_window(window):
    window = Toplevel(window)
    window.title("Login")
    window.geometry("1000x800")

    # Side Frame of Login
    side_frame = Frame(window, width=350,  bootstyle="dark")
    side_frame.pack_propagate(False)
    side_frame.pack(side="left", fill="y")

    side_center_frame = Frame(side_frame, bootstyle="dark")
    side_center_frame.pack(expand=True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    bg_logo = PhotoImage(file=os.path.join(BASE_DIR, "assets", "plv-logo.png"))

    bg_label_image =  Label(side_center_frame, image=bg_logo, background="#303030")
    bg_label_image.image = bg_logo

    bg_label_image.pack(expand=True)


    Label(side_center_frame,
          text="STUDENT INFORMATION SYSTEM",
          background="#303030",
          font=("Segoe UI", 25,
                "bold"), wraplength=250).pack(fill="both")

    Label(side_center_frame,
          text="PAMANTASAN NG LUNGSOD NG VALENZUELA",
          background="#303030",
          font=("Segoe UI", 13),
          wraplength=250).pack(fill="both")

    main_frame = Frame(window, borderwidth=2)
    main_frame.pack(fill="both", expand=True)

    center_content = Frame(main_frame)
    center_content.place(relx=0.5, rely=0.5, relwidth=0.5, anchor="center")

    label = Label(center_content, text="Welcome back", font=("Segoe UI", 25, "bold"))
    label.pack()

    label = Label(center_content, text="Log in to your workspace")
    label.pack()

    # User Label
    user_label = Label(center_content, text="Username")
    user_label.pack(anchor="w")

    # User Input
    user_input = Entry(center_content, width=200)
    user_input.pack(ipady=7, pady=(5, 10))

    # Password Label
    password_label = Label(center_content, text="Password")
    password_label.pack(anchor="w")

    # Password Input
    password_input = Entry(center_content, width=200, show="•")
    password_input.pack(ipady=7, pady=(5, 10))

    remember_me_frame = Frame(center_content)
    remember_me_frame.pack(anchor="w", pady=7)

    remember_me_checkbox = Checkbutton(remember_me_frame)
    remember_me_checkbox.pack(side=LEFT)

    remember_me_label = Label(remember_me_frame, text="Remember me")
    remember_me_label.pack(side=LEFT)


    button = Button(center_content, text="Login")
    button.pack(fill="x", pady=(10, 20), ipady=5)

