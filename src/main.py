import os
import sys

# If this file is executed as a script (e.g., `python src/main.py`), Python adds
# `src/` (not the project root) to sys.path, so `import src...` fails.
if __package__ in (None, ""):
	project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
	if project_root not in sys.path:
		sys.path.insert(0, project_root)

from src.frontend.login.login import open_login
from ttkbootstrap import Window

def main() -> None:
	window = Window(themename="darkly")
	window.withdraw()

	open_login(window)

	window.mainloop()


if __name__ == "__main__":
	main()