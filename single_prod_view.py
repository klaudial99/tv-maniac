import tkinter as tk
from io import BytesIO
import requests as reqs
from PIL import ImageTk, Image
import functions
from details_view import DetailsView

"""
creates window with details of specific production
"""


def create_window_details(what, id, photo):
    top = tk.Toplevel()
    top.wm_geometry("1100x500")
    DetailsView(top, what, id, photo)


class SingleProdView:

    """
    creates single production view with basic info about it
    """

    def __init__(self, master, table, i, data_source, number):
        self.m_frame = tk.Frame(master, bg=functions.BG_COLOR)

        # NUMBERS - ORDER
        if number:
            self.number = tk.Label(self.m_frame, text=(i + 1), padx=10, font=(functions.FONT, 20), anchor='w',
                                   bg=functions.BG_COLOR, fg=functions.FONT_COLOR)
            self.number.grid(row=0, sticky='w')

        # POSTER
        if data_source[i][2] is not None:
            img_url = "https://image.tmdb.org/t/p/w200" + data_source[i][2]
            img_data = reqs.get(img_url).content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((200, 300), Image.ANTIALIAS))
        else:
            img_path = functions.ICONS_PATH + "200x300.png"
            img = tk.PhotoImage(file=img_path)

        self.photo_label = tk.Label(self.m_frame, image=img, bg=functions.BG_COLOR)
        self.photo_label.image = img
        self.photo_label.grid(row=1)
        self.m_frame.rowconfigure(1, minsize=320)
        self.m_frame.rowconfigure(2, minsize=80)
        self.m_frame.rowconfigure(3, minsize=50)

        self.show_more_button = tk.Button(self.m_frame, text="Show details",
                                          command=lambda i_value=i: create_window_details(data_source[i_value][0],
                                                                                          data_source[i_value][1],
                                                                                          data_source[i_value][2]),
                                          fg="#FFFFFF",
                                          font=(functions.FONT, 11), bg=functions.SECOND_COLOR)
        self.show_more_button.grid(row=3, sticky='ne')

        self.rating = tk.Label(self.m_frame, text=str(data_source[i][-1]) + "/10", padx=5, bg=functions.BG_COLOR, fg=functions.FONT_COLOR,
                               font=(functions.FONT, 14))
        self.rating.grid(row=3, sticky='nw', pady=3)

        self.title_message = tk.Message(self.m_frame, text=data_source[i][3], padx=5, width=200, bg=functions.BG_COLOR,
                                        fg=functions.FONT_COLOR,
                                        font=(functions.FONT, 14))
        self.title_message.grid(row=2, sticky='nw')
        self.m_frame.update()

        table.append(self.m_frame)
