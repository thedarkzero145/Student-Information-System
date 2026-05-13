import os
import sys

_ico_path = None
_icon_photo = None


def _get_assets_dir(calling_file):
    src_dir = os.path.dirname(os.path.abspath(calling_file))
    # Walk up until we find the assets/ folder (handles different depths)
    candidate = src_dir
    for _ in range(6):
        assets = os.path.join(candidate, "assets")
        if os.path.isdir(assets):
            return assets
        candidate = os.path.dirname(candidate)
    return None


def apply_window_icon(win, assets_dir=None, calling_file=None):
    """Set the window icon reliably on Windows and other platforms.

    On Windows: converts PNG to ICO once, then uses iconbitmap().
    On other platforms: uses iconphoto() with a module-level reference.

    Call as: apply_window_icon(win, calling_file=__file__)
    or:       apply_window_icon(win, assets_dir='/absolute/path/to/assets')
    """
    global _ico_path, _icon_photo

    if assets_dir is None:
        assets_dir = _get_assets_dir(calling_file or __file__)
    if assets_dir is None:
        return

    png_path = os.path.join(assets_dir, "app-icon.png")
    if not os.path.exists(png_path):
        return

    def _set():
        global _ico_path, _icon_photo
        try:
            if sys.platform == "win32":
                if _ico_path is None:
                    from PIL import Image
                    ico = os.path.join(assets_dir, "app-icon.ico")
                    img = Image.open(png_path)
                    img.save(ico, format="ICO",
                             sizes=[(256, 256), (64, 64), (32, 32), (16, 16)])
                    _ico_path = ico
                win.iconbitmap(default=_ico_path)
            else:
                if _icon_photo is None:
                    from PIL import Image, ImageTk
                    img = Image.open(png_path).resize((64, 64), Image.LANCZOS)
                    _icon_photo = ImageTk.PhotoImage(img)
                win.iconphoto(True, _icon_photo)
        except Exception:
            pass

    win.after(0, _set)
