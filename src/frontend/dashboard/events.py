import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
CONTENT_BG    = "#edf0f5"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#e2e8f0"

def build_events_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=CONTENT_BG)
    container.pack(fill="both", expand=True, padx=32, pady=32)

    # Header
    top_row = tk.Frame(container, bg=CONTENT_BG)
    top_row.pack(fill="x", pady=(0, 24))
    tk.Label(top_row, text="Campus Events", font=("Segoe UI", 16, "bold"), fg=TEXT_PRIMARY, bg=CONTENT_BG).pack(side="left")

    btn_wrap = tk.Frame(top_row, bg=NAV_BG, highlightthickness=0, cursor="hand2")
    btn_wrap.pack(side="right")
    inner_btn = tk.Frame(btn_wrap, bg=NAV_BG, padx=16, pady=6)
    inner_btn.pack()
    tk.Label(inner_btn, text="➕", font=("Segoe UI Emoji", 9), fg=WHITE, bg=NAV_BG).pack(side="left", padx=(0,6))
    tk.Label(inner_btn, text="Suggest Event", font=("Segoe UI", 9, "bold"), fg=WHITE, bg=NAV_BG).pack(side="left")

    # Grid Container
    grid_container = tk.Frame(container, bg=CONTENT_BG)
    grid_container.pack(fill="both", expand=True)

    events_data = [
        {
            "month": "MAY",
            "day": "24",
            "title": "Annual Tech Symposium 2026",
            "time": "8:00 AM - 5:00 PM",
            "location": "University Grand Hall",
            "type": "Academic",
            "color": "#3b82f6"
        },
        {
            "month": "JUN",
            "day": "02",
            "title": "Freshman Orientation Seminar",
            "time": "9:00 AM - 12:00 PM",
            "location": "Student Union Auditorium",
            "type": "Campus Life",
            "color": "#10b981"
        },
        {
            "month": "JUN",
            "day": "15",
            "title": "Inter-Department Sports Fest",
            "time": "All Day Event",
            "location": "Main Athletics Field",
            "type": "Sports",
            "color": "#f59e0b"
        }
    ]

    for i in range(3):
        grid_container.columnconfigure(i, weight=1, uniform="col")

    for i, data in enumerate(events_data):
        card_outer = tk.Frame(grid_container, bg=CARD_BORDER)
        card_outer.grid(row=0, column=i, sticky="nsew", padx=(0 if i==0 else 12, 12 if i!=2 else 0))
        
        card_body = tk.Frame(card_outer, bg=CARD_BG)
        card_body.pack(padx=1, pady=1, fill="both", expand=True)

        # Date block
        date_f = tk.Frame(card_body, bg=data["color"])
        date_f.pack(fill="x")
        date_inner = tk.Frame(date_f, bg=data["color"], pady=16)
        date_inner.pack()
        tk.Label(date_inner, text=data["month"], font=("Segoe UI", 10, "bold"), fg=WHITE, bg=data["color"]).pack()
        tk.Label(date_inner, text=data["day"], font=("Segoe UI", 28, "bold"), fg=WHITE, bg=data["color"]).pack()

        # Content block
        content = tk.Frame(card_body, bg=CARD_BG)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(content, text=data["type"], font=("Segoe UI", 8, "bold"), fg=data["color"], bg=CARD_BG).pack(anchor="w", pady=(0, 8))
        
        title_f = tk.Frame(content, bg=CARD_BG, height=48)
        title_f.pack(fill="x", pady=(0, 16))
        title_f.pack_propagate(False)
        tk.Label(title_f, text=data["title"], font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG, wraplength=200, justify="left").pack(anchor="w")

        tk.Label(content, text=f"🕒 {data['time']}", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
        tk.Label(content, text=f"📍 {data['location']}", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")

        # RSVP button
        btn_f = tk.Frame(content, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER, cursor="hand2")
        btn_f.pack(fill="x", side="bottom", pady=(24,0))
        tk.Label(btn_f, text="RSVP Now", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=WHITE, pady=8).pack()
