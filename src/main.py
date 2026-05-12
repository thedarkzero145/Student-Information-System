from ttkbootstrap import Style

from constants import FONT_DEFAULT_NAME, CUSTOM_BACKGROUND_COLOR


def main() -> None:
	import os
	import sys


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
	# custom colors dont touch - aizen
	window.style.configure('BG_FRAME.TFrame', background=CUSTOM_BACKGROUND_COLOR)
	window.style.configure('BG_BUTTON.TButton', anchor="w", font=("Segoi UI", 10), padding=15, borderwidth=0, background=CUSTOM_BACKGROUND_COLOR)
	window.style.configure('BG_BUTTON_DANGER.TButton', foreground="#ff2414", anchor="w", font=("Segoi UI", 10), padding=15, borderwidth=0, background=CUSTOM_BACKGROUND_COLOR)
	window.style.configure("BG_CHECKBOX.TCheckbutton", background=CUSTOM_BACKGROUND_COLOR)
	window.style.configure("BG_ENTRY.TEntry", background=CUSTOM_BACKGROUND_COLOR)
	window.style.configure("BG_LABEL.TLabel", background=CUSTOM_BACKGROUND_COLOR, foreground="white")
	window.withdraw()


	open_dashboard_window(window)

	window.mainloop()

def on_hover(event):
	event.widget.config(background="#d9534f", foreground="white")
def on_leave(event):
	event.widget.config(background=CUSTOM_BACKGROUND_COLOR, foreground="#d9534f")

if __name__ == "__main__":
	main()