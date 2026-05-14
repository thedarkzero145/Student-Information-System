import os
import sys

from ttkbootstrap import Style

from constants import FONT_DEFAULT_NAME, CUSTOM_BACKGROUND_COLOR
from src.database.db_config import connect_db

def main() -> None:
        # If this file is executed as a script (e.g., `python src/main.py`), Python adds
        # `src/` (not the project root) to sys.path, so `import src...` fails.
        if __package__ in (None, ""):
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
                if project_root not in sys.path:
                        sys.path.insert(0, project_root)

        from src.frontend.login.login import open_login_window
        from src.frontend.dashboard.dashboard import open_dashboard_window
        from ttkbootstrap import Window

        window = Window()

        # INITIALIZE DATABASE
        conn = connect_db()

        # custom colors dont touch - aizen
        window.style.configure('BG_FRAME.TFrame', background=CUSTOM_BACKGROUND_COLOR)
        window.style.configure('BG_BUTTON.TButton', anchor="w", font=("Segoi UI", 10), padding=15, borderwidth=0, background=CUSTOM_BACKGROUND_COLOR)
        window.style.configure('BG_BUTTON_DANGER.TButton', foreground="#ff2414", anchor="w", font=("Segoi UI", 10), padding=15, borderwidth=0, background=CUSTOM_BACKGROUND_COLOR)
        window.style.configure("BG_CHECKBOX.TCheckbutton", background=CUSTOM_BACKGROUND_COLOR)
        window.style.configure("BG_ENTRY.TEntry", background=CUSTOM_BACKGROUND_COLOR)
        window.style.configure("BG_LABEL.TLabel", background=CUSTOM_BACKGROUND_COLOR, foreground="white")
        window.withdraw()

        open_login_window(window, conn)

        window.mainloop()

if __name__ == "__main__":
        main()
