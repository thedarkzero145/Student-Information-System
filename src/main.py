from src.frontend.login.login import open_login_window
from ttkbootstrap import Window

def main() -> None:
	window = Window(themename="darkly")
	window.withdraw()

open_login_window(window)

	window.mainloop()


if __name__ == "__main__":
	main()