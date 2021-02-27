import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter import messagebox
import functions
from search_view import SearchView
from start_view import StartView

"""
opens window with help
"""


def help_view():
    top = tk.Toplevel(bg=functions.BG_COLOR)

    top.wm_geometry("750x350")
    info = tk.Message(top, text="""Welcome to our app!
    
We're here to help you find any movie or tv series. Just look, it's very simple.

On the home page you can find best productions of last year and your history. You can switch the incognito mode if you don't want to save your history. There is a button in a bottom part. 

If you want to personalize your query just go to search page, choose whatever you're interested in and click 'SEARCH' button

Hope you'll enjoy it!
""", font=(functions.FONT, 12), width=700, pady=50, bg=functions.BG_COLOR, fg=functions.FONT_COLOR)
    info.pack()


"""
opens site of TMDb
"""


def open_site():
    webbrowser.open('https://www.themoviedb.org/')


class BaseWindow:

    """
    creates base window with menu, bottombar and tabs
    """

    def __init__(self, master):
        self.master = master
        self.master.title("TV Maniac")

        # MENU
        self.menubar = tk.Menu(self.master)
        self.master["menu"] = self.menubar

        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Exit", underline=0, command=self.exit)

        self.history_menu = tk.Menu(self.menubar)
        self.history_menu.add_command(label="Delete history", underline=0, command=functions.delete_history)
        self.history_menu.add_command(label="Switch incognito mode", underline=0, command=self.switch_incognito)

        self.help_menu = tk.Menu(self.menubar)
        self.help_menu.add_command(label="TMDb's site", underline=0, command=open_site)
        self.help_menu.add_command(label="Help", underline=0, command=help_view)

        self.menubar.add_cascade(label="File", menu=self.file_menu, underline=0)
        self.menubar.add_cascade(label="History", menu=self.history_menu, underline=0)
        self.menubar.add_cascade(label="About", menu=self.help_menu, underline=0)

        # BOTTOMBAR
        self.bottombar = tk.LabelFrame(master)
        self.bottombar.pack(side=tk.BOTTOM, anchor='w', fill='x')
        logo_path = functions.ICONS_PATH + "logo.png"
        self.logo = tk.PhotoImage(file=logo_path)
        self.logo_label = tk.Label(self.bottombar, image=self.logo)
        self.logo_label.pack(side=tk.LEFT, padx=20, pady=5)
        self.statusbar_text = tk.Label(self.bottombar,
                                       text="This product uses the TMDb API but is not endorsed or certified by TMDb",
                                       font=(functions.FONT, 10))
        self.statusbar_text.pack(side=tk.LEFT)

        self.incognito_button = tk.Button(self.bottombar, fg="#FFFFFF", command=self.switch_incognito, text="OFF",
                                          bg="#8B0000", width=10)
        self.incognito_button.pack(side=tk.RIGHT, padx=20)

        self.incognito_text = tk.Label(self.bottombar, text="INCOGNITO MODE:", font=(functions.FONT, 11))
        self.incognito_text.pack(side=tk.RIGHT)

        # TABS
        self.tab_control = ttk.Notebook(self.master)
        self.tab_control.pack(expand=1, fill="both")

        self.home_tab = tk.Frame(self.tab_control)
        self.start = StartView(self.home_tab)

        self.search_tab = tk.Frame(self.tab_control)
        self.search = SearchView(self.search_tab)

        self.tab_control.add(self.home_tab, text='Home')
        self.tab_control.add(self.search_tab, text='Search')

    """
    exits from app
    """

    def exit(self):
        answer = tk.messagebox.askyesno("TVManiac", "Do you want to exit?", parent=self.master)
        if answer:
            self.master.destroy()

    """
    switches incognito mode
    """

    def switch_incognito(self):
        if functions.INCOGNITO:
            self.incognito_button.configure(bg="#8B0000", text="OFF")
            functions.INCOGNITO = False
        else:
            self.incognito_button.configure(bg="#006400", text="ON")
            functions.INCOGNITO = True


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1300x750')
    functions.read_config_file("config_file.txt")
    icon_path = functions.ICONS_PATH + "television.png"
    root.iconphoto(True, tk.PhotoImage(file=icon_path))
    root.resizable(False, False)
    app = BaseWindow(root)
    root.mainloop()
