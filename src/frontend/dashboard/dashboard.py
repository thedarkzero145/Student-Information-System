import os
from PIL import Image, ImageTk

from ttkbootstrap import Toplevel, Frame, Label, Separator, Button
from ttkbootstrap.constants import LEFT, CENTER, BOTTOM
from ttkbootstrap.icons import Emoji

from constants import CUSTOM_BACKGROUND_NAME, CUSTOM_LABEL_NAME
from main import on_hover, on_leave
from icon_utils import apply_window_icon


def open_dashboard_window(window):
    window = Toplevel(window)
    window.title("Dashboard")
    window.geometry("1000x600")

    apply_window_icon(window, calling_file=__file__)

    window.columnconfigure(0, weight=0, minsize=250)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)

    # ==== SIDE FRAME ====
    side_frame = Frame(window, style=CUSTOM_BACKGROUND_NAME)
    side_frame.grid(row=0, column=0, sticky='nsew')

    # ==== DASHBOARD FRAME ====
    open_dashboard_frame(window)

    # ==== SIDE header CONTAINER ====
    side_header_container = Frame(side_frame, style=CUSTOM_BACKGROUND_NAME)
    side_header_container.pack(fill="x",
                              padx=(12, 18),
                              pady=(18, 0)
                              )

    # ==== SIDE TITLE WIDGETS ====
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, "..", "..", "..", "assets")

    origin_logo_img = Image.open(os.path.join(assets_dir, "edu1.png"))
    resized_img = origin_logo_img.resize((70, 70))
    tk_img = ImageTk.PhotoImage(resized_img)

    logo_label = Label(side_header_container,
                       text="Student Information System",
                       image=tk_img,
                       style=CUSTOM_LABEL_NAME
                       )
    logo_label.image = tk_img
    logo_label.pack(side=LEFT, padx=(0, 8))

    logo_title = Label(side_header_container,
                       text="ENCHONG DEE UNIVERSITY",
                        style=CUSTOM_LABEL_NAME,
                       font=("Times New Roman", 17),
                       wraplength=180
                       )
    logo_title.pack(anchor="w")

    logo_title = Label(side_header_container,
                       text="STUDENT INFORMATION SYSTEM",
                       style=CUSTOM_LABEL_NAME,
                       font=("Times New Roman", 7),
                       )
    logo_title.pack(anchor="w")

    # === SEPARATOR ===
    Separator(side_frame, bootstyle="light").pack(fill="x", padx=(12, 18), pady=14)

    # ==== SIDE BUTTON CONTAINER ===
    side_button_container = Frame(side_frame, style=CUSTOM_BACKGROUND_NAME)
    side_button_container.pack(
        fill="both",
        padx=(12, 18)
    )

    # === UPPER MULTIPLE BUTTONS ===

    dashboard_btn = Button(side_button_container,
                           text="🏠︎Dashboard",
                           cursor="hand2",
                           style="BG_BUTTON.TButton")
    dashboard_btn.pack(fill="x")

    grades_btn = Button(side_button_container,
                           text="🗂️Grades",
                           cursor="hand2",
                           style="BG_BUTTON.TButton")
    grades_btn.pack(fill="x")

    subjects_btn = Button(side_button_container,
                           text="🏠︎Subjects",
                           cursor="hand2",
                           style="BG_BUTTON.TButton")
    subjects_btn.pack(fill="x")

    announcement_btn = Button(side_button_container,
                           text="🔊    Announcement",
                           cursor="hand2",
                           style="BG_BUTTON.TButton")
    announcement_btn.pack(fill="x")

    events_btn = Button(side_button_container,
                           text="🎉︎Events",
                           cursor="hand2",
                           style="BG_BUTTON.TButton")
    events_btn.pack(fill="x")

    # ==== BOTTOM MULTIPLE BUTTONS
    bottom_buttons_container = Frame(side_frame, style=CUSTOM_BACKGROUND_NAME, padding=12)
    bottom_buttons_container.pack(side="bottom", fill="x")

    setting_btn = Button(bottom_buttons_container,
                           text="⚙️   Settings",
                           cursor="hand2",
                           style="BG_BUTTON.TButton")
    setting_btn.pack(fill="x")

    #   === SEPARATOR ===
    Separator(bottom_buttons_container, bootstyle="light").pack(fill="x", padx=4, pady=8)

    logout_btn = Button(bottom_buttons_container,
                           text="➜]   Logout",
                           cursor="hand2",
                           style="BG_BUTTON_DANGER.TButton"
                        )
    logout_btn.pack(fill="x")

def open_dashboard_frame(window):
    dashboard_frame = Frame(window)
    dashboard_frame.grid(row=0, column=1, sticky='nsew')

    dashboard_frame.columnconfigure(0, weight=1)
    dashboard_frame.columnconfigure(1, weight=1)
    dashboard_frame.columnconfigure(2, weight=1)
    dashboard_frame.columnconfigure(3, weight=1)
    dashboard_frame.columnconfigure(4, weight=1)

    dashboard_frame.rowconfigure(0, weight=0, minsize=80)
    dashboard_frame.rowconfigure(1, weight=2)
    dashboard_frame.rowconfigure(2, weight=2)
    dashboard_frame.rowconfigure(3, weight=2)
    # ===== UPPER HEADER DASHBOARD ====
    header_dashboard = Frame(dashboard_frame)
    header_dashboard.grid(row=0, columnspan=5, sticky='nsew', padx=18)

    Label(header_dashboard, text="Dashboard", font=("Times New Roman", 20, "bold")).pack(side=LEFT, fill="x")
