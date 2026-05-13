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

DASHBOARD_VERSION = "v5-figma-match"

# Store buttons for active state toggling
nav_btns = {}

# ── Helper: nav button ─────────────────────────────────────────────────────────
def _make_nav_btn(parent, text, icon, command=None):
    f = tk.Frame(parent, bg=NAV_BG, cursor="hand2", highlightthickness=0, bd=0)
    f.pack(fill="x", pady=1)
    inner = tk.Frame(f, bg=NAV_BG, highlightthickness=0, bd=0)
    inner.pack(fill="x", padx=8, pady=10)
    
    # Store references to images if any are used, to prevent garbage collection
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


# ── Helper: department load bar ────────────────────────────────────────────────
def _dept_bar(parent, dept_name, count, total):
    row = tk.Frame(parent, bg=WHITE)
    row.pack(fill="x", pady=5)

    hdr = tk.Frame(row, bg=WHITE)
    hdr.pack(fill="x")
    tk.Label(hdr, text=dept_name, font=("Segoe UI", 9, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")
    tk.Label(hdr, text=f"{count:,} students", font=("Segoe UI", 9),
             fg=TEXT_MUTED, bg=WHITE).pack(side="right")

    track = tk.Frame(row, bg=DEPT_BAR_TRACK, height=6)
    track.pack(fill="x", pady=(4, 0))
    fill_w = min(count / total, 1.0)
    tk.Frame(track, bg=DEPT_BAR_BG, height=6).place(
        relx=0, rely=0, relheight=1, relwidth=fill_w)

# ── VIEW BUILDERS ────────────────────────────────────────────────────────────
def build_dashboard_tab(parent, switch_cb):
    # ── STAT CARDS ────────────────────────────────────────────────────────────
    cards_row = tk.Frame(parent, bg=CONTENT_BG)
    cards_row.pack(fill="x", padx=24, pady=(22, 16))

    _stat_card(cards_row, "Total Students",    "12,482", None,
               "👥", trend_text="2.4%  from last semester")
    _stat_card(cards_row, "Active Students",   "11,940",
               "⊙  Currently enrolled in 1+ courses",
               "✅", badge_text="Active",   badge_bg=BADGE_GREEN_BG)
    _stat_card(cards_row, "Inactive Students", "542",
               "⊙  Includes graduated & on-leave",
               "🚫", badge_text="Inactive", badge_bg=BADGE_RED_BG)

    # ── LOWER ROW ─────────────────────────────────────────────────────────────
    lower = tk.Frame(parent, bg=CONTENT_BG)
    lower.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    # ── STUDENTS TABLE (dark navy card) ───────────────────────────────────────
    table_card = tk.Frame(lower, bg=TABLE_OUTER,
                          highlightthickness=0, bd=0)
    table_card.pack(side="left", fill="both", expand=True, padx=(0, 16))

    tk.Label(table_card, text="Students", font=("Segoe UI", 12, "bold"),
             fg=WHITE, bg=TABLE_OUTER, anchor="w").pack(anchor="w",
                                                        padx=16, pady=(14, 10))

    # Table inner area (light grey)
    tree_holder = tk.Frame(table_card, bg="#c8cdd8",
                           highlightthickness=0, bd=0)
    tree_holder.pack(fill="both", expand=True, padx=10, pady=(0, 14))

    style = tkttk.Style()
    style.configure("FigmaTree.Treeview",
                    background="#d8dde8",
                    foreground=TEXT_PRIMARY,
                    fieldbackground="#d8dde8",
                    rowheight=28,
                    font=("Segoe UI", 10))
    style.configure("FigmaTree.Treeview.Heading",
                    background="#c0c6d4",
                    foreground=TEXT_PRIMARY,
                    font=("Segoe UI", 10, "bold"),
                    relief="flat")
    style.map("FigmaTree.Treeview",
              background=[("selected", "#a0b4d0")],
              foreground=[("selected", TEXT_PRIMARY)])

    tree = tkttk.Treeview(tree_holder,
                          columns=("id", "name", "course", "year"),
                          show="headings",
                          style="FigmaTree.Treeview",
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
        ("25-0001", "Juan Dela Cruz",  "BS Computer Science",  "2nd"),
        ("25-0002", "Maria Santos",    "BS Nursing",           "3rd"),
        ("25-0003", "Carlos Reyes",    "BS Education",         "1st"),
        ("25-0004", "Ana Flores",      "BS Accountancy",       "4th"),
        ("25-0005", "Miguel Torres",   "BS Computer Science",  "1st"),
        ("25-0006", "Sophia Garcia",   "BS Medical Technology","2nd"),
        ("25-0007", "Luis Mendoza",    "BS Engineering",       "3rd"),
        ("25-0008", "Isabella Ramos",  "BS Psychology",        "2nd"),
        ("25-0009", "Rafael Cruz",     "BS Nursing",           "1st"),
        ("25-0010", "Patricia Lim",    "BS Accountancy",       "3rd"),
    ]
    for row in DEMO_STUDENTS:
        tree.insert("", "end", values=row)

    # Double click opens student profile
    tree.bind("<Double-1>", lambda e: switch_cb("Student Profile"))

    tree_vsb = tkttk.Scrollbar(tree_holder, orient="vertical",
                                command=tree.yview)
    tree.configure(yscrollcommand=tree_vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    tree_vsb.pack(side="right", fill="y")

    # ── RIGHT PANEL ───────────────────────────────────────────────────────────
    right_panel = tk.Frame(lower, bg=CONTENT_BG, width=290)
    right_panel.pack(side="left", fill="both")
    right_panel.pack_propagate(False)

    # Campus image card
    campus_h = 130
    campus_frame = tk.Frame(right_panel, bg="#0d2447", height=campus_h)
    campus_frame.pack(fill="x", pady=(0, 14))
    campus_frame.pack_propagate(False)

    campus_overlay = tk.Frame(campus_frame, bg="#0d2447")
    campus_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    tk.Label(campus_overlay, text="Enchong Dee University Main Campus",
             font=("Segoe UI", 11, "bold"), fg=WHITE, bg="#0d2447",
             anchor="w", wraplength=260, justify="left").pack(anchor="w",
                                                              padx=16, pady=(24, 4))
    tk.Label(campus_overlay,
             text="Summer 2026 Enrollment is now at 92% capacity.",
             font=("Segoe UI", 9), fg="#aab4c8", bg="#0d2447",
             anchor="w", wraplength=260, justify="left").pack(anchor="w", padx=16)

    # Department Load card
    dept_outer = tk.Frame(right_panel, bg=CARD_BORDER)
    dept_outer.pack(fill="x")
    dept_white = tk.Frame(dept_outer, bg=WHITE)
    dept_white.pack(padx=1, pady=1, fill="both", expand=True)
    dept_pad = tk.Frame(dept_white, bg=WHITE)
    dept_pad.pack(fill="both", padx=16, pady=14)

    tk.Label(dept_pad, text="Department Load", font=("Segoe UI", 11, "bold"),
             fg=TEXT_PRIMARY, bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 8))

    TOTAL = 12482
    _dept_bar(dept_pad, "STEM Programs",    4203, TOTAL)
    _dept_bar(dept_pad, "Medical Sciences", 3115, TOTAL)
    _dept_bar(dept_pad, "Liberal Arts",     2890, TOTAL)

    tk.Button(dept_pad, text="View Full Analytics",
              font=("Segoe UI", 10), fg=TEXT_PRIMARY, bg=WHITE,
              relief="solid", bd=1, cursor="hand2", pady=6,
              activebackground="#f3f4f6").pack(fill="x", pady=(14, 0))

def build_student_profile_tab(parent, switch_cb):
    # Top breadcrumb
    bc = tk.Frame(parent, bg=CONTENT_BG)
    bc.pack(fill="x", padx=24, pady=(16, 10))
    tk.Label(bc, text="Student Profile", font=("Segoe UI", 12, "bold"),
             fg=TEXT_PRIMARY, bg=CONTENT_BG).pack(side="left")
    
    # 2 columns layout
    cols = tk.Frame(parent, bg=CONTENT_BG)
    cols.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    # LEFT COLUMN (Profile Summary)
    left_col = tk.Frame(cols, bg=CARD_BORDER, width=320)
    left_col.pack(side="left", fill="y", padx=(0, 16))
    left_col.pack_propagate(False)
    
    left_inner = tk.Frame(left_col, bg=CARD_BG)
    left_inner.pack(padx=1, pady=1, fill="both", expand=True)
    
    # Avatar
    avatar_wrap = tk.Frame(left_inner, bg=CARD_BG, pady=24)
    avatar_wrap.pack(fill="x")
    avatar = tk.Label(avatar_wrap, text="👤", font=("Segoe UI Emoji", 48), fg="#cbd5e1", bg="#f1f5f9", width=3, height=1)
    avatar.pack(pady=10)
    
    tk.Label(left_inner, text="Juan Dela Cruz", font=("Segoe UI", 16, "bold"), fg=NAV_BG, bg=CARD_BG).pack()
    tk.Label(left_inner, text="B.Sc. Information Technology", font=("Segoe UI", 10), fg=TEXT_MUTED, bg=CARD_BG).pack()
    
    # Badges
    badges = tk.Frame(left_inner, bg=CARD_BG)
    badges.pack(pady=12)
    tk.Label(badges, text="Enrolled", font=("Segoe UI", 9, "bold"), fg="#16a34a", bg="#dcfce7", padx=8, pady=2).pack(side="left", padx=4)
    tk.Label(badges, text="Freshman Year", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg="#f1f5f9", padx=8, pady=2).pack(side="left", padx=4)
    
    # Details
    det = tk.Frame(left_inner, bg=CARD_BG)
    det.pack(fill="x", padx=24, pady=16)
    
    def _detail_row(p, label, val):
        r = tk.Frame(p, bg=CARD_BG)
        r.pack(fill="x", pady=6)
        tk.Label(r, text=label, font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left")
        tk.Label(r, text=val, font=("Segoe UI", 10), fg=TEXT_PRIMARY, bg=CARD_BG).pack(side="right")
        
    _detail_row(det, "Student ID", "SIS-2024-8842")
    _detail_row(det, "Admission Date", "August 04, 2026")
    _detail_row(det, "Email Address", "cleven.castillo10@plv.edu")
    _detail_row(det, "Phone", "+1 (555) 012-3456")
    
    # Bottom Academic Summary Card
    acad = tk.Frame(left_inner, bg=NAV_BG)
    acad.pack(fill="x", side="bottom", padx=16, pady=16)
    tk.Label(acad, text="Academic Summary", font=("Segoe UI", 9), fg=WHITE, bg=NAV_BG).pack(anchor="w", padx=12, pady=(12, 4))
    
    acad_grid = tk.Frame(acad, bg=NAV_BG)
    acad_grid.pack(fill="x", padx=12, pady=(0, 12))
    cgpa = tk.Frame(acad_grid, bg="#1a3a7a")
    cgpa.pack(side="left", fill="both", expand=True, padx=(0, 4))
    tk.Label(cgpa, text="CGPA", font=("Segoe UI", 8), fg="#aab4c8", bg="#1a3a7a").pack(anchor="w", padx=8, pady=(8, 0))
    tk.Label(cgpa, text="3.92", font=("Segoe UI", 16, "bold"), fg=WHITE, bg="#1a3a7a").pack(anchor="w", padx=8, pady=(0, 8))
    
    cred = tk.Frame(acad_grid, bg="#1a3a7a")
    cred.pack(side="right", fill="both", expand=True, padx=(4, 0))
    tk.Label(cred, text="Credits", font=("Segoe UI", 8), fg="#aab4c8", bg="#1a3a7a").pack(anchor="w", padx=8, pady=(8, 0))
    tk.Label(cred, text="112/128", font=("Segoe UI", 16, "bold"), fg=WHITE, bg="#1a3a7a").pack(anchor="w", padx=8, pady=(0, 8))

    # RIGHT COLUMN
    right_col = tk.Frame(cols, bg=CARD_BORDER)
    right_col.pack(side="left", fill="both", expand=True)
    
    right_inner = tk.Frame(right_col, bg=CARD_BG)
    right_inner.pack(padx=1, pady=1, fill="both", expand=True)
    
    # Tabs inside right col
    tab_hdr = tk.Frame(right_inner, bg="#f8fafc")
    tab_hdr.pack(fill="x")
    tk.Label(tab_hdr, text="Academic Info", font=("Segoe UI", 10, "bold"), fg=NAV_BG, bg=CARD_BG, padx=16, pady=12).pack(side="left")
    tk.Frame(tab_hdr, bg=CARD_BORDER, height=1).pack(side="bottom", fill="x")
    
    content = tk.Frame(right_inner, bg=CARD_BG)
    content.pack(fill="both", expand=True, padx=24, pady=24)
    
    row1 = tk.Frame(content, bg=CARD_BG)
    row1.pack(fill="x")
    
    maj_card = tk.Frame(row1, bg="#f8fafc", highlightthickness=1, highlightbackground=CARD_BORDER, bd=0)
    maj_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
    tk.Label(maj_card, text="PRIMARY MAJOR", font=("Segoe UI", 8, "bold"), fg=NAV_BG, bg="#f8fafc").pack(anchor="w", padx=16, pady=(16, 4))
    tk.Label(maj_card, text="School of Engineering", font=("Segoe UI", 11, "bold"), fg=TEXT_PRIMARY, bg="#f8fafc").pack(anchor="w", padx=16)
    tk.Label(maj_card, text="Computer Science Concentration", font=("Segoe UI", 9), fg=TEXT_MUTED, bg="#f8fafc").pack(anchor="w", padx=16, pady=(0, 16))
    
    adv_card = tk.Frame(row1, bg="#f8fafc", highlightthickness=1, highlightbackground=CARD_BORDER, bd=0)
    adv_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
    tk.Label(adv_card, text="ACADEMIC ADVISOR", font=("Segoe UI", 8, "bold"), fg=NAV_BG, bg="#f8fafc").pack(anchor="w", padx=16, pady=(16, 4))
    adv_in = tk.Frame(adv_card, bg="#f8fafc")
    adv_in.pack(fill="x", padx=16, pady=(0, 16))
    tk.Label(adv_in, text="👤", font=("Segoe UI", 18), bg="#e2e8f0").pack(side="left", padx=(0, 10))
    a_t = tk.Frame(adv_in, bg="#f8fafc")
    a_t.pack(side="left")
    tk.Label(a_t, text="Mr. John Christian Lor, MSIT", font=("Segoe UI", 10, "bold"), fg=TEXT_PRIMARY, bg="#f8fafc").pack(anchor="w")
    tk.Label(a_t, text="Senior Professor", font=("Segoe UI", 9), fg=TEXT_MUTED, bg="#f8fafc").pack(anchor="w")
    
    tk.Label(content, text="SCHOLARSHIPS & HONORS", font=("Segoe UI", 9, "bold"), fg=NAV_BG, bg=CARD_BG).pack(anchor="w", pady=(32, 8))
    
    schol = tk.Frame(content, bg=CARD_BG, highlightthickness=1, highlightbackground=CARD_BORDER, bd=0)
    schol.pack(fill="x", ipady=40)
    # Dashed effect simulated with a flat border for now
    tk.Label(schol, text="🎖️", font=("Segoe UI Emoji", 24), bg=CARD_BG).pack(pady=(20, 4))
    tk.Label(schol, text="No records yet.", font=("Segoe UI", 12, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack()
    tk.Label(schol, text="Additional honors and scholarship awards will be\ndisplayed once verified by the registrar's office.", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG, justify="center").pack()

    # Buttons bottom
    btm = tk.Frame(right_inner, bg=CARD_BG)
    btm.pack(fill="x", side="bottom", padx=24, pady=24)
    
    tk.Button(btm, text="← Back to List", font=("Segoe UI", 10), cursor="hand2", command=lambda: switch_cb("Dashboard"),
              bg=WHITE, fg=TEXT_PRIMARY, relief="solid", bd=1, padx=16, pady=6).pack(side="left")
    
    tk.Button(btm, text="✎ Edit Record", font=("Segoe UI", 10, "bold"), cursor="hand2", command=lambda: switch_cb("Edit Student"),
              bg=NAV_BG, fg=WHITE, relief="flat", bd=0, padx=16, pady=6).pack(side="right")
    tk.Button(btm, text="Generate Report", font=("Segoe UI", 10), cursor="hand2",
              bg=WHITE, fg=TEXT_PRIMARY, relief="solid", bd=1, padx=16, pady=6).pack(side="right", padx=12)

def build_add_student_tab(parent, switch_cb):
    # Main container
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    # Title
    tk.Label(container, text="New Student Record", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(pady=(48, 32))

    # Form Container
    form = tk.Frame(container, bg=WHITE)
    form.pack(fill="both", expand=True, padx=120)

    def _make_field(parent_frame, label_text, placeholder, is_dropdown=False, is_date=False):
        f = tk.Frame(parent_frame, bg=WHITE)
        f.pack(fill="x", expand=True, padx=16, pady=(0, 24))
        
        tk.Label(f, text=label_text, font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 8))
        
        input_bg = "#f4f4f5" # light gray
        inner = tk.Frame(f, bg=input_bg, height=48)
        inner.pack(fill="x")
        inner.pack_propagate(False)
        
        if is_dropdown:
            style = tkttk.Style()
            style.configure("AddStudent.TCombobox", padding=5)
            cb = tkttk.Combobox(inner, font=("Segoe UI", 10), state="readonly", style="AddStudent.TCombobox")
            cb.pack(fill="both", expand=True, padx=2, pady=8)
            cb.set(placeholder)
            if label_text == "Course":
                cb['values'] = ["BS Computer Science", "BS Information Technology", "BS Nursing", "BS Education", "BS Accountancy"]
            elif label_text == "Year Level":
                cb['values'] = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
            return cb
        elif is_date:
            import ttkbootstrap as tb
            de = tb.DateEntry(inner)
            de.pack(fill="both", expand=True, padx=2, pady=8)
            return de
        else:
            e = tk.Entry(inner, font=("Segoe UI", 10), bg=input_bg, fg=TEXT_PRIMARY, relief="flat", bd=0, insertbackground=TEXT_PRIMARY)
            e.pack(fill="both", expand=True, padx=16, pady=12)
            e.insert(0, placeholder)
            return e

    # Row 1
    r1 = tk.Frame(form, bg=WHITE)
    r1.pack(fill="x")
    c1_1 = tk.Frame(r1, bg=WHITE); c1_1.pack(side="left", fill="both", expand=True)
    c1_2 = tk.Frame(r1, bg=WHITE); c1_2.pack(side="left", fill="both", expand=True)
    
    _make_field(c1_1, "Student ID", "26-1234")
    _make_field(c1_2, "Full name", "Surname, Full name, M.I")

    # Row 2
    r2 = tk.Frame(form, bg=WHITE)
    r2.pack(fill="x")
    c2_1 = tk.Frame(r2, bg=WHITE); c2_1.pack(side="left", fill="both", expand=True)
    c2_2 = tk.Frame(r2, bg=WHITE); c2_2.pack(side="left", fill="both", expand=True)
    
    _make_field(c2_1, "Course", "Select Course", is_dropdown=True)
    _make_field(c2_2, "Year Level", "Select Year", is_dropdown=True)

    # Row 3
    r3 = tk.Frame(form, bg=WHITE)
    r3.pack(fill="x")
    c3_1 = tk.Frame(r3, bg=WHITE); c3_1.pack(side="left", fill="both", expand=True)
    c3_2 = tk.Frame(r3, bg=WHITE); c3_2.pack(side="left", fill="both", expand=True)
    
    _make_field(c3_1, "Email Address", "student@university.edu")
    _make_field(c3_2, "Contact Number", "+63 000 000 0000")

    # Row 4 (Full width)
    r4 = tk.Frame(form, bg=WHITE)
    r4.pack(fill="x")
    _make_field(r4, "Home Address", "House No. , Street, Barangay, City, Province")

    # Row 5 (Status and Date)
    r5 = tk.Frame(form, bg=WHITE)
    r5.pack(fill="x")
    c5_1 = tk.Frame(r5, bg=WHITE); c5_1.pack(side="left", fill="both", expand=True, padx=16)
    c5_2 = tk.Frame(r5, bg=WHITE); c5_2.pack(side="left", fill="both", expand=True)
    
    # Status
    tk.Label(c5_1, text="Account Status", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 12))
    status_f = tk.Frame(c5_1, bg=WHITE)
    status_f.pack(anchor="w")
    
    status_var = tk.StringVar(value="Active")
    radio_btns = []
    
    def _update_radios():
        for rb in radio_btns:
            is_sel = (status_var.get() == rb['val'])
            rb['icon'].config(text="●" if is_sel else "○", fg=NAV_BG if is_sel else "#cbd5e1")

    def _radio(parent_frame, text):
        f = tk.Frame(parent_frame, bg=WHITE, cursor="hand2")
        f.pack(side="left", padx=(0, 24))
        
        lbl_icon = tk.Label(f, font=("Segoe UI Emoji", 14), bg=WHITE)
        lbl_icon.pack(side="left")
        lbl_text = tk.Label(f, text=text, font=("Segoe UI", 9), fg=TEXT_PRIMARY, bg=WHITE)
        lbl_text.pack(side="left", padx=(4, 0))
        
        radio_btns.append({'val': text, 'icon': lbl_icon})
        
        def _on_click(e):
            status_var.set(text)
            _update_radios()
            
        f.bind("<Button-1>", _on_click)
        lbl_icon.bind("<Button-1>", _on_click)
        lbl_text.bind("<Button-1>", _on_click)
    
    _radio(status_f, "Active")
    _radio(status_f, "Inactive")
    _update_radios()
    
    _make_field(c5_2, "Enrollment Date", "mm/dd/yy", is_date=True)

    # Notification callback
    def show_notification(e=None):
        notif = tk.Frame(container, bg="#10b981", highlightthickness=0)
        notif.place(relx=1.0, rely=0.0, x=-32, y=32, anchor="ne")
        tk.Label(notif, text="✓ Student record added successfully", font=("Segoe UI", 10, "bold"), fg=WHITE, bg="#10b981", padx=16, pady=12).pack()
        container.after(3000, notif.destroy)

    # Bottom Buttons
    footer = tk.Frame(form, bg=WHITE)
    footer.pack(fill="x", pady=(32, 48), padx=16)
    
    btn_add = tk.Button(footer, text="Add Student Record", font=("Segoe UI", 10, "bold"), fg=WHITE, bg=NAV_BG, relief="flat", padx=16, pady=6, cursor="hand2", command=show_notification)
    btn_add.pack(side="right")
    
    btn_cancel = tk.Button(footer, text="Cancel", font=("Segoe UI", 10, "bold"), fg=NAV_BG, bg=WHITE, relief="solid", bd=1, padx=16, pady=6, cursor="hand2")
    btn_cancel.pack(side="right", padx=(0, 16))

def build_edit_student_tab(parent, switch_cb):
    tk.Label(parent, text="Edit Student Record", font=("Segoe UI", 18, "bold"), fg=NAV_BG, bg=CONTENT_BG).pack(anchor="w", padx=32, pady=32)
    f = tk.Frame(parent, bg=CARD_BG, highlightthickness=1, highlightbackground=CARD_BORDER)
    f.pack(fill="both", expand=True, padx=32, pady=(0, 32))
    tk.Label(f, text="(Search and edit form fields will go here)", font=("Segoe UI", 12), fg=TEXT_MUTED, bg=CARD_BG).pack(expand=True)

def build_settings_tab(parent, switch_cb):
    tk.Label(parent, text="System Settings", font=("Segoe UI", 18, "bold"), fg=NAV_BG, bg=CONTENT_BG).pack(anchor="w", padx=32, pady=32)
    f = tk.Frame(parent, bg=CARD_BG, highlightthickness=1, highlightbackground=CARD_BORDER)
    f.pack(fill="both", expand=True, padx=32, pady=(0, 32))
    tk.Label(f, text="(Settings toggles and configurations will go here)", font=("Segoe UI", 12), fg=TEXT_MUTED, bg=CARD_BG).pack(expand=True)


# ── Main entry ─────────────────────────────────────────────────────────────────
def open_admin_dashboard(window, on_logout=None):

    win = tk.Toplevel(window)
    win.title(f"Admin Dashboard — EDU SIS")
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

    # ── TAB SWITCHING LOGIC ───────────────────────────────────────────────────
    current_tab_frame = None

    def switch_tab(tab_name):
        nonlocal current_tab_frame
        if current_tab_frame:
            current_tab_frame.destroy()
        
        main_frame = tk.Frame(content_wrap, bg=CONTENT_BG)
        main_frame.grid(row=0, column=0, sticky="nsew")
        current_tab_frame = main_frame

        _set_active_nav(tab_name)
        
        try:
            if 'topbar_title_lbl' in globals() or 'topbar_title_lbl' in locals() or 'topbar_title_lbl' in win.__dict__:
                win.topbar_title_lbl.config(text=tab_name)
        except Exception:
            pass

        if tab_name == "Dashboard" or tab_name == "Shortcuts":
            build_dashboard_tab(main_frame, switch_tab)
        elif tab_name == "Add Student":
            build_add_student_tab(main_frame, switch_tab)
        elif tab_name == "Edit Student":
            build_edit_student_tab(main_frame, switch_tab)
        elif tab_name == "Student Profile":
            build_student_profile_tab(main_frame, switch_tab)
        elif tab_name == "Settings":
            build_settings_tab(main_frame, switch_tab)
        else:
            tk.Label(main_frame, text=f"{tab_name}\n(Under Construction)", font=("Segoe UI", 20), fg=TEXT_MUTED, bg=CONTENT_BG, justify="center").pack(expand=True)
            
        win.after(50, lambda: _force_bg(main_frame))

    # Initialize buttons
    btn_dashboard, lbl_dash = _make_nav_btn(nav, "Dashboard",    "⊞", command=lambda: switch_tab("Dashboard"))
    btn_shortcuts, lbl_short = _make_nav_btn(nav, "Shortcuts",    "↗", command=lambda: switch_tab("Shortcuts"))
    _section_label(nav, "MANAGEMENT")
    btn_add, lbl_add = _make_nav_btn(nav, "Add Student",  "+", command=lambda: switch_tab("Add Student"))
    btn_edit, lbl_edit = _make_nav_btn(nav, "Edit Student", "✎", command=lambda: switch_tab("Edit Student"))
    btn_remove, lbl_rem = _make_nav_btn(nav, "Remove",       "✕", command=lambda: switch_tab("Remove"))
    _section_label(nav, "SYSTEM")
    btn_search, lbl_search = _make_nav_btn(nav, "Search",       "🔍", command=lambda: switch_tab("Search"))
    btn_reports, lbl_rep = _make_nav_btn(nav, "Reports",      "📄", command=lambda: switch_tab("Reports"))
    btn_settings, lbl_set = _make_nav_btn(nav, "Settings",     "⚙", command=lambda: switch_tab("Settings"))

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
    _apply_nav_icon(btn_shortcuts, lbl_short, "shortcut-64.png", (22, 22))
    _apply_nav_icon(btn_add, lbl_add, "add-64.png", (22, 22))
    _apply_nav_icon(btn_edit, lbl_edit, "edit-64.png", (22, 22))
    _apply_nav_icon(btn_remove, lbl_rem, "erase-64.png", (22, 22))
    _apply_nav_icon(btn_search, lbl_search, "search-64.png", (22, 22))
    _apply_nav_icon(btn_reports, lbl_rep, "reports-48.png", (22, 22))
    _apply_nav_icon(btn_settings, lbl_set, "settings-24.png", (22, 22))

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

    win.topbar_title_lbl = tk.Label(left_top, text="Dashboard", font=("Segoe UI", 12, "bold"),
             fg=WHITE, bg=NAV_BG)
    win.topbar_title_lbl.pack(side="left", padx=(0, 16), pady=0)
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
    
    # Updated to have a white background and black text on focus
    search_entry = tk.Entry(search_wrap, font=("Segoe UI", 10),
                            fg="#8fa8cc", bg=WHITE,
                            insertbackground="black",
                            relief="flat", bd=0, width=26)
    search_entry.insert(0, "Search student ID or name...")
    search_entry.pack(side="left", pady=4, padx=(4, 10))

    def _fi(e):
        if search_entry.get() == "Search student ID or name...":
            search_entry.delete(0, "end")
            search_entry.config(fg=TEXT_PRIMARY)

    def _fo(e):
        if not search_entry.get().strip():
            search_entry.insert(0, "Search student ID or name...")
            search_entry.config(fg="#8fa8cc")

    search_entry.bind("<FocusIn>",  _fi)
    search_entry.bind("<FocusOut>", _fo)

    # Right: Admin User pill button
    right_top = tk.Frame(tb_inner, bg=NAV_BG)
    right_top.pack(side="right", fill="y")

    admin_pill = tk.Frame(right_top, bg=NAV_BG,
                          highlightthickness=1,
                          highlightbackground="#4a6fa5",
                          highlightcolor="#4a6fa5", bd=0,
                          cursor="hand2")
    admin_pill.pack(side="right", pady=15)

    # Small avatar circle (simulated with a colored label)
    avatar_f = tk.Frame(admin_pill, bg="#2d4d8a",
                        width=26, height=26,
                        highlightthickness=0, bd=0)
    avatar_f.pack(side="left", padx=(8, 6), pady=6)
    avatar_f.pack_propagate(False)
    tk.Label(avatar_f, text="👤", font=("Segoe UI Emoji", 12),
             fg=WHITE, bg="#2d4d8a").place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(admin_pill, text="Admin User", font=("Segoe UI", 10),
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
    
    # Init default tab
    switch_tab("Dashboard")
    
    win.after(100, lambda: _force_bg(win))
