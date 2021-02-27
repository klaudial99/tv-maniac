import datetime
import math
import tkinter as tk
import functions
from tkinter import ttk
from scroll import ScrollableFrame
from single_prod_view import SingleProdView


class SearchView:

    """
    creates search view with scroll, filter menu and place for results
    """

    def __init__(self, master):

        self.scroll_frame = ScrollableFrame(master)
        self.scroll_frame.pack(side=tk.LEFT, fill='both', expand=True)

        self.oldest_movie = int(functions.get_oldest_release_year("movie"))
        self.oldest_tv = int(functions.get_oldest_release_year("tv"))

        self.search_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg="#FFFFFF")
        self.search_frame.pack(side=tk.LEFT, anchor='n', fill='y')

        self.go_up_button = tk.Button(self.search_frame, text="GO UP", font=(functions.FONT, 12, "bold"), command=self.go_up,
                                      width=15, bg=functions.THIRD_COLOR, fg="#FFFFFF", pady=5)
        self.go_up_button.pack(side=tk.BOTTOM)

        self.var_what = tk.IntVar()
        self.checkbuttons_input = []
        self.checkbuttons_states = []

        self.title_input = ""
        self.sorting_input = ""
        self.release_date_from_input = tk.StringVar()
        self.release_date_to_input = tk.StringVar()
        self.vote_average_from_input = tk.StringVar()
        self.vote_average_to_input = tk.StringVar()

        self.sorting_options = ["", "A-Z", "Z-A", "release date - asc", "release date - desc", "popularity - asc",
                                "popularity - desc", "vote average - asc", "vote average - desc"]

        self.comboboxes = []
        self.create_options()

        self.results_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg=functions.BG_COLOR)
        self.results_frame.pack(side=tk.RIGHT, fill='x', expand=True, anchor='n')
        self.results_frame.columnconfigure(1, minsize=1000)

        self.results_grid_frame = tk.Frame(self.results_frame, bg=functions.BG_COLOR)
        self.results_grid_frame.pack(fill='x', expand=True)
        self.results_table = []

        self.pages_frame = tk.Frame(self.results_frame, bg=functions.BG_COLOR)
        self.pages_frame.pack()
        self.pages_table = []
        self.pages_amount = 0
        self.actual_page = -1

        self.default_fg = ""
        self.default_bg = ""

    """
    scrolls to the top of the page
    """

    def go_up(self):
        self.scroll_frame.canvas.yview_moveto('0.0')

    """
    chooses correct year for type of production
    """

    def oldest(self, what):
        if what == 1:
            return self.oldest_movie
        elif what == 2:
            return self.oldest_tv

    """
    creates filter options
    """

    def create_options(self):

        button_frame = tk.Frame(self.search_frame, padx=5, pady=5)
        button_frame.pack(fill='x')

        what_frame = tk.LabelFrame(self.search_frame, text="CATEGORY", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        what_frame.pack(fill='x')

        """
        changes content of widgets when required
        """

        def change_widgets():
            change_checkbuttons()
            change_comboboxes()

        """
        changes content of checkbuttons (genres) when required
        """

        def change_checkbuttons():

            for button in self.checkbuttons_input:
                button.destroy()
            self.checkbuttons_states.clear()
            self.checkbuttons_input.clear()

            for i in range(len(functions.get_genres(self.var_what.get())[0])):
                self.checkbuttons_states.append(tk.BooleanVar())
                checkbutton = tk.Checkbutton(genres_frame, variable=self.checkbuttons_states[-1],
                                             text=functions.get_genres(self.var_what.get())[0][i],
                                             font=(functions.FONT, 10), fg=functions.FONT_COLOR)
                checkbutton.grid(row=i, sticky='w')
                self.checkbuttons_input.append(checkbutton)

        # RADIOBUTTONS
        radio1 = tk.Radiobutton(what_frame, text="Movies", variable=self.var_what, command=change_widgets, value=1,
                                font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        radio1.grid(row=0, column=0)
        radio2 = tk.Radiobutton(what_frame, text="TV series", variable=self.var_what, command=change_widgets, value=2,
                                font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        radio2.grid(row=0, column=1)
        self.var_what.set('1')

        # TITLE
        title_frame = tk.LabelFrame(self.search_frame, text='TITLE', font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        title_frame.pack(fill='x')
        enter_title = tk.Entry(title_frame)
        enter_title.pack()

        # SORT
        sort_frame = tk.LabelFrame(self.search_frame, text='SORTING', font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        sort_frame.pack(fill='x')
        sort_combo = ttk.Combobox(sort_frame, values=self.sorting_options, state="readonly")
        sort_combo.pack()

        # GENRES
        genres_frame = tk.LabelFrame(self.search_frame, text="GENRES", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        genres_frame.pack(fill='x')

        change_checkbuttons()

        # RELEASE DATE
        when_frame = tk.LabelFrame(self.search_frame, text="RELEASE DATE", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        when_frame.pack(fill='x')
        year_from = tk.Label(when_frame, text="From", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        year_from.grid(row=0, sticky='w')
        year_to = tk.Label(when_frame, text="To", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        year_to.grid(row=2, sticky='w')
        now = datetime.datetime.now()

        self.wrong_query_date = tk.Message(when_frame, text="Date 'from' can't be bigger than 'to'.",
                                           font=(functions.FONT, 9), width=120, fg="#8B0000")

        """
        changes content of comboboxes (years) when required
        """

        def change_comboboxes():
            for combo in self.comboboxes:
                combo.destroy()
                self.comboboxes.clear()

            combo_from = ttk.Combobox(when_frame, values=list(range(self.oldest(self.var_what.get()), now.year + 1)),
                                      textvariable=self.release_date_from_input, state="readonly")
            combo_from.grid(row=1, sticky='w')
            self.comboboxes.append(combo_from)
            combo_to = ttk.Combobox(when_frame, values=list(range(self.oldest(self.var_what.get()), now.year + 1)),
                                    textvariable=self.release_date_to_input, state="readonly")
            combo_to.grid(row=3, sticky='w')
            self.comboboxes.append(combo_to)

        change_comboboxes()

        #VOTES AVERAGE
        vote_frame = tk.LabelFrame(self.search_frame, text="VOTE AVERAGE", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        vote_frame.pack(fill='x')
        avg_from = tk.Label(vote_frame, text="From", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        avg_from.grid(row=0, sticky='w')
        avg_to = tk.Label(vote_frame, text="To", font=(functions.FONT, 10), fg=functions.FONT_COLOR)
        avg_to.grid(row=2, sticky='w')
        combo_avg_from = ttk.Combobox(vote_frame, values=list(x / 10 for x in range(0, 101)),
                                      textvariable=self.vote_average_from_input, state="readonly")
        combo_avg_from.grid(row=1, sticky='w')
        combo_avg_to = ttk.Combobox(vote_frame, values=list(x / 10 for x in range(0, 101)),
                                    textvariable=self.vote_average_to_input, state="readonly")
        combo_avg_to.grid(row=3, sticky='w')

        self.wrong_query_vote = tk.Message(vote_frame, text="Vote 'from' can't be bigger than 'to'.",
                                           font=(functions.FONT, 9), width=120, fg="#8B0000")

        """
        gets selected filters and sorting and shows results
        """

        def get_input():
            # GENRES
            genres = []
            for i in range(len(self.checkbuttons_states)):
                if self.checkbuttons_states[i].get():
                    genres.append(self.checkbuttons_input[i].cget("text"))

            self.title_input = enter_title.get()
            self.sorting_input = sort_combo.get()

            # TYPE OF PRODUCTION
            what_get = self.var_what.get()

            if what_get == 1:
                what = "movie"
            elif what_get == 2:
                what = "tv"

            # GET REST OF INFO
            title = self.title_input
            sorting = self.sorting_input
            date_from = self.release_date_from_input.get()
            date_to = self.release_date_to_input.get()
            vote_from = self.vote_average_from_input.get()
            vote_to = self.vote_average_to_input.get()

            self.actual_page = -1

            self.results_table.clear()
            self.pages_table.clear()

            # FILTER, SORT PRODUCTIONS AND GET MOST IMPORTANT INFO
            result = functions.search_filter_sort(what, title, genres, date_from, date_to, vote_from, vote_to, sorting)
            result = functions.filter_info(what, result)

            for item in self.results_table:
                item.grid_forget()

            for widget in self.results_grid_frame.winfo_children():
                widget.destroy()

            for widget in self.pages_frame.winfo_children():
                widget.destroy()

            """
            devides list into lists of n elements
            """

            def chunks(lst, n):
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]

            # INCONSISTENT FILTERS (DATE, VOTE)
            if len(self.release_date_from_input.get()) > 0 and len(self.release_date_to_input.get()) > 0 and len(self.vote_average_from_input.get()) > 0 and len(self.vote_average_to_input.get()) > 0:
                if int(self.release_date_from_input.get()) > int(self.release_date_to_input.get()) and float(self.vote_average_from_input.get()) > float(self.vote_average_to_input.get()):
                    self.wrong_query_date.grid(row=4, sticky='w')
                    self.wrong_query_vote.grid(row=4, sticky='w')
                    return

            if len(self.release_date_from_input.get()) > 0 and len(self.release_date_to_input.get()) > 0:
                if int(self.release_date_from_input.get()) > int(self.release_date_to_input.get()):
                    self.wrong_query_vote.grid_forget()
                    self.wrong_query_date.grid(row=4, sticky='w')
                    return

            if len(self.vote_average_from_input.get()) > 0 and len(self.vote_average_to_input.get()) > 0:
                if float(self.vote_average_from_input.get()) > float(self.vote_average_to_input.get()):
                    self.wrong_query_date.grid_forget()
                    self.wrong_query_vote.grid(row=4, sticky='w')
                    return

            """
            shows n-th page of results
            """

            def show_page(page):
                if self.actual_page != -1:
                    for child in self.results_table[self.actual_page]:
                        child.grid_forget()

                # CHANGE COLOR OF ACTUAL PAGE
                if self.actual_page != page:
                    self.pages_table[self.actual_page].configure(bg=self.default_bg, fg=self.default_fg)
                    self.pages_table[page].configure(bg=functions.SECOND_COLOR, fg="#FFFFFF")

                self.actual_page = page
                rows = math.ceil(len(self.results_table[page]) / 5)
                columns_last_row = len(self.results_table[page]) % 5

                # DEVIDE INTO COLUMNS AND ROWS
                for row in range(rows):
                    if row == rows - 1 and columns_last_row != 0:
                        columns = columns_last_row
                    else:
                        columns = 5
                    for column in range(columns):
                        self.results_table[page][row * 5 + column].grid(column=column, row=row, padx=10, sticky='n')

                for page_button in self.pages_table:
                    page_button.pack_forget()

                # SHOW PROPER NUMBER OF PAGES
                if self.pages_amount < 11:
                    for page_button in self.pages_table:
                        page_button.pack(side=tk.LEFT)
                else:
                    if page <= 5:
                        for i in range(10):
                            self.pages_table[i].pack(side=tk.LEFT)
                    elif page >= self.pages_amount - 5:
                        for i in range(self.pages_amount - 10, self.pages_amount):
                            self.pages_table[i].pack(side=tk.LEFT)
                    else:
                        for i in range(page - 5, page + 5):
                            self.pages_table[i].pack(side=tk.LEFT)

                self.scroll_frame.canvas.yview_moveto('0.0')

            self.wrong_query_date.grid_forget()
            self.wrong_query_vote.grid_forget()

            # NO RESULTS
            if len(result) == 0:
                no_results = tk.Label(self.results_grid_frame, text="Sorry, there are no results for your query:(",
                                      font=(functions.FONT, 30), bg=functions.BG_COLOR, fg=functions.FONT_COLOR, pady=100)
                no_results.pack(fill='x', expand=True, anchor='center')

            # RESULTS
            else:
                for i in range(len(result)):
                    SingleProdView(self.results_grid_frame, self.results_table, i, result, False)

                self.results_table = list(chunks(self.results_table, 20))
                self.pages_amount = len(self.results_table)

                # PAGES
                for i in range(len(self.results_table)):
                    button = tk.Button(self.pages_frame, text=(i + 1), command=lambda page=i: show_page(page), fg=functions.FONT_COLOR)
                    self.pages_table.append(button)

                self.default_bg = self.pages_table[0].cget("background")
                self.default_fg = self.pages_table[0].cget("foreground")

                show_page(0)

        # SEARCH
        search_button = tk.Button(button_frame, text="SEARCH", font=(functions.FONT, 12, "bold"), pady=5, padx=25,
                                  command=lambda: get_input(), bg=functions.THIRD_COLOR, fg="#FFFFFF")
        search_button.pack(fill='x', expand=True)
