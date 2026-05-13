import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
CONTENT_BG    = "#edf0f5"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#e2e8f0"

def build_subjects_tab(parent, switch_cb):
    # Main container
    container = tk.Frame(parent, bg=CONTENT_BG)
    container.pack(fill="both", expand=True, padx=32, pady=32)

    # --- TOP ROW ---
    top_row = tk.Frame(container, bg=CONTENT_BG)
    top_row.pack(fill="x", pady=(0, 24))
    
    # Export Schedule Button
    btn_wrap = tk.Frame(top_row, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER, cursor="hand2")
    btn_wrap.pack(side="right")
    
    inner_btn = tk.Frame(btn_wrap, bg=WHITE, padx=12, pady=6)
    inner_btn.pack()
    tk.Label(inner_btn, text="📅", font=("Segoe UI Emoji", 10), fg="#1e3a8a", bg=WHITE).pack(side="left", padx=(0, 6))
    tk.Label(inner_btn, text="Export Schedule", font=("Segoe UI", 9, "bold"), fg="#1e3a8a", bg=WHITE).pack(side="left")

    # --- GRID OF CARDS ---
    grid_container = tk.Frame(container, bg=CONTENT_BG)
    grid_container.pack(fill="both", expand=True)
    
    subjects_data = [
        {
            "code": "CS 301",
            "status": "Enrolled",
            "status_color": "#22c55e",
            "title": "Data Structures and\nAlgorithms",
            "prof": "Prof. Alan Turing",
            "time_day": "Mon / Wed",
            "time_span": "9:00 AM - 10:30 AM",
            "loc_bldg": "Science Center",
            "loc_room": "Room 402",
            "credits": "4 Credits"
        },
        {
            "code": "MTH 210",
            "status": "Enrolled",
            "status_color": "#22c55e",
            "title": "Linear Algebra & Matrix\nTheory",
            "prof": "Dr. Katherine Johnson",
            "time_day": "Tue / Thu",
            "time_span": "11:00 AM - 12:15 PM",
            "loc_bldg": "Mathematics Bldg",
            "loc_room": "Hall B",
            "credits": "3 Credits"
        },
        {
            "code": "ENG 105",
            "status": "Waitlisted",
            "status_color": "#eab308",
            "title": "Modern Literature\nSemantics",
            "prof": "Prof. Virginia Woolf",
            "time_day": "Friday",
            "time_span": "2:00 PM - 5:00 PM",
            "loc_bldg": "Humanities Pavilion",
            "loc_room": "Seminar Room 12",
            "credits": "3 Credits"
        }
    ]

    for i in range(3):
        grid_container.columnconfigure(i, weight=1, uniform="col")
        
    for i, data in enumerate(subjects_data):
        card_outer = tk.Frame(grid_container, bg=NAV_BG) # Top blue border effect
        card_outer.grid(row=0, column=i, sticky="nsew", padx=(0 if i==0 else 12, 12 if i!=2 else 0))
        
        # Thick blue border at top
        tk.Frame(card_outer, bg=NAV_BG, height=6).pack(fill="x")
        
        card_body = tk.Frame(card_outer, bg=CARD_BG, highlightthickness=1, highlightbackground=CARD_BORDER)
        card_body.pack(fill="both", expand=True)
        
        # --- Card Content ---
        content = tk.Frame(card_body, bg=CARD_BG)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tags row
        tags_row = tk.Frame(content, bg=CARD_BG)
        tags_row.pack(fill="x", pady=(0, 16))
        
        # Code pill
        tk.Label(tags_row, text=data["code"], font=("Segoe UI", 8, "bold"), fg="#1e3a8a", bg="#f1f5f9", padx=8, pady=4).pack(side="left")
        
        # Status pill
        status_f = tk.Frame(tags_row, bg="#f0fdf4" if data["status"] == "Enrolled" else "#fefce8")
        status_f.pack(side="right")
        tk.Label(status_f, text="●", font=("Segoe UI", 8), fg=data["status_color"], bg=status_f["bg"], padx=4).pack(side="left")
        tk.Label(status_f, text=data["status"], font=("Segoe UI", 8, "bold"), fg="#166534" if data["status"] == "Enrolled" else "#854d0e", bg=status_f["bg"], padx=4, pady=4).pack(side="left")
        
        # Title
        title_f = tk.Frame(content, bg=CARD_BG, height=48)
        title_f.pack(fill="x", pady=(0, 8))
        title_f.pack_propagate(False)
        tk.Label(title_f, text=data["title"], font=("Segoe UI", 12, "bold"), fg="#1e3a8a", bg=CARD_BG, justify="left").pack(anchor="w")
        
        # Prof
        prof_f = tk.Frame(content, bg=CARD_BG)
        prof_f.pack(fill="x", pady=(0, 16))
        tk.Label(prof_f, text="👤", font=("Segoe UI Emoji", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left", padx=(0, 4))
        tk.Label(prof_f, text=data["prof"], font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left")
        
        # Divider
        tk.Frame(content, bg=CARD_BORDER, height=1).pack(fill="x", pady=(0, 16))
        
        # Schedule Info
        sched_f = tk.Frame(content, bg=CARD_BG)
        sched_f.pack(fill="x", pady=(0, 16))
        
        # Time
        time_f = tk.Frame(sched_f, bg=CARD_BG)
        time_f.pack(fill="x", pady=(0, 12))
        tk.Label(time_f, text="🕒", font=("Segoe UI Emoji", 9), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left", anchor="n", padx=(0, 6))
        time_txt_f = tk.Frame(time_f, bg=CARD_BG)
        time_txt_f.pack(side="left")
        tk.Label(time_txt_f, text=data["time_day"], font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG).pack(anchor="w")
        tk.Label(time_txt_f, text=data["time_span"], font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        
        # Location
        loc_f = tk.Frame(sched_f, bg=CARD_BG)
        loc_f.pack(fill="x")
        tk.Label(loc_f, text="🏢", font=("Segoe UI Emoji", 9), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left", anchor="n", padx=(0, 6))
        loc_txt_f = tk.Frame(loc_f, bg=CARD_BG)
        loc_txt_f.pack(side="left")
        tk.Label(loc_txt_f, text=data["loc_bldg"], font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG).pack(anchor="w")
        tk.Label(loc_txt_f, text=data["loc_room"], font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        
        # Divider
        tk.Frame(content, bg=CARD_BORDER, height=1).pack(fill="x", pady=(16, 16))
        
        # Footer
        footer_f = tk.Frame(content, bg=CARD_BG)
        footer_f.pack(fill="x")
        tk.Label(footer_f, text=data["credits"], font=("Segoe UI", 8), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left")
        tk.Label(footer_f, text="View Syllabus ➔", font=("Segoe UI", 8, "bold"), fg="#1e3a8a", bg=CARD_BG, cursor="hand2").pack(side="right")
