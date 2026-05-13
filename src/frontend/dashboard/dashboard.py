import os
import tkinter as tk
from tkinter import ttk as tkttk
from PIL import Image, ImageTk

from constants import CUSTOM_BACKGROUND_COLOR
from icon_utils import apply_window_icon
from src.frontend.dashboard.grade import build_grades_tab
from src.frontend.dashboard.subjects import build_subjects_tab
from src.frontend.dashboard.announcements import build_announcements_tab
from src.frontend.dashboard.events import build_events_tab
from src.frontend.dashboard.settings import build_settings_tab

# ── TKINTER OVERRIDES TO FIX TTKBOOTSTRAP STYLING INTERFERENCE ──────────────
original_frame = tk.Frame
class ThemedFrame(original_frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "bg" in kwargs: self._my_bg = kwargs["bg"]
        if "background" in kwargs: self._my_bg = kwargs["background"]

original_label = tk.Label
class ThemedLabel(original_label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "bg" in kwargs: self._my_bg = kwargs["bg"]
        if "background" in kwargs: self._my_bg = kwargs["background"]
        if "fg" in kwargs: self._my_fg = kwargs["fg"]
        if "foreground" in kwargs: self._my_fg = kwargs["foreground"]

tk.Frame = ThemedFrame
tk.Label = ThemedLabel

# ── Colour tokens (from Figma design) ─────────────────────────────────────────
NAV_BG        = "#001f5b"   # deep navy sidebar / topbar
NAV_HOVER     = "#1a3a7a"   # hover state
WHITE         = "#ffffff"
CONTENT_BG    = "#edf0f5"   # light blue-grey page background
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
TEXT_NAV      = "#ffffff"
ACCENT_GREEN  = "#22c55e"
ACCENT_RED    = "#ef4444"
SEPARATOR     = "#e5e7eb"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#e2e8f0"

DASHBOARD_VERSION = "v6-student-figma"

nav_btns = {}

# ── Helper: nav button ─────────────────────────────────────────────────────────
def _make_nav_btn(parent, text, icon, command=None):
    f = tk.Frame(parent, bg=NAV_BG, cursor="hand2", highlightthickness=0, bd=0)
    f.pack(fill="x", pady=0)
    inner = tk.Frame(f, bg=NAV_BG, highlightthickness=0, bd=0)
    inner.pack(fill="x", padx=8, pady=6)
    
    if not hasattr(f, "_image_refs"):
        f._image_refs = []
        
    icon_lbl = tk.Label(inner, text=icon, font=("Segoe UI", 16),
                        fg=WHITE, bg=NAV_BG)
    icon_lbl.pack(side="left", padx=(8, 14))
    text_lbl = tk.Label(inner, text=text, font=("Segoe UI", 13),
                        fg=WHITE, bg=NAV_BG, anchor="w")
    text_lbl.pack(side="left", fill="x")

    all_w = [f, inner, icon_lbl, text_lbl]
    nav_btns[text] = all_w

    def _enter(e):
        for w in all_w: 
            if getattr(w, '_is_active', False) == False:
                w.config(bg=NAV_HOVER)

    def _leave(e):
        for w in all_w: 
            if getattr(w, '_is_active', False) == False:
                w.config(bg=NAV_BG)

    for w in all_w:
        w.bind("<Enter>", _enter)
        w.bind("<Leave>", _leave)
        if command:
            w.bind("<Button-1>", lambda e, cmd=command: cmd())
    return f, icon_lbl

def _set_active_nav(text):
    for name, widgets in nav_btns.items():
        is_active = (name == text)
        bg_col = NAV_HOVER if is_active else NAV_BG
        for w in widgets:
            w._is_active = is_active
            w.config(bg=bg_col)

def _section_label(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 8, "bold"),
             fg="#7a9cc7", bg=NAV_BG, anchor="w",
             padx=22).pack(fill="x", pady=(16, 2))


# ── VIEW BUILDERS ────────────────────────────────────────────────────────────
def build_dashboard_tab(parent, switch_cb):
    
    # ── Profile Banner ──
    banner_outer = tk.Frame(parent, bg=CARD_BORDER)
    banner_outer.pack(fill="x", padx=24, pady=(24, 16))
    banner = tk.Frame(banner_outer, bg=NAV_BG)
    banner.pack(padx=1, pady=1, fill="both", expand=True)
    
    banner_pad = tk.Frame(banner, bg=NAV_BG)
    banner_pad.pack(fill="x", padx=32, pady=32)
    
    # Avatar Circle
    avatar_bg = tk.Frame(banner_pad, bg=WHITE, width=100, height=100)
    avatar_bg.pack(side="left", padx=(0, 24))
    avatar_bg.pack_propagate(False)
    # inside grey circle
    avatar_inner = tk.Frame(avatar_bg, bg="#a0aab8", width=90, height=90)
    avatar_inner.place(relx=0.5, rely=0.5, anchor="center")
    avatar_inner.pack_propagate(False)
    tk.Label(avatar_inner, text="👤", font=("Segoe UI Emoji", 48), fg=WHITE, bg="#a0aab8").place(relx=0.5, rely=0.5, anchor="center")
    
    text_f = tk.Frame(banner_pad, bg=NAV_BG)
    text_f.pack(side="left", fill="y", pady=6)
    tk.Label(text_f, text="Juan Dela Cruz", font=("Segoe UI", 24), fg=WHITE, bg=NAV_BG).pack(anchor="w")
    tk.Label(text_f, text="BSIT 1-1", font=("Segoe UI", 12), fg=WHITE, bg=NAV_BG).pack(anchor="w", pady=(4,0))
    tk.Label(text_f, text="25-2751", font=("Segoe UI", 10), fg="#aab4c8", bg=NAV_BG).pack(anchor="w", pady=(4,0))
    
    
    # ── Grid Layout ──
    cols = tk.Frame(parent, bg=CONTENT_BG)
    cols.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    # ── Left: Schedule ──
    left_col = tk.Frame(cols, bg=CARD_BORDER, width=420)
    left_col.pack(side="left", fill="y", padx=(0, 16))
    left_col.pack_propagate(False)
    
    left_inner = tk.Frame(left_col, bg=CARD_BG)
    left_inner.pack(padx=1, pady=1, fill="both", expand=True)
    
    sched_hdr = tk.Frame(left_inner, bg=CARD_BG)
    sched_hdr.pack(fill="x", padx=24, pady=24)
    tk.Label(sched_hdr, text="Today's Schedule", font=("Segoe UI", 11, "bold"), fg=NAV_BG, bg=CARD_BG).pack(side="left")
    tk.Label(sched_hdr, text="Monday, May 18", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(side="right")
    
    tk.Frame(left_inner, bg=CARD_BORDER, height=1).pack(fill="x", padx=24)
    
    timeline = tk.Frame(left_inner, bg=CARD_BG)
    timeline.pack(fill="both", expand=True, padx=24, pady=24)
    
    def _timeline_item(p, time_val, title, type_badge, room, current=False, last=False, advisor=None):
        r = tk.Frame(p, bg=CARD_BG)
        r.pack(fill="x", pady=0)
        
        # Left bar with dot
        bar = tk.Frame(r, bg=CARD_BG, width=20)
        bar.pack(side="left", fill="y")
        bar.pack_propagate(False)
        
        dot_col = NAV_BG if current else "#cbd5e1"
        dot = tk.Frame(bar, bg=dot_col, width=10, height=10)
        dot.pack(pady=4)
        if not last:
            line = tk.Frame(bar, bg="#e2e8f0", width=2)
            line.pack(fill="y", expand=True)
            
        content = tk.Frame(r, bg=CARD_BG)
        content.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 24))
        
        top = tk.Frame(content, bg=CARD_BG)
        top.pack(fill="x")
        tk.Label(top, text=title, font=("Segoe UI", 10, "bold" if current else "normal"), fg=TEXT_PRIMARY if current else TEXT_MUTED, bg=CARD_BG).pack(side="left")
        if type_badge:
            tk.Label(top, text=type_badge, font=("Segoe UI", 7), fg="#4a6fa5", bg="#f1f5f9", padx=4).pack(side="left", padx=8)
            
        btm = tk.Frame(content, bg=CARD_BG)
        btm.pack(fill="x", pady=(4, 0))
        t_col = NAV_BG if current else TEXT_MUTED
        t_txt = f"{time_val} (Current)" if current else time_val
        tk.Label(btm, text=f"🕒 {t_txt}", font=("Segoe UI", 8, "bold" if current else "normal"), fg=t_col, bg=CARD_BG).pack(side="left")
        
        loc_str = f"📍 {room}" if room else f"👤 {advisor}"
        tk.Label(btm, text=loc_str, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left", padx=(12, 0))

    _timeline_item(timeline, "09:00 AM - 10:30 AM", "ECO 201: Microeconomic Theory", "Lecture", "Hall 4B, Business Building")
    _timeline_item(timeline, "11:00 AM - 12:30 PM", "STA 102: Statistics for Business", "Seminar", "Room 204, Tech Center", current=True)
    _timeline_item(timeline, "02:00 PM - 02:30 PM", "Academic Advising Meeting", None, None, last=True, advisor="Advisor: Dr. Sarah Jenkins")

    # ── Right: Tiles ──
    right_col = tk.Frame(cols, bg=CONTENT_BG)
    right_col.pack(side="left", fill="both", expand=True)
    
    # Quotes
    quotes_outer = tk.Frame(right_col, bg=CARD_BORDER)
    quotes_outer.pack(fill="x", pady=(0, 16))
    quotes = tk.Frame(quotes_outer, bg=NAV_BG)
    quotes.pack(padx=1, pady=1, fill="both", expand=True)
    tk.Label(quotes, text="Motivational Quote", font=("Segoe UI", 14), fg=WHITE, bg=NAV_BG).pack(anchor="w", padx=24, pady=(24, 16))
    tk.Label(quotes, text='"I Think, therefore I am"', font=("Segoe UI", 20), fg=WHITE, bg=NAV_BG).pack(anchor="w", padx=24, pady=(0, 16))
    tk.Label(quotes, text="— Renz Descartes", font=("Segoe UI", 10), fg="#aab4c8", bg=NAV_BG).pack(anchor="w", padx=24, pady=(0, 24))

    # Two small cards row
    row2 = tk.Frame(right_col, bg=CONTENT_BG)
    row2.pack(fill="x", pady=(0, 16))
    
    def _navy_stat(parent, icon, title, val):
        outer = tk.Frame(parent, bg=CARD_BORDER)
        outer.pack(side="left", fill="both", expand=True, padx=(0, 16))
        c = tk.Frame(outer, bg=NAV_BG)
        c.pack(padx=1, pady=1, fill="both", expand=True)
        
        c_in = tk.Frame(c, bg=NAV_BG)
        c_in.pack(expand=True, padx=24, pady=24)
        
        tk.Label(c_in, text=icon, font=("Segoe UI", 32), fg=WHITE, bg=NAV_BG).pack(side="left", padx=(0, 24))
        r = tk.Frame(c_in, bg=NAV_BG)
        r.pack(side="left")
        tk.Label(r, text=title, font=("Segoe UI", 11), fg="#aab4c8", bg=NAV_BG).pack(anchor="w")
        tk.Label(r, text=val, font=("Segoe UI", 20), fg=WHITE, bg=NAV_BG).pack(anchor="w")
        return outer
        
    _navy_stat(row2, "★", "Grade", "99.6")
    att = _navy_stat(row2, "👤", "Attendance", "18.0 Units")
    att.pack_configure(padx=0) # remove right margin on second card
    
    # Third small card row
    row3 = tk.Frame(right_col, bg=CONTENT_BG)
    row3.pack(fill="x")
    
    c3 = _navy_stat(row3, "≡", "Credits Earned", "18.0 Units")
    c3.pack_configure(side="left", fill="both", expand=True, padx=0)





# ── Main entry ─────────────────────────────────────────────────────────────────
def open_dashboard_window(window, on_logout=None):
    win = tk.Toplevel(window)
    win.title(f"Student Dashboard — EDU SIS")
    
    # Make it wide and dynamically as tall as the screen allows without capping
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    width = 1440
    height = min(1000, screen_height - 80)
    
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    
    # Prevent negative coordinates if screen is smaller than window
    x = max(0, x)
    y = max(0, y)
    
    win.geometry(f"{width}x{height}+{x}+{y}")
    win.minsize(1100, 720)
    win.configure(bg=NAV_BG)

    apply_window_icon(win, calling_file=__file__)

    win.columnconfigure(0, weight=0, minsize=260)
    win.columnconfigure(1, weight=1)
    win.rowconfigure(0, weight=1)

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    SIDEBAR_W = 260
    sidebar_canvas = tk.Canvas(win, width=SIDEBAR_W, bg=NAV_BG,
                               highlightthickness=0, borderwidth=0, bd=0)
    sidebar_canvas.grid(row=0, column=0, sticky="nsew")

    sidebar = tk.Frame(sidebar_canvas, bg=NAV_BG, highlightthickness=0, bd=0)
    _sb_win = sidebar_canvas.create_window(0, 0, anchor="nw",
                                           window=sidebar, width=SIDEBAR_W)

    def _resize_sb(e):
        sidebar_canvas.itemconfig(_sb_win, width=e.width, height=e.height)
        sidebar_canvas.delete("bg_rect")
        sidebar_canvas.create_rectangle(0, 0, e.width, e.height,
                                        fill=NAV_BG, outline="", tags="bg_rect")
        sidebar_canvas.tag_lower("bg_rect")

    sidebar_canvas.bind("<Configure>", _resize_sb)

    # Logo row
    logo_row = tk.Frame(sidebar, bg=NAV_BG, highlightthickness=0, bd=0)
    logo_row.pack(fill="x", padx=18, pady=(16, 8))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir  = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "assets"))

    lbl_logo = tk.Label(logo_row, bg=NAV_BG)
    lbl_logo.pack(side="left", padx=(0, 12))
    
    try:
        from PIL import Image, ImageTk
        path = os.path.join(assets_dir, "edu-icon.png")
        if os.path.exists(path):
            img = Image.open(path).resize((42, 42), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl_logo.config(image=photo)
            lbl_logo.image = photo
        else:
            lbl_logo.config(text="🎓", font=("Segoe UI Emoji", 28), fg=WHITE)
    except Exception:
        lbl_logo.config(text="🎓", font=("Segoe UI Emoji", 28), fg=WHITE)

    text_col = tk.Frame(logo_row, bg=NAV_BG, highlightthickness=0, bd=0)
    text_col.pack(side="left")
    tk.Label(text_col, text="ENCHONG DEE\nUNIVERSITY",
             font=("Segoe UI", 13, "bold"), fg=WHITE, bg=NAV_BG,
             justify="left", anchor="w").pack(anchor="w")
    tk.Label(text_col, text="STUDENT INFORMATION SYSTEM",
             font=("Segoe UI", 7), fg="#8fa8cc", bg=NAV_BG,
             justify="left", anchor="w").pack(anchor="w")

    # Divider
    tk.Frame(sidebar, bg="#1e3d7a", height=1,
             highlightthickness=0, bd=0).pack(fill="x", padx=14, pady=(4, 8))

    # Nav buttons
    nav = tk.Frame(sidebar, bg=NAV_BG)
    nav.pack(fill="x", padx=4)

    current_tab_frame = None

    def switch_tab(tab_name):
        nonlocal current_tab_frame
        if current_tab_frame:
            current_tab_frame.destroy()
        
        main_frame = tk.Frame(content_wrap, bg=CONTENT_BG)
        main_frame.grid(row=0, column=0, sticky="nsew")
        current_tab_frame = main_frame

        _set_active_nav(tab_name)

        if tab_name == "Dashboard":
            title_lbl.config(text="Dashboard")
            build_dashboard_tab(main_frame, switch_tab)
        elif tab_name == "Grades":
            title_lbl.config(text="Grades")
            build_grades_tab(main_frame, switch_tab)
        elif tab_name == "Subjects":
            title_lbl.config(text="Enrolled Subjects")
            build_subjects_tab(main_frame, switch_tab)
        elif tab_name == "Announcements":
            title_lbl.config(text="Announcements")
            build_announcements_tab(main_frame, switch_tab)
        elif tab_name == "Events":
            title_lbl.config(text="Events")
            build_events_tab(main_frame, switch_tab)
        elif tab_name == "Settings":
            title_lbl.config(text="Settings")
            build_settings_tab(main_frame, switch_tab)
        else:
            title_lbl.config(text=tab_name)
            tk.Label(main_frame, text=f"{tab_name}\n(Under Construction)", font=("Segoe UI", 20), fg=TEXT_MUTED, bg=CONTENT_BG, justify="center").pack(expand=True)
            
        win.after(50, lambda: _force_bg(main_frame))

    btn_dashboard, lbl_dash   = _make_nav_btn(nav, "Dashboard", "⊞", command=lambda: switch_tab("Dashboard"))
    
    _section_label(nav, "ACADEMICS")
    btn_grades, lbl_grades     = _make_nav_btn(nav, "Grades", "🗂️", command=lambda: switch_tab("Grades"))
    btn_subjects, lbl_subjects = _make_nav_btn(nav, "Subjects", "📚", command=lambda: switch_tab("Subjects"))
    
    _section_label(nav, "CAMPUS LIFE")
    btn_ann, lbl_ann           = _make_nav_btn(nav, "Announcements", "🔊", command=lambda: switch_tab("Announcements"))
    btn_events, lbl_events     = _make_nav_btn(nav, "Events", "🎉", command=lambda: switch_tab("Events"))
    
    _section_label(nav, "SYSTEM")
    btn_settings, lbl_set      = _make_nav_btn(nav, "Settings", "⚙", command=lambda: switch_tab("Settings"))

    # Helper to load an icon safely
    def _apply_nav_icon(btn, lbl, filename, size=(20, 20)):
        try:
            path = os.path.join(assets_dir, filename)
            if os.path.exists(path):
                img = Image.open(path).resize(size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl.configure(image=photo, text="")
                lbl.image = photo
                btn._image_refs.append(photo)
        except Exception as e:
            print(f"Failed to load icon {filename}: {e}")

    # Load image icons into nav buttons
    _apply_nav_icon(btn_dashboard, lbl_dash, "dashboard-50.png", (22, 22))
    _apply_nav_icon(btn_grades, lbl_grades, "rating-64.png", (22, 22))
    _apply_nav_icon(btn_subjects, lbl_subjects, "elective-50.png", (22, 22))
    _apply_nav_icon(btn_ann, lbl_ann, "announcement-64.png", (22, 22))
    _apply_nav_icon(btn_events, lbl_events, "events-64.png", (22, 22))
    _apply_nav_icon(btn_settings, lbl_set, "settings-24.png", (22, 22))


    # Logout (bottom)
    bottom = tk.Frame(sidebar, bg=NAV_BG, highlightthickness=0, bd=0)
    bottom.pack(side="bottom", fill="x", padx=4, pady=8)
    tk.Frame(bottom, bg="#1e3d7a", height=1,
             highlightthickness=0, bd=0).pack(fill="x", padx=14, pady=(0, 6))

    logout_f = tk.Frame(bottom, bg=NAV_BG, cursor="hand2",
                        highlightthickness=0, bd=0)
    logout_f.pack(fill="x")
    lo_inner = tk.Frame(logout_f, bg=NAV_BG, highlightthickness=0, bd=0)
    lo_inner.pack(fill="x", padx=10, pady=6)
    
    logout_f._image_refs = []

    lbl_lo_icon = tk.Label(lo_inner, text="◼", font=("Segoe UI", 16),
                           fg=ACCENT_RED, bg=NAV_BG)
    lbl_lo_icon.pack(side="left", padx=(8, 14))
    lbl_lo_text = tk.Label(lo_inner, text="Logout", font=("Segoe UI", 13),
                           fg=ACCENT_RED, bg=NAV_BG, anchor="w")
    lbl_lo_text.pack(side="left")
    
    _apply_nav_icon(logout_f, lbl_lo_icon, "log-out-64.png", (22, 22))

    def do_logout():
        win.destroy()
        if on_logout:
            on_logout()

    for w in (logout_f, lo_inner, lbl_lo_icon, lbl_lo_text):
        w.bind("<Button-1>", lambda e: do_logout())

    # ── RIGHT SIDE (topbar + content) ─────────────────────────────────────────
    right_side = tk.Frame(win, bg=NAV_BG, highlightthickness=0, bd=0)
    right_side.grid(row=0, column=1, sticky="nsew")
    right_side.rowconfigure(1, weight=1)
    right_side.columnconfigure(0, weight=1)

    # ── TOP BAR (dark navy, same as sidebar) ──────────────────────────────────
    topbar = tk.Frame(right_side, bg=NAV_BG, height=60,
                      highlightthickness=0, bd=0)
    topbar.grid(row=0, column=0, sticky="ew")
    topbar.grid_propagate(False)

    tb_inner = tk.Frame(topbar, bg=NAV_BG, highlightthickness=0, bd=0)
    tb_inner.pack(fill="both", expand=True, padx=20)

    # Left: "Dashboard" title + divider + search
    left_top = tk.Frame(tb_inner, bg=NAV_BG)
    left_top.pack(side="left", fill="y")

    title_lbl = tk.Label(left_top, text="Dashboard", font=("Segoe UI", 12, "bold"),
             fg=WHITE, bg=NAV_BG)
    title_lbl.pack(side="left", padx=(0, 16), pady=0)
    # bind vertical centering
    left_top.pack_configure(pady=0)



    # Right: Student User pill button
    right_top = tk.Frame(tb_inner, bg=NAV_BG)
    right_top.pack(side="right", fill="y")

    user_pill = tk.Frame(right_top, bg=NAV_BG,
                          highlightthickness=1,
                          highlightbackground="#4a6fa5",
                          highlightcolor="#4a6fa5", bd=0,
                          cursor="hand2")
    user_pill.pack(side="right", pady=15)

    # Small avatar circle (simulated with a colored label)
    avatar_f = tk.Frame(user_pill, bg="#2d4d8a",
                        width=26, height=26,
                        highlightthickness=0, bd=0)
    avatar_f.pack(side="left", padx=(8, 6), pady=6)
    avatar_f.pack_propagate(False)
    tk.Label(avatar_f, text="🎓", font=("Segoe UI Emoji", 12),
             fg=WHITE, bg="#2d4d8a").place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(user_pill, text="Student Name", font=("Segoe UI", 10),
             fg=WHITE, bg=NAV_BG).pack(side="left", padx=(0, 12), pady=6)

    # ── CONTENT AREA (light grey page) ────────────────────────────────────────
    content_wrap = tk.Frame(right_side, bg=CONTENT_BG,
                            highlightthickness=0, bd=0)
    content_wrap.grid(row=1, column=0, sticky="nsew")
    content_wrap.rowconfigure(0, weight=1)
    content_wrap.columnconfigure(0, weight=1)

    # ── FORCE BACKGROUNDS ─────────────────────────────────────────────────────
    # ttkbootstrap's theme engine can override tk widget bg colors.
    # Walk the entire widget tree and re-apply each widget's intended bg.
    def _force_bg(widget):
        if hasattr(widget, '_my_bg'):
            try: widget.configure(bg=widget._my_bg)
            except Exception: pass
        if hasattr(widget, '_my_fg'):
            try: widget.configure(fg=widget._my_fg)
            except Exception: pass
        for child in widget.winfo_children():
            _force_bg(child)

    win.update_idletasks()
    
    switch_tab("Dashboard")
    
    win.after(100, lambda: _force_bg(win))
