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
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    # Header
    tk.Label(container, text="System Settings", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(48, 32), padx=120)

    # Form Container
    form = tk.Frame(container, bg=WHITE)
    form.pack(fill="both", expand=True, padx=120)

    # Layout: 2 Columns
    col1 = tk.Frame(form, bg=WHITE)
    col1.pack(side="left", fill="both", expand=True, padx=(0, 16))

    col2 = tk.Frame(form, bg=WHITE)
    col2.pack(side="left", fill="both", expand=True, padx=(16, 0))

    # --- LEFT COL: Academic Profile ---
    tk.Label(col1, text="Academic Profile", font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 16))

    def _make_field(parent_frame, label_text, value, disabled=False):
        f = tk.Frame(parent_frame, bg=WHITE)
        f.pack(fill="x", pady=(0, 24))
        tk.Label(f, text=label_text, font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 8))
        
        bg_col = "#e2e8f0" if disabled else "#f4f4f5"
        fg_col = "#94a3b8" if disabled else TEXT_PRIMARY
        
        inner = tk.Frame(f, bg=bg_col, height=48)
        inner.pack(fill="x"); inner.pack_propagate(False)
        e = tk.Entry(inner, font=("Segoe UI", 10), bg=bg_col, fg=fg_col, relief="flat", bd=0, insertbackground=TEXT_PRIMARY)
        e.pack(fill="both", expand=True, padx=16, pady=12)
        e.insert(0, value)
        if disabled:
            e.config(state="disabled")

    _make_field(col1, "Student Name", "Juan Dela Cruz", disabled=True)
    _make_field(col1, "Student ID", "25-2751", disabled=True)
    _make_field(col1, "Department", "BS Information Technology", disabled=True)


    # --- RIGHT COL: Preferences ---
    tk.Label(col2, text="System Preferences", font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 16))

    def _toggle(p, text, on=False):
        f = tk.Frame(p, bg=WHITE)
        f.pack(fill="x", pady=(0, 16))
        tk.Label(f, text="☑" if on else "☐", font=("Segoe UI Emoji", 14), fg=NAV_BG if on else "#94a3b8", bg=WHITE).pack(side="left")
        tk.Label(f, text=text, font=("Segoe UI", 10), fg=TEXT_PRIMARY, bg=WHITE).pack(side="left", padx=(8, 0))

    _toggle(col2, "Email Notifications: Announcements", True)
    _toggle(col2, "Email Notifications: Grades", True)
    _toggle(col2, "SMS Notifications: Events", False)

    def show_notification(e=None):
        notif = tk.Frame(container, bg="#10b981", highlightthickness=0)
        notif.place(relx=1.0, rely=0.0, x=-32, y=32, anchor="ne")
        tk.Label(notif, text="✓ Settings saved successfully", font=("Segoe UI", 10, "bold"), fg=WHITE, bg="#10b981", padx=16, pady=12).pack()
        container.after(3000, notif.destroy)

    # Footer Save Button
    footer = tk.Frame(form, bg=WHITE)
    footer.pack(side="bottom", fill="x", pady=(48, 0))
    btn_save = tk.Button(footer, text="Save Settings", font=("Segoe UI", 10, "bold"), fg=WHITE, bg=NAV_BG, relief="flat", padx=32, pady=8, cursor="hand2", command=show_notification)
    btn_save.pack(anchor="w")
