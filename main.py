from login.login import open_login
from ttkbootstrap import Window


window = Window(themename="darkly")
window.withdraw()

open_login(window)

window.mainloop()