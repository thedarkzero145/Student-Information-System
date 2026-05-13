import tkinter as tk
from tkinter import ttk as tkttk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BORDER   = "#e2e8f0"

def build_announcements_list_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    # Header
    top_bar = tk.Frame(container, bg=WHITE)
    top_bar.pack(fill="x", pady=(48, 16), padx=48)
    tk.Label(top_bar, text="Announcement Management", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")

    btn_add = tk.Button(top_bar, text="➕ Post Announcement", font=("Segoe UI", 9, "bold"), fg=WHITE, bg=NAV_BG, relief="flat", padx=16, pady=6, cursor="hand2", command=lambda: switch_cb("Add Announcement"))
    btn_add.pack(side="right")

    tk.Frame(container, bg=CARD_BORDER, height=1).pack(fill="x", padx=48, pady=16)

    # Table
    table_f = tk.Frame(container, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER)
    table_f.pack(fill="both", expand=True, padx=48, pady=(0, 48))

    cols = ("title", "date", "author", "category")
    tree = tkttk.Treeview(table_f, columns=cols, show="headings", height=15)
    
    tree.heading("title", text="Announcement Title")
    tree.heading("date", text="Date Posted")
    tree.heading("author", text="Author")
    tree.heading("category", text="Category")
    
    tree.column("title", width=400)
    tree.column("date", width=150)
    tree.column("author", width=200)
    tree.column("category", width=150)
    
    tree.pack(fill="both", expand=True)
    
    mock_data = [
        ("Final Examination Schedule Released for Spring 2026", "Today, 9:00 AM", "Registrar's Office", "ACADEMICS"),
        ("Main Library Renovation Notice", "Yesterday, 2:30 PM", "Facilities Management", "CAMPUS"),
        ("System Maintenance Downtime", "May 10, 2026", "IT Department", "URGENT"),
    ]
    for d in mock_data:
        tree.insert("", "end", values=d)


def build_add_announcement_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Post New Announcement", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(48, 16), padx=120)
    tk.Frame(container, bg=CARD_BORDER, height=1).pack(fill="x", padx=120, pady=16)

    form = tk.Frame(container, bg=WHITE)
    form.pack(fill="both", expand=True, padx=120)

    def _make_field(parent_frame, label_text, placeholder):
        f = tk.Frame(parent_frame, bg=WHITE)
        f.pack(fill="x", pady=(0, 24))
        tk.Label(f, text=label_text, font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 8))
        inner = tk.Frame(f, bg="#f4f4f5", height=48)
        inner.pack(fill="x"); inner.pack_propagate(False)
        e = tk.Entry(inner, font=("Segoe UI", 10), bg="#f4f4f5", fg=TEXT_PRIMARY, relief="flat", bd=0, insertbackground=TEXT_PRIMARY)
        e.pack(fill="both", expand=True, padx=16, pady=12)
        e.insert(0, placeholder)

    _make_field(form, "Title", "e.g. System Maintenance Notice")
    _make_field(form, "Category", "e.g. URGENT, ACADEMICS, CAMPUS")
    
    # Text Area
    f_area = tk.Frame(form, bg=WHITE)
    f_area.pack(fill="both", expand=True, pady=(0, 24))
    tk.Label(f_area, text="Announcement Content", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 8))
    
    text_inner = tk.Frame(f_area, bg="#f4f4f5")
    text_inner.pack(fill="both", expand=True)
    t = tk.Text(text_inner, font=("Segoe UI", 10), bg="#f4f4f5", fg=TEXT_PRIMARY, relief="flat", bd=0, insertbackground=TEXT_PRIMARY, height=8)
    t.pack(fill="both", expand=True, padx=16, pady=12)

    def show_notification(e=None):
        notif = tk.Frame(container, bg="#10b981", highlightthickness=0)
        notif.place(relx=1.0, rely=0.0, x=-32, y=32, anchor="ne")
        tk.Label(notif, text="✓ Announcement posted", font=("Segoe UI", 10, "bold"), fg=WHITE, bg="#10b981", padx=16, pady=12).pack()
        container.after(3000, notif.destroy)
        switch_cb("Announcement List")

    footer = tk.Frame(form, bg=WHITE)
    footer.pack(fill="x", pady=(16, 0))
    btn_add = tk.Button(footer, text="Post Announcement", font=("Segoe UI", 10, "bold"), fg=WHITE, bg=NAV_BG, relief="flat", padx=32, pady=8, cursor="hand2", command=show_notification)
    btn_add.pack(side="left")
    btn_cancel = tk.Button(footer, text="Cancel", font=("Segoe UI", 10, "bold"), fg=NAV_BG, bg=WHITE, relief="solid", bd=1, padx=32, pady=8, cursor="hand2", command=lambda: switch_cb("Announcement List"))
    btn_cancel.pack(side="left", padx=(16, 0))
