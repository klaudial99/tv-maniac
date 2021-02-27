import os
import tkinter as tk
import functions
from scroll import ScrollableFrame
from start_view_section import StartViewSection


class StartView:

    """
    creates start view with scroll, top movies, tv series from last year, and history
    """

    def __init__(self, master):
        self.scroll_frame = ScrollableFrame(master)
        self.scroll_frame.pack(fill='both', expand=True)

        self.master = master

        self.movies_frame = tk.LabelFrame(self.scroll_frame.scrollable_frame, bg=functions.BG_COLOR)
        self.tv_frame = tk.LabelFrame(self.scroll_frame.scrollable_frame, bg=functions.BG_COLOR)
        self.last_frame = tk.LabelFrame(self.scroll_frame.scrollable_frame, bg=functions.BG_COLOR)
        functions.ACTUAL_HISTORY_OBJECT_MASTER = self.last_frame

        self.movies_frame.grid(column=0, row=0, padx=30, pady=30)
        self.tv_frame.grid(column=0, row=1)
        self.last_frame.grid(column=0, row=2, pady=30, sticky='w', padx=30)

        StartViewSection(self.movies_frame, "movie")
        StartViewSection(self.tv_frame, "tv")
        if os.path.exists("history.txt"):
            history = StartViewSection(self.last_frame, "last")
            functions.ACTUAL_HISTORY_OBJECT = history

