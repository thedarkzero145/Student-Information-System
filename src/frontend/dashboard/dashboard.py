from ttkbootstrap import Toplevel, Frame, Label, Separator, Button
from ttkbootstrap.constants import LEFT
from ttkbootstrap.icons import Emoji


def open_dashboard_window(window):
    window = Toplevel(window)
    window.title("Dashboard")
    window.geometry("1250x800")

    # === SIDEBAR ====
    side_bar_frame = Frame(window, width=250,  bootstyle="dark")
    side_bar_frame.pack_propagate(False)
    side_bar_frame.pack(side="left", fill="y", expand=False)

    Label(side_bar_frame, text="SIS", font=("SYSTEM ONLINE", 15), background="#303030").pack()
    Label(side_bar_frame,
          text="Student Information System",
          font=("Nova Mono", 12, "bold"), background="#303030").pack()


    button_frame = Frame(side_bar_frame)
    button_frame.pack(fill="both")

    dashboard_button = Button(button_frame,  text="Dashboard", bootstyle="dark-outline")
    dashboard_button.pack(fill="x", expand=True)

    # === DASHBOARD ====
    dashboard_frame = Frame(window, )
    dashboard_frame.pack(fill="both", expand=True)





