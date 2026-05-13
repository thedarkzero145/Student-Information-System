import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BORDER   = "#e2e8f0"

def build_events_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    # Header
    top_row = tk.Frame(container, bg=WHITE)
    top_row.pack(fill="x", pady=(48, 32), padx=48)
    tk.Label(top_row, text="Campus Events", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")

    def show_notification(e=None):
        notif = tk.Frame(container, bg="#10b981", highlightthickness=0)
        notif.place(relx=1.0, rely=0.0, x=-32, y=32, anchor="ne")
        tk.Label(notif, text="✓ Suggestion portal opened", font=("Segoe UI", 10, "bold"), fg=WHITE, bg="#10b981", padx=16, pady=12).pack()
        container.after(3000, notif.destroy)

    btn_suggest = tk.Button(top_row, text="➕ Suggest Event", font=("Segoe UI", 9, "bold"), fg=WHITE, bg=NAV_BG, relief="flat", padx=16, pady=6, cursor="hand2", command=show_notification)
    btn_suggest.pack(side="right")

    # Grid Container
    grid_container = tk.Frame(container, bg=WHITE)
    grid_container.pack(fill="both", expand=True, padx=48)

    events_data = [
        {
            "month": "MAY",
            "day": "24",
            "title": "Annual Tech Symposium 2026",
            "time": "8:00 AM - 5:00 PM",
            "location": "University Grand Hall",
            "type": "Academic",
            "color": "#2563eb"
        },
        {
            "month": "JUN",
            "day": "02",
            "title": "Freshman Orientation Seminar",
            "time": "9:00 AM - 12:00 PM",
            "location": "Student Union Auditorium",
            "type": "Campus Life",
            "color": "#16a34a"
        },
        {
            "month": "JUN",
            "day": "15",
            "title": "Inter-Department Sports Fest",
            "time": "All Day Event",
            "location": "Main Athletics Field",
            "type": "Sports",
            "color": "#d97706"
        }
    ]

    for i in range(3):
        grid_container.columnconfigure(i, weight=1, uniform="col")

    def show_rsvp(e=None):
        notif = tk.Frame(container, bg="#10b981", highlightthickness=0)
        notif.place(relx=1.0, rely=0.0, x=-32, y=32, anchor="ne")
        tk.Label(notif, text="✓ Successfully RSVP'd for event", font=("Segoe UI", 10, "bold"), fg=WHITE, bg="#10b981", padx=16, pady=12).pack()
        container.after(3000, notif.destroy)

    for i, data in enumerate(events_data):
        card = tk.Frame(grid_container, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER)
        card.grid(row=0, column=i, sticky="nsew", padx=(0 if i==0 else 12, 12 if i!=2 else 0))
        
        # Date block
        date_f = tk.Frame(card, bg=data["color"])
        date_f.pack(fill="x")
        date_inner = tk.Frame(date_f, bg=data["color"], pady=16)
        date_inner.pack()
        tk.Label(date_inner, text=data["month"], font=("Segoe UI", 10, "bold"), fg=WHITE, bg=data["color"]).pack()
        tk.Label(date_inner, text=data["day"], font=("Segoe UI", 28, "bold"), fg=WHITE, bg=data["color"]).pack()

        # Content block
        content = tk.Frame(card, bg=WHITE)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(content, text=data["type"], font=("Segoe UI", 8, "bold"), fg=data["color"], bg=WHITE).pack(anchor="w", pady=(0, 8))
        
        title_f = tk.Frame(content, bg=WHITE, height=48)
        title_f.pack(fill="x", pady=(0, 16))
        title_f.pack_propagate(False)
        tk.Label(title_f, text=data["title"], font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE, wraplength=200, justify="left").pack(anchor="w")

        tk.Label(content, text=f"🕒 {data['time']}", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=WHITE).pack(anchor="w", pady=(0, 4))
        tk.Label(content, text=f"📍 {data['location']}", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=WHITE).pack(anchor="w")

        # RSVP button
        btn_rsvp = tk.Button(content, text="RSVP Now", font=("Segoe UI", 9, "bold"), fg=NAV_BG, bg=WHITE, relief="solid", bd=1, pady=6, cursor="hand2", command=show_rsvp)
        btn_rsvp.pack(fill="x", side="bottom", pady=(24,0))
