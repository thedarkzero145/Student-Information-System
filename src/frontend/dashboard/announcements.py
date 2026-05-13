import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
CONTENT_BG    = "#edf0f5"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BG       = "#ffffff"
CARD_BORDER   = "#e2e8f0"
ACCENT_GREEN  = "#22c55e"

def build_announcements_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=CONTENT_BG)
    container.pack(fill="both", expand=True, padx=32, pady=32)

    # Header
    top_row = tk.Frame(container, bg=CONTENT_BG)
    top_row.pack(fill="x", pady=(0, 24))
    tk.Label(top_row, text="University Announcements", font=("Segoe UI", 16, "bold"), fg=TEXT_PRIMARY, bg=CONTENT_BG).pack(side="left")

    btn_wrap = tk.Frame(top_row, bg=WHITE, highlightthickness=1, highlightbackground=CARD_BORDER, cursor="hand2")
    btn_wrap.pack(side="right")
    inner_btn = tk.Frame(btn_wrap, bg=WHITE, padx=12, pady=6)
    inner_btn.pack()
    tk.Label(inner_btn, text="Mark all as read", font=("Segoe UI", 9, "bold"), fg="#1e3a8a", bg=WHITE).pack()

    # Feed Container
    feed_outer = tk.Frame(container, bg=CARD_BORDER)
    feed_outer.pack(fill="both", expand=True)
    feed = tk.Frame(feed_outer, bg=CARD_BG)
    feed.pack(padx=1, pady=1, fill="both", expand=True)

    announcements_data = [
        {
            "tag": "ACADEMICS",
            "tag_color": "#1e3a8a",
            "tag_bg": "#dbeafe",
            "title": "Final Examination Schedule Released for Spring 2026",
            "date": "Today, 9:00 AM",
            "author": "Registrar's Office",
            "content": "Please be advised that the final examination schedule for the current semester is now available. Students are required to check their respective portals to verify their schedule. Conflict resolution forms must be submitted by Friday.",
            "is_new": True
        },
        {
            "tag": "CAMPUS",
            "tag_color": "#166534",
            "tag_bg": "#dcfce7",
            "title": "Main Library Renovation Notice",
            "date": "Yesterday, 2:30 PM",
            "author": "Facilities Management",
            "content": "The West Wing of the Main Library will be closed for renovations starting next Monday. Temporary study areas have been set up in the Student Union building. We apologize for the inconvenience.",
            "is_new": False
        },
        {
            "tag": "URGENT",
            "tag_color": "#991b1b",
            "tag_bg": "#fee2e2",
            "title": "System Maintenance Downtime",
            "date": "May 10, 2026",
            "author": "IT Department",
            "content": "The Student Information System will undergo scheduled maintenance this coming weekend from 12:00 AM to 4:00 AM. Access to grades and enrollment modules will be temporarily unavailable.",
            "is_new": False
        }
    ]

    for i, data in enumerate(announcements_data):
        card = tk.Frame(feed, bg=CARD_BG)
        card.pack(fill="x", padx=24, pady=20)
        
        # New indicator dot
        left_col = tk.Frame(card, bg=CARD_BG, width=20)
        left_col.pack(side="left", fill="y", padx=(0, 16))
        left_col.pack_propagate(False)
        if data["is_new"]:
            dot = tk.Frame(left_col, bg="#3b82f6", width=8, height=8)
            dot.pack(pady=(6,0))

        content_col = tk.Frame(card, bg=CARD_BG)
        content_col.pack(side="left", fill="both", expand=True)

        # Header of card
        hdr = tk.Frame(content_col, bg=CARD_BG)
        hdr.pack(fill="x", pady=(0, 8))
        
        tk.Label(hdr, text=data["tag"], font=("Segoe UI", 7, "bold"), fg=data["tag_color"], bg=data["tag_bg"], padx=6, pady=2).pack(side="left")
        tk.Label(hdr, text=f"•  {data['date']}  •  {data['author']}", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD_BG).pack(side="left", padx=(8,0))

        # Title
        tk.Label(content_col, text=data["title"], font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=CARD_BG).pack(anchor="w", pady=(0, 4))
        
        # Content
        tk.Label(content_col, text=data["content"], font=("Segoe UI", 10), fg="#4b5563", bg=CARD_BG, justify="left", wraplength=800).pack(anchor="w")

        if i < len(announcements_data) - 1:
            tk.Frame(feed, bg=CARD_BORDER, height=1).pack(fill="x", padx=24)
