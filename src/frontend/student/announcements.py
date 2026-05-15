import tkinter as tk

NAV_BG        = "#001f5b"
WHITE         = "#ffffff"
TEXT_PRIMARY  = "#111827"
TEXT_MUTED    = "#6b7280"
CARD_BORDER   = "#e2e8f0"

def build_announcements_tab(parent, switch_cb):
    container = tk.Frame(parent, bg=WHITE)
    container.pack(fill="both", expand=True)

    # Header
    top_row = tk.Frame(container, bg=WHITE)
    top_row.pack(fill="x", pady=(48, 32), padx=48)
    tk.Label(top_row, text="University Announcements", font=("Georgia", 24), fg=TEXT_PRIMARY, bg=WHITE).pack(side="left")

    def show_notification(e=None):
        notif = tk.Frame(container, bg="#10b981", highlightthickness=0)
        notif.place(relx=1.0, rely=0.0, x=-32, y=32, anchor="ne")
        tk.Label(notif, text="✓ All announcements marked as read", font=("Segoe UI", 10, "bold"), fg=WHITE, bg="#10b981", padx=16, pady=12).pack()
        container.after(3000, notif.destroy)

    btn_read = tk.Button(top_row, text="Mark all as read", font=("Segoe UI", 9, "bold"), fg=NAV_BG, bg=WHITE, relief="solid", bd=1, padx=16, pady=4, cursor="hand2", command=show_notification)
    btn_read.pack(side="right")

    # Feed Container
    feed = tk.Frame(container, bg=WHITE)
    feed.pack(fill="both", expand=True, padx=24)

    announcements_data = [] #no mock datas

    for i, data in enumerate(announcements_data):
        card = tk.Frame(feed, bg=WHITE)
        card.pack(fill="x", padx=24, pady=20)
        
        # New indicator dot
        left_col = tk.Frame(card, bg=WHITE, width=20)
        left_col.pack(side="left", fill="y", padx=(0, 16))
        left_col.pack_propagate(False)
        if data["is_new"]:
            dot = tk.Frame(left_col, bg=NAV_BG, width=8, height=8)
            dot.pack(pady=(6,0))

        content_col = tk.Frame(card, bg=WHITE)
        content_col.pack(side="left", fill="both", expand=True)

        # Header of card
        hdr = tk.Frame(content_col, bg=WHITE)
        hdr.pack(fill="x", pady=(0, 8))
        
        tk.Label(hdr, text=data["tag"], font=("Segoe UI", 7, "bold"), fg=data["tag_color"], bg=data["tag_bg"], padx=6, pady=2).pack(side="left")
        tk.Label(hdr, text=f"•  {data['date']}  •  {data['author']}", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=WHITE).pack(side="left", padx=(8,0))

        # Title
        tk.Label(content_col, text=data["title"], font=("Segoe UI", 12, "bold"), fg=TEXT_PRIMARY, bg=WHITE).pack(anchor="w", pady=(0, 4))
        
        # Content
        tk.Label(content_col, text=data["content"], font=("Segoe UI", 10), fg="#4b5563", bg=WHITE, justify="left", wraplength=800).pack(anchor="w")

        if i < len(announcements_data) - 1:
            tk.Frame(feed, bg=CARD_BORDER, height=1).pack(fill="x", padx=24)
