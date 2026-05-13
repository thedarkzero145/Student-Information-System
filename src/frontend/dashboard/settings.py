import tkinter as tk
from tkinter import ttk as tkttk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
CONTENT_BG    = "#edf0f5"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#e2e8f0"

def build_settings_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=CONTENT_BG)
    container.pack(fill="both", expand=True, padx=32, pady=32)

    # Header
    tk.Label(container, text="System Settings", font=("Segoe UI", 16, "bold"), fg=TEXT_PRIMARY, bg=CONTENT_BG).pack(anchor="w", pady=(0, 24))

    # Main Card
    card_outer = tk.Frame(container, bg=CARD_BORDER)
    card_outer.pack(fill="both", expand=True)
    card_bg = tk.Frame(card_outer, bg=CARD_BG)
    card_bg.pack(padx=1, pady=1, fill="both", expand=True)

    # Layout: 2 Columns for settings
    cols = tk.Frame(card_bg, bg=CARD_BG)
    cols.pack(fill="both", expand=True, padx=32, pady=32)

    left_col = tk.Frame(cols, bg=CARD_BG)
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 16))

    right_col = tk.Frame(cols, bg=CARD_BG)
    right_col.pack(side="left", fill="both", expand=True, padx=(16, 0))

    # --- LEFT COL: Profile & Academic ---
    tk.Label(left_col, text="Academic Profile", font=("Segoe UI", 12, "bold"), fg=NAV_BG, bg=CARD_BG).pack(anchor="w", pady=(0, 16))

    def _make_field(parent, label, value, disabled=False):
        f = tk.Frame(parent, bg=CARD_BG)
        f.pack(fill="x", pady=(0, 16))
        tk.Label(f, text=label, font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
        
        entry_wrap = tk.Frame(f, bg=CARD_BORDER if disabled else "#cbd5e1", highlightthickness=0, bd=0)
        entry_wrap.pack(fill="x")
        
        bg_col = "#f1f5f9" if disabled else WHITE
        fg_col = "#94a3b8" if disabled else TEXT_PRIMARY
        
        entry_inner = tk.Frame(entry_wrap, bg=bg_col)
        entry_inner.pack(padx=1, pady=1, fill="x")
        
        e = tk.Entry(entry_inner, font=("Segoe UI", 10), bg=bg_col, fg=fg_col, relief="flat", disabledbackground=bg_col, disabledforeground=fg_col)
        e.pack(fill="x", padx=12, pady=8)
        e.insert(0, value)
        if disabled:
            e.config(state="disabled")

    _make_field(left_col, "Student Name", "Juan Dela Cruz", disabled=True)
    _make_field(left_col, "Student ID", "25-2751", disabled=True)
    
    # Department Dropdown (Grayed out/Disabled as requested)
    dept_f = tk.Frame(left_col, bg=CARD_BG)
    dept_f.pack(fill="x", pady=(0, 16))
    tk.Label(dept_f, text="Department", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
    
    dept_wrap = tk.Frame(dept_f, bg=CARD_BORDER, highlightthickness=0)
    dept_wrap.pack(fill="x")
    dept_inner = tk.Frame(dept_wrap, bg="#f1f5f9")
    dept_inner.pack(padx=1, pady=1, fill="x")
    
    # Simulate a disabled dropdown visually
    lbl = tk.Label(dept_inner, text="BS Information Technology", font=("Segoe UI", 10), bg="#f1f5f9", fg="#94a3b8")
    lbl.pack(side="left", padx=12, pady=8)
    tk.Label(dept_inner, text="▼", font=("Segoe UI", 8), bg="#f1f5f9", fg="#94a3b8").pack(side="right", padx=12)

    # --- RIGHT COL: Preferences ---
    tk.Label(right_col, text="System Preferences", font=("Segoe UI", 12, "bold"), fg=NAV_BG, bg=CARD_BG).pack(anchor="w", pady=(0, 16))



    # Notifications
    notif_f = tk.Frame(right_col, bg=CARD_BG)
    notif_f.pack(fill="x", pady=(0, 16))
    tk.Label(notif_f, text="Email Notifications", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", pady=(0, 8))
    
    # Custom simple checkbox UI for aesthetics
    def _make_checkbox(parent, text, checked=True):
        row = tk.Frame(parent, bg=CARD_BG)
        row.pack(fill="x", pady=4)
        box = tk.Label(row, text="☑" if checked else "☐", font=("Segoe UI Emoji", 14), fg="#22c55e" if checked else TEXT_MUTED, bg=CARD_BG)
        box.pack(side="left")
        tk.Label(row, text=text, font=("Segoe UI", 10), fg=TEXT_PRIMARY, bg=CARD_BG).pack(side="left", padx=(8, 0))
        
    _make_checkbox(notif_f, "New Announcements", True)
    _make_checkbox(notif_f, "Grade Updates", True)
    _make_checkbox(notif_f, "Event Reminders", False)

    # Note: Two Factor Authentication explicitly removed from here per user request.

    # Footer Save Button
    footer = tk.Frame(card_bg, bg=CARD_BG)
    footer.pack(fill="x", side="bottom", padx=32, pady=32)
    
    tk.Frame(card_bg, bg=CARD_BORDER, height=1).pack(fill="x", side="bottom")

    btn_wrap = tk.Frame(footer, bg=NAV_BG, highlightthickness=0, cursor="hand2")
    btn_wrap.pack(side="right")
    inner_btn = tk.Frame(btn_wrap, bg=NAV_BG, padx=24, pady=8)
    inner_btn.pack()
    tk.Label(inner_btn, text="Save Changes", font=("Segoe UI", 10, "bold"), fg=WHITE, bg=NAV_BG).pack()
