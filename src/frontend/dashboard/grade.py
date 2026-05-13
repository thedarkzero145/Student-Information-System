import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
CONTENT_BG    = "#edf0f5"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#e2e8f0"

def build_grades_tab(parent, switch_cb):
    # Main container
    container = tk.Frame(parent, bg=CONTENT_BG)
    container.pack(fill="both", expand=True, padx=32, pady=32)

    # --- TOP ROW ---
    top_row = tk.Frame(container, bg=CONTENT_BG)
    top_row.pack(fill="x", pady=(0, 24))

    # Left Card: Cumulative Grade
    left_card_outer = tk.Frame(top_row, bg=CARD_BORDER)
    left_card_outer.pack(side="left", fill="both", expand=True, padx=(0, 16))
    
    left_card = tk.Frame(left_card_outer, bg="#f8fafc") # Slightly off-white light bg
    left_card.pack(padx=1, pady=1, fill="both", expand=True)
    
    left_inner = tk.Frame(left_card, bg="#f8fafc")
    left_inner.pack(padx=24, pady=24, fill="both", expand=True)

    tk.Label(left_inner, text="CUMULATIVE GRADE", font=("Segoe UI", 12), fg="#1e3a8a", bg="#f8fafc").pack(anchor="w")
    
    grade_f = tk.Frame(left_inner, bg="#f8fafc")
    grade_f.pack(anchor="w", pady=(12, 16))
    tk.Label(grade_f, text="1.25", font=("Segoe UI", 48), fg=TEXT_PRIMARY, bg="#f8fafc").pack(side="left")
    
    # To bottom align "/ 5.00", we wrap it
    slash_f = tk.Frame(grade_f, bg="#f8fafc")
    slash_f.pack(side="left", fill="y")
    tk.Label(slash_f, text=" / 5.00", font=("Segoe UI", 16), fg=TEXT_PRIMARY, bg="#f8fafc").pack(side="bottom", pady=(0, 10))

    # Badge
    badge_f = tk.Frame(left_inner, bg="#f8fafc")
    badge_f.pack(anchor="w", side="bottom")
    tk.Label(badge_f, text="📈 Top 5%", font=("Segoe UI", 8, "bold"), fg="#1e3a8a", bg="#dbeafe", padx=6, pady=2).pack(side="left")
    tk.Label(badge_f, text="Dean's List Standing", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg="#f8fafc").pack(side="left", padx=(8,0))

    # Right Card: Total Earned Credits
    right_card_outer = tk.Frame(top_row, bg=CARD_BORDER)
    right_card_outer.pack(side="left", fill="both", expand=True)

    right_card = tk.Frame(right_card_outer, bg="#1e3a8a")
    right_card.pack(padx=1, pady=1, fill="both", expand=True)

    right_inner = tk.Frame(right_card, bg="#1e3a8a")
    right_inner.pack(padx=24, pady=24, fill="both", expand=True)

    tk.Label(right_inner, text="TOTAL EARNED CREDITS", font=("Segoe UI", 10, "bold"), fg="#93c5fd", bg="#1e3a8a").pack(anchor="w")
    tk.Label(right_inner, text="96", font=("Segoe UI", 48, "bold"), fg=WHITE, bg="#1e3a8a").pack(anchor="w", pady=(4, 16))
    
    # Progress bar
    prog_bg = tk.Frame(right_inner, bg="#3b82f6", height=6)
    prog_bg.pack(fill="x", pady=(0, 8))
    prog_bg.pack_propagate(False)
    prog_fg = tk.Frame(prog_bg, bg="#bfdbfe", width=250)
    prog_fg.pack(side="left", fill="y")
    
    tk.Label(right_inner, text="Senior Status", font=("Segoe UI", 10), fg="#bfdbfe", bg="#1e3a8a").pack(anchor="e")

    # --- MIDDLE: Transcript Title ---
    tk.Label(container, text="Current Semester Transcript", font=("Segoe UI", 18), fg=TEXT_PRIMARY, bg=CONTENT_BG).pack(anchor="w", pady=(0, 12))

    # --- BOTTOM: Table ---
    table_outer = tk.Frame(container, bg=CARD_BORDER)
    table_outer.pack(fill="both", expand=True)

    table_bg = tk.Frame(table_outer, bg=CARD_BG)
    table_bg.pack(padx=1, pady=1, fill="both", expand=True)

    # Header
    header = tk.Frame(table_bg, bg="#002d72", height=40) # using a deep blue for the table header
    header.pack(fill="x")
    header.pack_propagate(False)
    
    for col in range(4):
        header.columnconfigure(col, weight=1 if col == 1 else 0, minsize=150 if col != 1 else 0)
    
    tk.Label(header, text="Course Code", font=("Segoe UI", 10), fg=WHITE, bg="#002d72").grid(row=0, column=0, sticky="w", padx=24, pady=10)
    tk.Label(header, text="Course Title", font=("Segoe UI", 10), fg=WHITE, bg="#002d72").grid(row=0, column=1, sticky="w", pady=10)
    tk.Label(header, text="Units", font=("Segoe UI", 10), fg=WHITE, bg="#002d72").grid(row=0, column=2, sticky="e", padx=(0, 48), pady=10)
    tk.Label(header, text="Grades", font=("Segoe UI", 10), fg=WHITE, bg="#002d72").grid(row=0, column=3, sticky="w", padx=24, pady=10)

    # Rows
    courses = [
        ("CS 401", "Advanced Data Structures", "4.0", "1.00", "#dcfce7", "#166534"),
        ("MAT 310", "Linear Algebra II", "3.0", "1.25", "#dcfce7", "#166534"),
        ("ENG 250", "Technical Writing for Sciences", "3.0", "1.00", "#dcfce7", "#166534"),
        ("PHY 205", "Quantum Mechanics Introduction", "4.0", "2.25", "#fef08a", "#854d0e"),
        ("HIST 102", "Modern European History", "2.0", "1.50", "#dcfce7", "#166534"),
    ]

    for i, (code, title, units, grade, bg_col, fg_col) in enumerate(courses):
        row_bg = CARD_BG if i % 2 == 0 else "#f8fafc"
        row_f = tk.Frame(table_bg, bg=row_bg, height=60)
        row_f.pack(fill="x")
        row_f.pack_propagate(False)
        
        for col in range(4):
            row_f.columnconfigure(col, weight=1 if col == 1 else 0, minsize=150 if col != 1 else 0)

        tk.Label(row_f, text=code, font=("Segoe UI", 10, "bold"), fg="#1e3a8a", bg=row_bg).grid(row=0, column=0, sticky="w", padx=24, pady=20)
        tk.Label(row_f, text=title, font=("Segoe UI", 10, "bold"), fg="#4b5563", bg=row_bg).grid(row=0, column=1, sticky="w", pady=20)
        tk.Label(row_f, text=units, font=("Segoe UI", 10), fg="#4b5563", bg=row_bg).grid(row=0, column=2, sticky="e", padx=(0, 48), pady=20)
        
        badge_wrap = tk.Frame(row_f, bg=row_bg)
        badge_wrap.grid(row=0, column=3, sticky="w", padx=24, pady=20)
        tk.Label(badge_wrap, text=grade, font=("Segoe UI", 10, "bold"), fg=fg_col, bg=bg_col, width=4).pack()

    # --- FOOTER ---
    footer = tk.Frame(container, bg=CONTENT_BG)
    footer.pack(fill="x", pady=(16, 0))
    
    btn_wrap = tk.Frame(footer, bg=WHITE, highlightthickness=1, highlightbackground="#002d72", cursor="hand2")
    btn_wrap.pack(side="right")
    
    inner_btn = tk.Frame(btn_wrap, bg=WHITE, padx=16, pady=8)
    inner_btn.pack()
    tk.Label(inner_btn, text="📥", font=("Segoe UI Emoji", 12), fg="#002d72", bg=WHITE).pack(side="left", padx=(0, 8))
    tk.Label(inner_btn, text="Download Unofficial Transcript", font=("Segoe UI", 10, "bold"), fg="#002d72", bg=WHITE).pack(side="left")

