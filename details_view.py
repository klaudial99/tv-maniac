import tkinter as tk
from io import BytesIO
import requests as reqs
from PIL import ImageTk, Image
import functions
from scroll import ScrollableFrame


class DetailsView:

    """
    creates details view with info about specific production
    """

    def __init__(self, master, what, id, photo):

        self.scroll_frame = ScrollableFrame(master)
        self.scroll_frame.pack(fill='both', expand=True)

        self.details_frame = tk.LabelFrame(self.scroll_frame.scrollable_frame, bg=functions.BG_COLOR)
        self.details_frame.grid(column=0, row=0, padx=30, pady=50)

        self.info = functions.get_info_about(what, id, True)

        functions.write_history(what, id)

        self.place_poster(photo)
        self.place_info(self.info, what)

    """
    send request to get poster of production and places it
    """

    def place_poster(self, photo):
        if photo is not None:
            img_url = "https://image.tmdb.org/t/p/w300" + photo
            img_data = reqs.get(img_url).content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((300, 450), Image.ANTIALIAS))
        else:
            img_path = functions.ICONS_PATH + "300x450.png"
            img = tk.PhotoImage(file=img_path)

        photo_label = tk.Label(self.details_frame, image=img, bg="#FFFFFF")
        photo_label.image = img
        photo_label.grid(row=0, column=0, rowspan=5, sticky='nw')

    """
    places info about production
    """

    def place_info(self, info, what):

        title = tk.Message(self.details_frame, text=info[0], padx=10, font=(functions.FONT, 36), bg=functions.BG_COLOR,
                           fg=functions.FONT_COLOR, width=700)
        title.grid(row=0, column=1, sticky='w')

        if what == "movie":
            date = info[1]
            details_text = info[4]
            genres = info[2]
        elif what == "tv":
            if info[6] == "Ended":
                if info[1] == info[2]:
                    date = info[1]
                else:
                    date = str(info[1]) + " - " + str(info[2])
            else:
                date = str(info[1]) + " - now"

            details_text = info[5]
            genres = info[3]

        genres = ", ".join(genres)
        genres.replace("{", "").replace("}", "")

        genres_label = tk.Message(self.details_frame, text=genres, padx=10, font=(functions.FONT, 24), bg=functions.BG_COLOR, fg=functions.FONT_COLOR, width=700)
        genres_label.grid(row=1, column=1, sticky='nw')

        year = tk.Label(self.details_frame, text=date, padx=10, font=(functions.FONT, 24), bg=functions.BG_COLOR, fg=functions.FONT_COLOR)
        year.grid(row=2, column=1, sticky='nw')

        rating = tk.Label(self.details_frame, text=str(info[-1]) + "/10", padx=10, bg=functions.BG_COLOR, fg=functions.FONT_COLOR,
                          font=(functions.FONT, 18))
        rating.grid(row=3, column=1, sticky='w')

        details = tk.Message(self.details_frame, text=details_text, padx=10, font=(functions.FONT, 16), bg=functions.BG_COLOR,
                             fg=functions.FONT_COLOR, width=700)
        details.grid(row=4, column=1, sticky='w')

        self.details_frame.rowconfigure(0, weight=1)
        self.details_frame.rowconfigure(1, weight=1)
        self.details_frame.rowconfigure(2, weight=1)
        self.details_frame.rowconfigure(3, weight=1)
        self.details_frame.rowconfigure(4, weight=5)
