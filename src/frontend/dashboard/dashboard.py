import os
import tkinter as tk
from tkinter import ttk as tkttk
from PIL import Image, ImageTk

from constants import CUSTOM_BACKGROUND_COLOR
from icon_utils import apply_window_icon

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
TABLE_OUTER   = "#1a305e"   # navy card holding the table
TABLE_HEADER_BG = "#d1d5db" # light grey header row inside table
TABLE_BODY_BG   = "#e8eaf0" # light grey table body area
BADGE_GREEN_BG  = "#22c55e"
BADGE_RED_BG    = "#ef4444"
DEPT_BAR_BG     = "#001f5b"
DEPT_BAR_TRACK  = "#e5e7eb"

DASHBOARD_VERSION = "v5-student-figma"


# ── Helper: nav button ─────────────────────────────────────────────────────────
def _make_nav_btn(parent, text, icon, active=False, command=None):
    bg = NAV_HOVER if active else NAV_BG
    f = tk.Frame(parent, bg=bg, cursor="hand2", highlightthickness=0, bd=0)
    f.pack(fill="x", pady=1)
    inner = tk.Frame(f, bg=bg, highlightthickness=0, bd=0)
    inner.pack(fill="x", padx=8, pady=10)
    
    # Store references to images if any are used, to prevent garbage collection
    if not hasattr(f, "_image_refs"):
        f._image_refs = []
        
    icon_lbl = tk.Label(inner, text=icon, font=("Segoe UI", 16),
                        fg=WHITE, bg=bg)
    icon_lbl.pack(side="left", padx=(8, 14))
    text_lbl = tk.Label(inner, text=text, font=("Segoe UI", 13),
                        fg=WHITE, bg=bg, anchor="w")
    text_lbl.pack(side="left", fill="x")

    all_w = [f, inner, icon_lbl, text_lbl]

    def _enter(e):
        for w in all_w: w.config(bg=NAV_HOVER)

    def _leave(e):
        for w in all_w: w.config(bg=bg)

    for w in all_w:
        w.bind("<Enter>", _enter)
        w.bind("<Leave>", _leave)
        if command:
            w.bind("<Button-1>", lambda e, cmd=command: cmd())
    return f, icon_lbl


def _section_label(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 8, "bold"),
             fg="#7a9cc7", bg=NAV_BG, anchor="w",
             padx=22).pack(fill="x", pady=(16, 2))


# ── Helper: stat card (white rounded-border card) ──────────────────────────────
def _stat_card(parent, title, value, subtitle=None, icon_text="👥",
               badge_text=None, badge_bg=None, trend_text=None):
    # Outer border frame (simulates rounded border via 1-px colored frame)
    outer = tk.Frame(parent, bg=CARD_BORDER, highlightthickness=0, bd=0)
    outer.pack(side="left", fill="both", expand=True, padx=(0, 14))

    inner = tk.Frame(outer, bg=CARD_BG, highlightthickness=0, bd=0)
    inner.pack(padx=1, pady=1, fill="both", expand=True)

    pad = tk.Frame(inner, bg=CARD_BG)
    pad.pack(fill="both", expand=True, padx=18, pady=16)

    # Top row: icon + badge/label
    top = tk.Frame(pad, bg=CARD_BG)
    top.pack(fill="x")

    tk.Label(top, text=icon_text, font=("Segoe UI Emoji", 20),
             fg=TEXT_MUTED, bg=CARD_BG).pack(side="left")

    if badge_text and badge_bg:
        badge_f = tk.Frame(top, bg=badge_bg, highlightthickness=0, bd=0)
        badge_f.pack(side="right")
        tk.Label(badge_f, text=badge_text, font=("Segoe UI", 8, "bold"),
                 fg=WHITE, bg=badge_bg).pack(padx=9, pady=3)
    else:
        tk.Label(top, text="OVERALL", font=("Segoe UI", 8),
                 fg=TEXT_MUTED, bg=CARD_BG).pack(side="right")

    # Title
    tk.Label(pad, text=title, font=("Segoe UI", 10),
             fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x", pady=(12, 2))

    # Big value
    tk.Label(pad, text=value, font=("Segoe UI", 28, "bold"),
             fg=TEXT_PRIMARY, bg=CARD_BG, anchor="w").pack(fill="x")

    # Trend arrow (green)
    if trend_text:
        tr = tk.Frame(pad, bg=CARD_BG)
        tr.pack(fill="x", pady=(6, 0))
        tk.Label(tr, text="↗  " + trend_text, font=("Segoe UI", 9),
                 fg=ACCENT_GREEN, bg=CARD_BG, anchor="w").pack(side="left")

    # Subtitle (muted small text)
    if subtitle:
        tk.Label(pad, text=subtitle, font=("Segoe UI", 9),
                 fg=TEXT_MUTED, bg=CARD_BG, anchor="w").pack(fill="x", pady=(4, 0))

# ── Main entry ─────────────────────────────────────────────────────────────────
def open_dashboard_window(window, on_logout=None):


    win = tk.Toplevel(window)
    win.title(f"Student Dashboard — EDU SIS")
    win.geometry("1280x800")
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
    logo_row.pack(fill="x", padx=18, pady=(24, 16))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir  = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "assets"))

    tk.Label(logo_row, text="🎓", font=("Segoe UI Emoji", 28),
             fg=WHITE, bg=NAV_BG).pack(side="left", padx=(0, 12))

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

    btn_dashboard, lbl_dash   = _make_nav_btn(nav, "Dashboard", "⊞", active=True)
    
    _section_label(nav, "ACADEMICS")
    btn_grades, lbl_grades     = _make_nav_btn(nav, "Grades", "🗂️")
    btn_subjects, lbl_subjects = _make_nav_btn(nav, "Subjects", "📚")
    
    _section_label(nav, "CAMPUS LIFE")
    btn_ann, lbl_ann           = _make_nav_btn(nav, "Announcements", "🔊")
    btn_events, lbl_events     = _make_nav_btn(nav, "Events", "🎉")
    
    _section_label(nav, "SYSTEM")
    btn_settings, lbl_set      = _make_nav_btn(nav, "Settings", "⚙")

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
    _apply_nav_icon(btn_dashboard, lbl_dash, "icons8-dashboard-50.png", (22, 22))
    _apply_nav_icon(btn_grades, lbl_grades, "icons8-report-card-64.png", (22, 22))
    _apply_nav_icon(btn_subjects, lbl_subjects, "icons8-elective-50.png", (22, 22))
    _apply_nav_icon(btn_ann, lbl_ann, "icons8-announcement-64.png", (22, 22))
    _apply_nav_icon(btn_events, lbl_events, "icons8-events-64.png", (22, 22))
    _apply_nav_icon(btn_settings, lbl_set, "icons8-settings-24.png", (22, 22))


    # Logout (bottom)
    bottom = tk.Frame(sidebar, bg=NAV_BG, highlightthickness=0, bd=0)
    bottom.pack(side="bottom", fill="x", padx=4, pady=14)
    tk.Frame(bottom, bg="#1e3d7a", height=1,
             highlightthickness=0, bd=0).pack(fill="x", padx=14, pady=(0, 10))

    logout_f = tk.Frame(bottom, bg=NAV_BG, cursor="hand2",
                        highlightthickness=0, bd=0)
    logout_f.pack(fill="x")
    lo_inner = tk.Frame(logout_f, bg=NAV_BG, highlightthickness=0, bd=0)
    lo_inner.pack(fill="x", padx=10, pady=10)
    
    logout_f._image_refs = []

    lbl_lo_icon = tk.Label(lo_inner, text="◼", font=("Segoe UI", 16),
                           fg=ACCENT_RED, bg=NAV_BG)
    lbl_lo_icon.pack(side="left", padx=(8, 14))
    lbl_lo_text = tk.Label(lo_inner, text="Logout", font=("Segoe UI", 13),
                           fg=ACCENT_RED, bg=NAV_BG, anchor="w")
    lbl_lo_text.pack(side="left")
    
    _apply_nav_icon(logout_f, lbl_lo_icon, "icons8-log-out-64.png", (22, 22))

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

    tk.Label(left_top, text="Dashboard", font=("Segoe UI", 12, "bold"),
             fg=WHITE, bg=NAV_BG).pack(side="left", padx=(0, 16), pady=0)
    # bind vertical centering
    left_top.pack_configure(pady=0)

    tk.Frame(left_top, bg="#2d4d8a", width=1).pack(side="left", fill="y",
                                                    pady=14)

    search_wrap = tk.Frame(left_top, bg="#0d2d6b",
                           highlightthickness=1,
                           highlightbackground="#2d4d8a",
                           highlightcolor="#2d4d8a", bd=0)
    search_wrap.pack(side="left", padx=(16, 0), pady=15)
    tk.Label(search_wrap, text="🔍", font=("Segoe UI", 9),
             fg="#8fa8cc", bg="#0d2d6b").pack(side="left", padx=(8, 2))
    search_entry = tk.Entry(search_wrap, font=("Segoe UI", 10),
                            fg="#8fa8cc", bg="#0d2d6b",
                            insertbackground=WHITE,
                            relief="flat", bd=0, width=26)
    search_entry.insert(0, "Search courses, events...")
    search_entry.pack(side="left", pady=7, padx=(0, 10))

    def _fi(e):
        if search_entry.get() == "Search courses, events...":
            search_entry.delete(0, "end")
            search_entry.config(fg=WHITE)

    def _fo(e):
        if not search_entry.get().strip():
            search_entry.insert(0, "Search courses, events...")
            search_entry.config(fg="#8fa8cc")

    search_entry.bind("<FocusIn>",  _fi)
    search_entry.bind("<FocusOut>", _fo)

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

    main_frame = tk.Frame(content_wrap, bg=CONTENT_BG)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # ── STAT CARDS ────────────────────────────────────────────────────────────
    cards_row = tk.Frame(main_frame, bg=CONTENT_BG)
    cards_row.pack(fill="x", padx=24, pady=(22, 16))

    _stat_card(cards_row, "Current GPA",    "3.85", None,
               "📝", badge_text="Excellent",   badge_bg=BADGE_GREEN_BG)
    _stat_card(cards_row, "Total Units",   "18",
               "⊙  6 Enrolled Courses",
               "📚", badge_text="Active",   badge_bg=BADGE_GREEN_BG)
    _stat_card(cards_row, "Account Balance", "₱0.00",
               "⊙  Fully Paid for Semester",
               "💳", badge_text="Cleared", badge_bg=BADGE_GREEN_BG)

    # ── LOWER ROW ─────────────────────────────────────────────────────────────
    lower = tk.Frame(main_frame, bg=CONTENT_BG)
    lower.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    # ── ENROLLED COURSES TABLE (dark navy card) ───────────────────────────────────────
    table_card = tk.Frame(lower, bg=TABLE_OUTER,
                          highlightthickness=0, bd=0)
    table_card.pack(side="left", fill="both", expand=True, padx=(0, 16))

    tk.Label(table_card, text="Currently Enrolled Subjects", font=("Segoe UI", 12, "bold"),
             fg=WHITE, bg=TABLE_OUTER, anchor="w").pack(anchor="w",
                                                        padx=16, pady=(14, 10))

    # Table inner area (light grey)
    tree_holder = tk.Frame(table_card, bg="#c8cdd8",
                           highlightthickness=0, bd=0)
    tree_holder.pack(fill="both", expand=True, padx=10, pady=(0, 14))

    style = tkttk.Style()
    style.configure("StudentTree.Treeview",
                    background="#d8dde8",
                    foreground=TEXT_PRIMARY,
                    fieldbackground="#d8dde8",
                    rowheight=28,
                    font=("Segoe UI", 10))
    style.configure("StudentTree.Treeview.Heading",
                    background="#c0c6d4",
                    foreground=TEXT_PRIMARY,
                    font=("Segoe UI", 10, "bold"),
                    relief="flat")
    style.map("StudentTree.Treeview",
              background=[("selected", "#a0b4d0")],
              foreground=[("selected", TEXT_PRIMARY)])

    tree = tkttk.Treeview(tree_holder,
                          columns=("code", "title", "units", "schedule"),
                          show="headings",
                          style="StudentTree.Treeview",
                          height=10)
    tree.heading("code",     text="Course Code")
    tree.heading("title",   text="Course Title")
    tree.heading("units", text="Units")
    tree.heading("schedule",   text="Schedule")
    tree.column("code",     width=120, anchor="center", minwidth=80)
    tree.column("title",   width=260, anchor="w",      minwidth=140)
    tree.column("units", width=80, anchor="center", minwidth=50)
    tree.column("schedule",   width=150,  anchor="center", minwidth=100)

    DEMO_SUBJECTS = [
        ("CS101", "Introduction to Computing", "3.0", "MWF 9:00-10:00AM"),
        ("ENG101", "Purposive Communication", "3.0", "TTh 1:00-2:30PM"),
        ("MATH101", "Mathematics in the Modern World", "3.0", "MWF 11:00-12:00PM"),
        ("PE101", "Physical Fitness", "2.0", "Sat 8:00-10:00AM"),
        ("NSTP1", "Civic Welfare Training Service", "3.0", "Sun 8:00-11:00AM"),
        ("SCI101", "Science, Technology & Society", "3.0", "TTh 3:00-4:30PM"),
    ]
    for row in DEMO_SUBJECTS:
        tree.insert("", "end", values=row)

    tree_vsb = tkttk.Scrollbar(tree_holder, orient="vertical",
                                command=tree.yview)
    tree.configure(yscrollcommand=tree_vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    tree_vsb.pack(side="right", fill="y")

    # ── RIGHT PANEL ───────────────────────────────────────────────────────────
    right_panel = tk.Frame(lower, bg=CONTENT_BG, width=290)
    right_panel.pack(side="left", fill="both")
    right_panel.pack_propagate(False)

    # Campus image card (or announcement placeholder)
    campus_h = 130
    campus_frame = tk.Frame(right_panel, bg="#0d2447", height=campus_h)
    campus_frame.pack(fill="x", pady=(0, 14))
    campus_frame.pack_propagate(False)

    campus_overlay = tk.Frame(campus_frame, bg="#0d2447")
    campus_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    tk.Label(campus_overlay, text="Upcoming Event",
             font=("Segoe UI", 11, "bold"), fg=WHITE, bg="#0d2447",
             anchor="w", wraplength=260, justify="left").pack(anchor="w",
                                                              padx=16, pady=(24, 4))
    tk.Label(campus_overlay,
             text="Intramurals Week 2026 starting next Monday!",
             font=("Segoe UI", 9), fg="#aab4c8", bg="#0d2447",
             anchor="w", wraplength=260, justify="left").pack(anchor="w", padx=16)

    # Progress/Tasks card
    dept_outer = tk.Frame(right_panel, bg=CARD_BORDER)
    dept_outer.pack(fill="x")
    dept_white = tk.Frame(dept_outer, bg=WHITE)
    dept_white.pack(padx=1, pady=1, fill="both", expand=True)
    dept_pad = tk.Frame(dept_white, bg=WHITE)
    dept_pad.pack(fill="both", padx=16, pady=14)

    tk.Label(dept_pad, text="Semester Progress", font=("Segoe UI", 11, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 8))

    TOTAL = 100
    # Reusing the _dept_bar function for progress
    def _progress_bar(parent, name, percent):
        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill="x", pady=5)

        hdr = tk.Frame(row, bg=WHITE)
        hdr.pack(fill="x")
        tk.Label(hdr, text=name, font=("Segoe UI", 9, "bold"),
                 fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")
        tk.Label(hdr, text=f"{percent}%", font=("Segoe UI", 9),
                 fg=TEXT_MUTED, bg=WHITE).pack(side="right")

        track = tk.Frame(row, bg=DEPT_BAR_TRACK, height=6)
        track.pack(fill="x", pady=(4, 0))
        fill_w = min(percent / 100.0, 1.0)
        tk.Frame(track, bg=DEPT_BAR_BG, height=6).place(
            relx=0, rely=0, relheight=1, relwidth=fill_w)

    _progress_bar(dept_pad, "Week 8 of 16", 50)
    _progress_bar(dept_pad, "Attendance", 98)

    tk.Button(dept_pad, text="View Detailed Schedule",
              font=("Segoe UI", 10), fg=TEXT_PRIMARY, bg=WHITE,
              relief="solid", bd=1, cursor="hand2", pady=6,
              activebackground="#f3f4f6").pack(fill="x", pady=(14, 0))

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
    win.after(100, lambda: _force_bg(win))
