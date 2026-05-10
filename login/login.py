from ttkbootstrap import Frame, Toplevel, Label, Entry, Button
from tkinter import END

# initialize login
def open_login(window):
    window = Toplevel(window)
    window.title("Login")
    window.geometry("1000x500")

    # Side Frame of Login
    side_frame = Frame(window,
                       width=300,
                       bootstyle="dark"
                       )

    side_frame.pack(side="left", fill="y")


    main_frame = Frame(window, borderwidth=2)
    main_frame.pack(fill="both", expand=True)


    center_content = Frame(main_frame)
    center_content.pack(expand=True, padx=150, anchor="w")

    label = Label(center_content, text="Welcome back", font=("Segoe UI", 35, "bold"), anchor="w")
    label.pack()

    label = Label(center_content, text="Sign in to your workspace")
    label.pack()

    # User Label
    user_label = Label(center_content, text="Username")
    user_label.pack(anchor="w")

    # User Input
    user_input = Entry(center_content, width=200)
    user_input.pack(ipady=5, pady=(0, 10))

    # Password Label
    password_label = Label(center_content, text="Password")
    password_label.pack(anchor="w")

    # Password Input
    password_input = Entry(center_content, width=200)
    password_input.pack(ipady=5, pady=(0, 10))


    button = Button(center_content, text="Sign in")
    button.pack(fill="x", pady=10, ipady=3)


