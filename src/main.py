from src.frontend.login.login import open_login_window
from ttkbootstrap import Window


window = Window(themename="darkly")
window.withdraw()

open_login_window(window)

window.mainloop()