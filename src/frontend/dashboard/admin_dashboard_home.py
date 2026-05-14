import tkinter as tk
import os
from dotenv import load_dotenv

load_dotenv()

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

    _stat_card(stats_f, "Total Students", os.getenv("ADMIN_HOME_TOTAL_STUDENTS", "1,245"), "👥")
    _stat_card(stats_f, "Active Subjects", os.getenv("ADMIN_HOME_ACTIVE_SUBJECTS", "142"), "📚")
    _stat_card(stats_f, "Upcoming Events", os.getenv("ADMIN_HOME_UPCOMING_EVENTS", "12"), "🎉")
    c4 = _stat_card(stats_f, "Announcements", os.getenv("ADMIN_HOME_ANNOUNCEMENTS", "3"), "🔊")
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
        w, h = e.width, e.height
        env_data = os.getenv("ADMIN_HOME_BAR_DATA", "2022|800,2023|950,2024|1100,2025|1050,2026|1245")
        data = []
        for pair in env_data.split(","):
            year, val = pair.split("|")
            data.append((year, int(val)))
        max_val = 1500
        bar_w = 40
        spacing = (w - (bar_w * len(data))) / (len(data) + 1)
        
        for i, (year, val) in enumerate(data):
            x = spacing + i * (bar_w + spacing)
            bar_h = (val / max_val) * (h - 40)
            y = h - 30 - bar_h
            
            c_bar.create_rectangle(x, y, x + bar_w, h - 30, fill=NAV_BG, outline="")
            c_bar.create_text(x + bar_w/2, h - 15, text=year, font=("Segoe UI", 9), fill=TEXT_MUTED)
            c_bar.create_text(x + bar_w/2, y - 10, text=str(val), font=("Segoe UI", 9, "bold"), fill=TEXT_PRIMARY)

    c_bar.bind("<Configure>", _draw_bar_chart)

    # Pie Chart (Department Distribution)
    pie_outer = tk.Frame(graphs_f, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER)
    pie_outer.pack(side="left", fill="both", expand=True)

    tk.Label(pie_outer, text="Students by Department", font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", padx=24, pady=(24, 8))

    c_pie = tk.Canvas(pie_outer, bg=WHITE, highlightthickness=0, height=250)
    c_pie.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def _draw_pie_chart(e):
        c_pie.delete("all")
        w, h = e.width, e.height
        cx, cy = w/2, h/2 - 10
        r = min(w, h)/2 - 30
        
        env_data = os.getenv("ADMIN_HOME_PIE_DATA", "BSIT|45|#2563eb,BSCS|25|#16a34a,BSBA|20|#d97706,Other|10|#94a3b8")
        data = []
        for triplet in env_data.split(","):
            label, pct, color = triplet.split("|")
            data.append((label, int(pct), color))
        
        start_ang = 0
        for label, pct, col in data:
            extent = (pct / 100) * 360
            c_pie.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_ang, extent=extent, fill=col, outline=WHITE, width=2)
            start_ang += extent
            
        # Legend
        leg = cx - 100
        for i, (label, pct, col) in enumerate(data):
            c_pie.create_rectangle(leg + i*50, h-15, leg + i*50 + 10, h-5, fill=col, outline="")
            c_pie.create_text(leg + i*50 + 15, h-10, text=label, font=("Segoe UI", 8), fill=TEXT_MUTED, anchor="w")

    c_pie.bind("<Configure>", _draw_pie_chart)
