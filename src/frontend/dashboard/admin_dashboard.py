import os
import tkinter as tk
from tkinter import ttk as tkttk
from PIL import Image, ImageTk

from constants import CUSTOM_BACKGROUND_COLOR
from icon_utils import apply_window_icon

NAV_BG       = "#002961"
NAV_HOVER    = "#1a4080"
WHITE        = "#ffffff"
CONTENT_BG   = "#f5f7fa"
TEXT_PRIMARY = "#111827"
TEXT_MUTED   = "#6b7280"
ACCENT_GREEN = "#22c55e"
ACCENT_RED   = "#ef4444"
SEPARATOR    = "#e5e7eb"
CARD_BORDER  = "#d1d5db"
TABLE_BG     = "#0d2447"
TABLE_ALT    = "#102d55"


def _make_nav_btn(parent, text, icon, active=False, command=None):
    bg = NAV_HOVER if active else NAV_BG
    f = tk.Frame(parent, bg=bg, cursor="hand2",
                 highlightthickness=0, bd=0)
    f.pack(fill="x", pady=1)
    inner = tk.Frame(f, bg=bg, highlightthickness=0, bd=0)
    inner.pack(fill="x", padx=10, pady=11)
    icon_lbl = tk.Label(inner, text=icon, font=("Segoe UI", 16),
                        fg=WHITE, bg=bg)
    icon_lbl.pack(side="left", padx=(6, 14))
    text_lbl = tk.Label(inner, text=text, font=("Segoe UI", 14),
                        fg=WHITE, bg=bg, anchor="w")
    text_lbl.pack(side="left", fill="x")

    all_widgets = [f, inner, icon_lbl, text_lbl]

    def _enter(e):
        for w in all_widgets:
            w.config(bg=NAV_HOVER)

    def _leave(e):
        for w in all_widgets:
            w.config(bg=bg)

    for w in all_widgets:
        w.bind("<Enter>", _enter)
        w.bind("<Leave>", _leave)
        if command:
            w.bind("<Button-1>", lambda e, cmd=command: cmd())

    return f


def _section_label(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 9, "bold"),
             fg="#7a9cc7", bg=NAV_BG, anchor="w",
             padx=20).pack(fill="x", pady=(14, 4))


def _stat_card(parent, title, value, subtitle=None, icon_text="👥",
               badge_text=None, badge_bg=None, trend_text=None):
    outer = tk.Frame(parent, bg=CARD_BORDER)
    outer.pack(side="left", fill="both", expand=True, padx=(0, 14))
    inner = tk.Frame(outer, bg=WHITE)
    inner.pack(padx=1, pady=1, fill="both", expand=True)
    pad = tk.Frame(inner, bg=WHITE)
    pad.pack(fill="both", expand=True, padx=16, pady=14)

    top = tk.Frame(pad, bg=WHITE)
    top.pack(fill="x")
    tk.Label(top, text=icon_text, font=("Segoe UI Emoji", 18),
             fg=TEXT_MUTED, bg=WHITE).pack(side="left")

    if badge_text and badge_bg:
        badge_f = tk.Frame(top, bg=badge_bg)
        badge_f.pack(side="right")
        tk.Label(badge_f, text=badge_text, font=("Segoe UI", 8, "bold"),
                 fg=WHITE, bg=badge_bg).pack(padx=7, pady=3)
    else:
        tk.Label(top, text="OVERALL", font=("Segoe UI", 8),
                 fg=TEXT_MUTED, bg=WHITE).pack(side="right")

    tk.Label(pad, text=title, font=("Segoe UI", 10),
             fg=TEXT_MUTED, bg=WHITE, anchor="w").pack(fill="x", pady=(10, 2))
    tk.Label(pad, text=value, font=("Segoe UI", 26, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE, anchor="w").pack(fill="x")

    if trend_text:
        tr = tk.Frame(pad, bg=WHITE)
        tr.pack(fill="x", pady=(4, 0))
        tk.Label(tr, text="↗ ", font=("Segoe UI", 9),
                 fg=ACCENT_GREEN, bg=WHITE).pack(side="left")
        tk.Label(tr, text=trend_text, font=("Segoe UI", 9),
                 fg=ACCENT_GREEN, bg=WHITE).pack(side="left")

    if subtitle:
        tk.Label(pad, text=subtitle, font=("Segoe UI", 9),
                 fg=TEXT_MUTED, bg=WHITE, anchor="w").pack(fill="x", pady=(4, 0))


def _dept_bar(parent, dept_name, count, total):
    row = tk.Frame(parent, bg=WHITE)
    row.pack(fill="x", pady=6)
    top = tk.Frame(row, bg=WHITE)
    top.pack(fill="x")
    tk.Label(top, text=dept_name, font=("Segoe UI", 9, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")
    tk.Label(top, text=f"{count:,} students", font=("Segoe UI", 9),
             fg=TEXT_MUTED, bg=WHITE).pack(side="right")
    track = tk.Frame(row, bg="#e5e7eb", height=6)
    track.pack(fill="x", pady=(4, 0))
    tk.Frame(track, bg=NAV_BG, height=6).place(
        relx=0, rely=0, relheight=1, relwidth=min(count / total, 1.0)
    )


def open_admin_dashboard(window, on_logout=None):
    win = tk.Toplevel(window)
    win.title("Admin Dashboard — EDU SIS")
    win.geometry("1500x900")
    win.minsize(1280, 760)
    win.configure(bg=NAV_BG)

    apply_window_icon(win, calling_file=__file__)

    win.columnconfigure(0, weight=0, minsize=270)
    win.columnconfigure(1, weight=1)
    win.rowconfigure(0, weight=1)

    # ── SIDEBAR (Canvas-based for bulletproof navy bg rendering) ──────────────
    SIDEBAR_W = 270
    sidebar_canvas = tk.Canvas(win, width=SIDEBAR_W, bg=NAV_BG,
                               highlightthickness=0, borderwidth=0,
                               bd=0, relief="flat")
    sidebar_canvas.grid(row=0, column=0, sticky="nsew")

    # Inner frame holds the actual sidebar widgets, painted on top of canvas bg
    sidebar = tk.Frame(sidebar_canvas, bg=NAV_BG,
                       highlightthickness=0, bd=0)
    _sb_window = sidebar_canvas.create_window(0, 0, anchor="nw",
                                              window=sidebar,
                                              width=SIDEBAR_W)

    def _resize_sidebar(e):
        sidebar_canvas.itemconfig(_sb_window,
                                  width=e.width, height=e.height)
        # Repaint a navy rectangle covering the full canvas
        sidebar_canvas.delete("bg")
        sidebar_canvas.create_rectangle(0, 0, e.width, e.height,
                                        fill=NAV_BG, outline="",
                                        tags="bg")
        sidebar_canvas.tag_lower("bg")

    sidebar_canvas.bind("<Configure>", _resize_sidebar)

    logo_row = tk.Frame(sidebar, bg=NAV_BG, highlightthickness=0, bd=0)
    logo_row.pack(fill="x", padx=18, pady=(22, 14))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir  = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "assets"))

    try:
        _img   = Image.open(os.path.join(assets_dir, "edu-crest-white.png")).resize((68, 68), Image.LANCZOS)
        _photo = ImageTk.PhotoImage(_img)
        lbl_logo = tk.Label(logo_row, image=_photo, bg=NAV_BG,
                            highlightthickness=0, bd=0)
        lbl_logo.image = _photo
        lbl_logo.pack(side="left", padx=(0, 12))
    except Exception:
        pass

    text_col = tk.Frame(logo_row, bg=NAV_BG, highlightthickness=0, bd=0)
    text_col.pack(side="left")
    tk.Label(text_col, text="ENCHONG DEE\nUNIVERSITY",
             font=("Segoe UI", 13, "bold"), fg=WHITE, bg=NAV_BG,
             justify="left", anchor="w").pack(anchor="w")
    tk.Label(text_col, text="STUDENT INFORMATION SYSTEM",
             font=("Segoe UI", 7), fg="#8fa8cc", bg=NAV_BG,
             justify="left", anchor="w").pack(anchor="w")

    tk.Frame(sidebar, bg="#1a3a6b", height=1,
             highlightthickness=0, bd=0).pack(fill="x", padx=14, pady=(6, 10))

    nav = tk.Frame(sidebar, bg=NAV_BG)
    nav.pack(fill="x", padx=4)

    _make_nav_btn(nav, "Dashboard",   "⊞", active=True)
    _make_nav_btn(nav, "Shortcuts",   "↗")
    _section_label(nav, "MANAGEMENT")
    _make_nav_btn(nav, "Add Student", "+")
    _make_nav_btn(nav, "Edit Student","✎")
    _make_nav_btn(nav, "Remove",      "✕")
    _section_label(nav, "SYSTEM")
    _make_nav_btn(nav, "Search",      "🔍")
    _make_nav_btn(nav, "Reports",     "📄")
    _make_nav_btn(nav, "Settings",    "⚙")

    # Logout at bottom
    bottom = tk.Frame(sidebar, bg=NAV_BG, highlightthickness=0, bd=0)
    bottom.pack(side="bottom", fill="x", padx=4, pady=14)
    tk.Frame(bottom, bg="#1a3a6b", height=1,
             highlightthickness=0, bd=0).pack(fill="x", padx=14, pady=(0, 10))

    logout_f = tk.Frame(bottom, bg=NAV_BG, cursor="hand2",
                        highlightthickness=0, bd=0)
    logout_f.pack(fill="x")
    logout_inner = tk.Frame(logout_f, bg=NAV_BG, highlightthickness=0, bd=0)
    logout_inner.pack(fill="x", padx=10, pady=11)
    lbl_logout_icon = tk.Label(logout_inner, text="◼", font=("Segoe UI", 16),
                               fg=ACCENT_RED, bg=NAV_BG)
    lbl_logout_icon.pack(side="left", padx=(6, 14))
    lbl_logout_text = tk.Label(logout_inner, text="Logout", font=("Segoe UI", 14),
                               fg=ACCENT_RED, bg=NAV_BG, anchor="w")
    lbl_logout_text.pack(side="left")

    def do_logout():
        win.destroy()
        if on_logout:
            on_logout()

    for w in (logout_f, logout_inner, lbl_logout_icon, lbl_logout_text):
        w.bind("<Button-1>", lambda e: do_logout())

    # ── CONTENT AREA ──────────────────────────────────────────────────────────
    content = tk.Frame(win, bg=CONTENT_BG)
    content.grid(row=0, column=1, sticky="nsew")
    content.rowconfigure(2, weight=1)
    content.columnconfigure(0, weight=1)

    # ── TOP BAR ───────────────────────────────────────────────────────────────
    topbar = tk.Frame(content, bg=WHITE, height=62)
    topbar.grid(row=0, column=0, sticky="ew")
    topbar.grid_propagate(False)

    topbar_inner = tk.Frame(topbar, bg=WHITE)
    topbar_inner.pack(fill="both", expand=True, padx=20)

    left_top = tk.Frame(topbar_inner, bg=WHITE)
    left_top.pack(side="left", fill="y")

    tk.Label(left_top, text="Dashboard", font=("Segoe UI", 13, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE).pack(side="left", padx=(0, 16), pady=18)
    tk.Frame(left_top, bg=SEPARATOR, width=1).pack(side="left", fill="y", pady=14)

    search_bg = tk.Frame(left_top, bg="#f3f4f6")
    search_bg.pack(side="left", padx=(16, 0), pady=14)
    tk.Label(search_bg, text="🔍", font=("Segoe UI", 10),
             fg=TEXT_MUTED, bg="#f3f4f6").pack(side="left", padx=(8, 2))
    search_entry = tk.Entry(search_bg, font=("Segoe UI", 10),
                            fg=TEXT_MUTED, bg="#f3f4f6",
                            relief="flat", bd=0, width=26)
    search_entry.insert(0, "Search student ID or name...")
    search_entry.pack(side="left", pady=8, padx=(0, 10))

    def _focus_in(e):
        if search_entry.get() == "Search student ID or name...":
            search_entry.delete(0, "end")
            search_entry.config(fg=TEXT_PRIMARY)

    def _focus_out(e):
        if not search_entry.get().strip():
            search_entry.insert(0, "Search student ID or name...")
            search_entry.config(fg=TEXT_MUTED)

    search_entry.bind("<FocusIn>",  _focus_in)
    search_entry.bind("<FocusOut>", _focus_out)

    right_top = tk.Frame(topbar_inner, bg=WHITE)
    right_top.pack(side="right", fill="y")

    user_btn = tk.Frame(right_top, bg="#f3f4f6", cursor="hand2")
    user_btn.pack(side="right", pady=14, padx=(8, 0))
    tk.Label(user_btn, text="👤  Admin User", font=("Segoe UI", 10),
             fg=TEXT_PRIMARY, bg="#f3f4f6").pack(padx=12, pady=6)

    tk.Label(right_top, text="❓", font=("Segoe UI", 14),
             fg=TEXT_MUTED, bg=WHITE, cursor="hand2").pack(side="right", padx=6)
    tk.Label(right_top, text="🔔", font=("Segoe UI", 14),
             fg=TEXT_MUTED, bg=WHITE, cursor="hand2").pack(side="right", padx=6)

    tk.Frame(content, bg=SEPARATOR, height=1).grid(row=1, column=0, sticky="ew")

    # ── SCROLLABLE MAIN AREA ──────────────────────────────────────────────────
    scroll_wrap = tk.Frame(content, bg=CONTENT_BG)
    scroll_wrap.grid(row=2, column=0, sticky="nsew")
    scroll_wrap.rowconfigure(0, weight=1)
    scroll_wrap.columnconfigure(0, weight=1)

    canvas = tk.Canvas(scroll_wrap, bg=CONTENT_BG, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    vsb = tk.Scrollbar(scroll_wrap, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=vsb.set)

    main_frame = tk.Frame(canvas, bg=CONTENT_BG)
    cw = canvas.create_window((0, 0), window=main_frame, anchor="nw")

    main_frame.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

    # ── STAT CARDS ────────────────────────────────────────────────────────────
    cards_row = tk.Frame(main_frame, bg=CONTENT_BG)
    cards_row.pack(fill="x", padx=24, pady=(20, 16))

    _stat_card(cards_row, "Total Students",    "12,482", None,
               "👥", trend_text="2.4%  from last semester")
    _stat_card(cards_row, "Active Students",   "11,940",
               "⊙  Currently enrolled in 1+ courses",
               "✅", badge_text="Active",   badge_bg=ACCENT_GREEN)
    _stat_card(cards_row, "Inactive Students", "542",
               "⊙  Includes graduated & on-leave",
               "🚫", badge_text="Inactive", badge_bg=ACCENT_RED)

    # ── LOWER SECTION ─────────────────────────────────────────────────────────
    lower = tk.Frame(main_frame, bg=CONTENT_BG)
    lower.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    # ── STUDENTS TABLE ────────────────────────────────────────────────────────
    table_card = tk.Frame(lower, bg=NAV_BG)
    table_card.pack(side="left", fill="both", expand=True, padx=(0, 14))

    tk.Label(table_card, text="Students", font=("Segoe UI", 13, "bold"),
             fg=WHITE, bg=NAV_BG, anchor="w").pack(anchor="w", padx=16, pady=(14, 8))

    tree_holder = tk.Frame(table_card, bg=NAV_BG)
    tree_holder.pack(fill="both", expand=True, padx=10, pady=(0, 14))

    style = tkttk.Style()
    style.configure("AdminTree.Treeview",
                    background=TABLE_BG, foreground=WHITE,
                    fieldbackground=TABLE_BG, rowheight=30,
                    font=("Segoe UI", 10))
    style.configure("AdminTree.Treeview.Heading",
                    background="#0d1f40", foreground=WHITE,
                    font=("Segoe UI", 10, "bold"), relief="flat")
    style.map("AdminTree.Treeview",
              background=[("selected", "#1e5496")],
              foreground=[("selected", WHITE)])

    tree = tkttk.Treeview(tree_holder,
                           columns=("id", "name", "course", "year"),
                           show="headings",
                           style="AdminTree.Treeview",
                           height=14)
    tree.heading("id",     text="ID")
    tree.heading("name",   text="Name")
    tree.heading("course", text="Course")
    tree.heading("year",   text="Year")
    tree.column("id",     width=100, anchor="center", minwidth=80)
    tree.column("name",   width=200, anchor="w",      minwidth=140)
    tree.column("course", width=200, anchor="center", minwidth=130)
    tree.column("year",   width=70,  anchor="center", minwidth=50)

    DEMO_STUDENTS = [
        ("25-0001", "Juan Dela Cruz",   "BS Computer Science",     "2nd"),
        ("25-0002", "Maria Santos",     "BS Nursing",               "3rd"),
        ("25-0003", "Carlos Reyes",     "BS Education",             "1st"),
        ("25-0004", "Ana Flores",       "BS Accountancy",           "4th"),
        ("25-0005", "Miguel Torres",    "BS Computer Science",      "1st"),
        ("25-0006", "Sophia Garcia",    "BS Medical Technology",    "2nd"),
        ("25-0007", "Luis Mendoza",     "BS Engineering",           "3rd"),
        ("25-0008", "Isabella Ramos",   "BS Psychology",            "2nd"),
        ("25-0009", "Rafael Cruz",      "BS Nursing",               "1st"),
        ("25-0010", "Patricia Lim",     "BS Accountancy",           "3rd"),
    ]
    for row in DEMO_STUDENTS:
        tree.insert("", "end", values=row)

    tree_vsb = tkttk.Scrollbar(tree_holder, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    tree_vsb.pack(side="right", fill="y")

    # ── RIGHT PANEL ───────────────────────────────────────────────────────────
    right_panel = tk.Frame(lower, bg=CONTENT_BG, width=300)
    right_panel.pack(side="left", fill="both")
    right_panel.pack_propagate(False)

    # Campus card — actual campus night photo
    campus_h = 160
    campus_frame = tk.Frame(right_panel, bg="#0d2447", height=campus_h)
    campus_frame.pack(fill="x", pady=(0, 14))
    campus_frame.pack_propagate(False)

    try:
        _camp_raw   = Image.open(os.path.join(assets_dir, "campus.png"))
        _camp_ratio = _camp_raw.width / _camp_raw.height
        _camp_w     = int(campus_h * _camp_ratio)
        _camp_img   = _camp_raw.resize((_camp_w, campus_h), Image.LANCZOS)
        _camp_photo = ImageTk.PhotoImage(_camp_img)
        campus_lbl  = tk.Label(campus_frame, image=_camp_photo, bg="#0d2447")
        campus_lbl.image = _camp_photo
        campus_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception:
        pass

    # Semi-transparent gradient overlay at the bottom via a dark frame
    campus_overlay = tk.Frame(campus_frame, bg="#0d1732")
    campus_overlay.place(relx=0, rely=0.52, relwidth=1, relheight=0.50)
    tk.Label(campus_overlay, text="Enchong Dee University Main Campus",
             font=("Segoe UI", 9, "bold"), fg=WHITE, bg="#0d1732",
             anchor="w", wraplength=270, justify="left").pack(anchor="w", padx=12, pady=(6, 2))
    tk.Label(campus_overlay,
             text="Summer 2026 Enrollment is now at 92% capacity.",
             font=("Segoe UI", 8), fg="#aab4c8", bg="#0d1732",
             anchor="w", wraplength=270, justify="left").pack(anchor="w", padx=12)

    # Department Load card
    dept_outer = tk.Frame(right_panel, bg=CARD_BORDER)
    dept_outer.pack(fill="x")
    dept_white = tk.Frame(dept_outer, bg=WHITE)
    dept_white.pack(padx=1, pady=1, fill="both", expand=True)
    dept_pad = tk.Frame(dept_white, bg=WHITE)
    dept_pad.pack(fill="both", padx=16, pady=14)

    tk.Label(dept_pad, text="Department Load", font=("Segoe UI", 11, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 10))

    TOTAL = 12482
    _dept_bar(dept_pad, "STEM Programs",    4203, TOTAL)
    _dept_bar(dept_pad, "Medical Sciences", 3115, TOTAL)
    _dept_bar(dept_pad, "Liberal Arts",     2890, TOTAL)

    tk.Button(dept_pad, text="View Full Analytics",
              font=("Segoe UI", 10), fg=TEXT_PRIMARY, bg=WHITE,
              relief="solid", bd=1, cursor="hand2", pady=6,
              activebackground="#f3f4f6").pack(fill="x", pady=(14, 0))
