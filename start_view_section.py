import os
import tkinter as tk
from datetime import date
import functions
from single_prod_view import SingleProdView


class StartViewSection:

    """
    creates start view section with single productions and horizontal scroll in buttons
    """

    def __init__(self, master, what):

        self.master = master
        self.what = what

        self.index = 0
        self.how_many = 10

        self.last_year = date.today().year - 1

        self.table = []
        right_path = functions.ICONS_PATH + "next.png"
        left_path = functions.ICONS_PATH + "back.png"
        self.right_arrow = tk.PhotoImage(file=right_path)
        self.left_arrow = tk.PhotoImage(file=left_path)

        self.create_top(what)
        self.show_top(what)

    """
    creates views of single productions
    
    :param what: type of production - movie or tv
    """

    def create_top(self, what):

        if what == "movie":
            top_10 = functions.get_top_year_config_file("movie", self.last_year, self.how_many, True)
        elif what == "tv":
            top_10 = functions.get_top_year_config_file("tv", self.last_year, self.how_many, True)
        elif what == "last":
            if os.path.exists("history.txt"):
                self.info, self.how_many = functions.read_history()
            top_10 = self.info
            self.table.clear()

        for i in range(len(top_10)):
            SingleProdView(self.master, self.table, i, top_10, True)

    """
    shows views of single productions with scroll buttons if required (number>5)

    :param what: type of production - movie or tv
    """

    def show_top(self, what):

        if what == "movie":
            text = str(self.last_year) + "'s top 10 movies"
        elif what == "tv":
            text = str(self.last_year) + "'s top TV series"
        elif what == "last":
            text = "last viewed productions"

        text = tk.Label(self.master, text=text, padx=10, font=(functions.FONT, 26), bg=functions.BG_COLOR, fg=functions.FONT_COLOR)
        text.grid(row=0, columnspan=3, sticky='w')

        # LEFT BUTTON
        if len(self.table) > 5:
            left_button = tk.Button(self.master, image=self.left_arrow, command=lambda: self.left_click(what))
            left_button.grid(column=0, row=1)
            self.master.grid_columnconfigure(0, minsize=50)
            self.master.grid_columnconfigure(6, minsize=50)

        for item in self.table:
            item.grid_forget()

        counter = 0
        if len(self.table) > 5:
            my_range = self.index + 5
        else:
            my_range = len(self.table)
        for i in range(self.index, my_range):
            counter += 1
            self.table[i].grid(column=counter, row=1, padx=10, sticky='n')

        # RIGHT BUTTON
        if len(self.table) > 5:
            right_button = tk.Button(self.master, image=self.right_arrow, command=lambda: self.right_click(what))
            right_button.grid(column=6, row=1)

    """
    scroll left by one item
    """

    def left_click(self, what):
        if self.index >= 1:
            self.index -= 1

        self.show_top(what)

    """
    scroll right by one item
    """

    def right_click(self, what):
        if self.index <= self.how_many - 6:
            self.index += 1

        self.show_top(what)