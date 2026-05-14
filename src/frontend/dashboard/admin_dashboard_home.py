import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BORDER   = "#e2e8f0"

def build_dashboard_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    # Header
    top_bar = tk.Frame(container, bg=WHITE)
    top_bar.pack(fill="x", pady=(48, 24), padx=48)
    tk.Label(top_bar, text="Overview Dashboard", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")

    # Stat Cards Row
    stats_f = tk.Frame(container, bg=WHITE)
    stats_f.pack(fill="x", padx=48, pady=(0, 24))

    def _stat_card(p, title, val, icon):
        outer = tk.Frame(p, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER)
        outer.pack(side="left", fill="both", expand=True, padx=(0, 16))
        pad = tk.Frame(outer, bg=WHITE)
        pad.pack(fill="both", expand=True, padx=24, pady=24)
        
        tk.Label(pad, text=icon, font=("Segoe UI Emoji", 20), fg=TEXT_MUTED, bg=WHITE).pack(side="left", padx=(0, 16))
        
        txt_f = tk.Frame(pad, bg=WHITE)
        txt_f.pack(side="left", fill="both", expand=True)
        tk.Label(txt_f, text=title, font=("Segoe UI", 10, "bold"), fg=TEXT_MUTED, bg=WHITE).pack(anchor="w")
        tk.Label(txt_f, text=val, font=("Segoe UI", 24, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w")
        return outer

    _stat_card(stats_f, "Total Students", "", "\U0001f465")
    _stat_card(stats_f, "Active Subjects", "", "\U0001f4da")
    _stat_card(stats_f, "Upcoming Events", "", "\U0001f389")
    c4 = _stat_card(stats_f, "Announcements", "", "\U0001f50a")
    c4.pack_configure(padx=0)

    # Graphs Row
    graphs_f = tk.Frame(container, bg=WHITE)
    graphs_f.pack(fill="both", expand=True, padx=48, pady=(0, 48))

    # Bar Chart (Enrollment Trends)
    bar_outer = tk.Frame(graphs_f, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER)
    bar_outer.pack(side="left", fill="both", expand=True, padx=(0, 16))
    
    tk.Label(bar_outer, text="Enrollment Trends (Last 5 Years)", font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", padx=24, pady=(24, 8))
    
    c_bar = tk.Canvas(bar_outer, bg=WHITE, highlightthickness=0, height=250)
    c_bar.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _draw_bar_chart(e):
        c_bar.delete("all")
        # No data — will be populated by database

    c_bar.bind("<Configure>", _draw_bar_chart)

    # Pie Chart (Department Distribution)
    pie_outer = tk.Frame(graphs_f, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER)
    pie_outer.pack(side="left", fill="both", expand=True)

    tk.Label(pie_outer, text="Students by Department", font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", padx=24, pady=(24, 8))

    c_pie = tk.Canvas(pie_outer, bg=WHITE, highlightthickness=0, height=250)
    c_pie.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def _draw_pie_chart(e):
        c_pie.delete("all")
        # No data — will be populated by database

    c_pie.bind("<Configure>", _draw_pie_chart)
