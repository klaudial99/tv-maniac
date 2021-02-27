import os
import pickle
import requests as reqs
from datetime import date
import json
from start_view_section import StartViewSection

MIN_VOTES_MOVIE = ""
MIN_VOTES_TV = ""
API_KEY = ""
INCOGNITO = ""
BG_COLOR = ""
FONT = ""
FONT_COLOR = ""
SECOND_COLOR = ""
THIRD_COLOR = ""
ICONS_PATH = "%s/Icons/" % os.curdir

ACTUAL_HISTORY_OBJECT = None
ACTUAL_HISTORY_OBJECT_MASTER = None

"""
sends request and get results from all pages

:param what: type of production - movie or tv
:return: list of productions with min x votes
"""


def get_productions(what):
    if what == "movie":
        url = "https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEY + \
              "&language=en-US&include_adult=false&include_video=false&vote_count.gte=" + MIN_VOTES_MOVIE
    elif what == "tv":
        url = "https://api.themoviedb.org/3/discover/tv?api_key=" + API_KEY + \
              "&language=en-US&include_null_first_air_dates=false&vote_count.gte=" + MIN_VOTES_TV

    response = reqs.get(url)
    response_dict = json.loads(response.text)
    all_productions = []
    for page in range(1, response_dict["total_pages"] + 1):

        url_page = url + "&page=" + str(page)
        response_page = reqs.get(url_page)
        response_dict_page = json.loads(response_page.text)
        for result in response_dict_page["results"]:
            all_productions.append(result)

    return all_productions


"""
sends request and get info about genres

:param what: type of production - movie or tv
:return: list of available genres and dictionary of mapped ids to genres
"""


def get_genres(what):
    if what == 1:
        what = "movie"
    elif what == 2:
        what = "tv"
    url = "https://api.themoviedb.org/3/genre/" + what + "/list?api_key=" + API_KEY + "&language=en-US"

    response = reqs.get(url)
    resp = json.loads(response.text)
    genres = []
    for i in resp["genres"]:
        genres.append(i["name"])

    return genres, resp


"""
from all productions chooses list of those that match user's filers

:param what: type of production - movie or tv
:param title: demanded title or it's part
:param genres: list of demanded genres
:param year_from: the earliest demanded year of release
:param year_to: the latest demanded year of release
:param vote_from: the smallest demanded average vote
:param vote_to: the biggest demanded average vote
:return: list of productions that matches the filters
"""


def filter_results(what, title, genres, year_from, year_to, vote_from, vote_to):
    results = get_productions(what)
    index_delete = []

    if what == "movie":
        prod_title = "title"
        genres_map = get_genres(1)[1]["genres"]
        date = "release_date"
    elif what == "tv":
        prod_title = "name"
        genres_map = get_genres(2)[1]["genres"]
        date = "first_air_date"

    for i in range(len(results)):

        if len(title) > 0:
            if title.lower() not in results[i][prod_title].lower():
                index_delete.append(i)
                continue

        if len(genres) > 0:
            to_delete = True

            for genre in genres:
                gen_id = 0
                for gen in genres_map:
                    if gen["name"] == genre:
                        gen_id = gen["id"]
                if gen_id in results[i]["genre_ids"]:
                    to_delete = False
                    break
                if not to_delete:
                    break
            if to_delete:
                index_delete.append(i)
                continue

        if len(year_from) > 0:
            if int(year_from) > int(results[i][date][:4]):
                index_delete.append(i)
                continue

        if len(year_to) > 0:
            if int(results[i][date][:4]) > int(year_to):
                index_delete.append(i)
                continue

        if len(vote_from) > 0:
            if float(vote_from) > float(results[i]["vote_average"]):
                index_delete.append(i)
                continue

        if len(vote_to) > 0:
            if float(results[i]["vote_average"]) > float(vote_to):
                index_delete.append(i)
                continue
    correct = []
    for i in range(len(results)):
        if i not in index_delete:
            correct.append(results[i])

    return correct


"""
sorts list of productions

:param what: type of production - movie or tv
:param results: list of productions to sort
:param sorting_type: demanded type of sorting
:return: sorted list of productions
"""


def sort_results(what, results, sorting_type):
    def switch_case(value):
        switch = {
            "A-Z": lambda: (["title", "name"], False),
            "Z-A": lambda: (["title", "name"], True),
            "release date - asc": lambda: (["release_date", "first_air_date"], False),
            "release date - desc": lambda: (["release_date", "first_air_date"], True),
            "popularity - asc": lambda: (["popularity", "popularity"], False),
            "popularity - desc": lambda: (["popularity", "popularity"], True),
            "vote average - asc": lambda: (["vote_average", "vote_average"], False),
            "vote average - desc": lambda: (["vote_average", "vote_average"], True),
        }
        func = switch.get(value, lambda: (["", ""], False))

        return func()

    if what == "movie":
        index = 0
    elif what == "tv":
        index = 1

    if len(sorting_type) > 0:
        results = sorted(results, key=lambda k: (k[switch_case(sorting_type)[0][index]]),
                         reverse=switch_case(sorting_type)[1])

    return results


"""
uses functions to filter and sort results

:param what: type of production - movie or tv
:param title: demanded title or it's part
:param genres: list of demanded genres
:param year_from: the earliest demanded year of release
:param year_to: the latest demanded year of release
:param vote_from: the smallest demanded average vote
:param vote_to: the biggest demanded average vote
:param sorting_type: demanded type of sorting
:return: filtered and sorted list of productions
"""


def search_filter_sort(what, title, genres, year_from, year_to, vote_from, vote_to, sorting_type):
    after_filtres = filter_results(what, title, genres, year_from, year_to, vote_from, vote_to)

    if len(sorting_type) > 0:
        after_filtres = sort_results(what, after_filtres, sorting_type)

    return after_filtres


"""
sends request about specific production

:param what: type of production - movie or tv
:param id: id of production
:param extended: boolean, chooses extended version of info
:return: list of information about demanded production
"""


def get_info_about(what, id, extended):
    url = "https://api.themoviedb.org/3/" + what + "/" + str(id) + "?api_key=" + API_KEY + "&language=en-US"
    response = reqs.get(url)
    resp = json.loads(response.text)
    genres = []
    for i in resp["genres"]:
        genres.append(i["name"])

    if extended:
        if what == "movie":
            info = [resp["title"], resp["release_date"][:4], genres, resp["poster_path"], resp["overview"],
                    resp["vote_average"]]
        elif what == "tv":
            info = [resp["name"], resp["first_air_date"][:4], resp["last_air_date"][:4], genres, resp["poster_path"],
                    resp["overview"], resp["status"], resp["vote_average"]]
    else:
        if what == "movie":
            info = ["movie", resp["id"], resp["poster_path"], resp["title"], resp["vote_average"]]
        elif what == "tv":
            info = ["tv", resp["id"], resp["poster_path"], resp["name"], resp["vote_average"]]

    return info


"""
chooses most important info about productions

:param what: type of production - movie or tv
:param data: dictionary with full info of productions
:return: list with most important info about productions
"""


def filter_info(what, data):
    info = []
    for prod in data:
        if what == "movie":
            info.append(["movie", prod["id"], prod["poster_path"], prod["title"], prod["vote_average"]])
        elif what == "tv":
            info.append(["tv", prod["id"], prod["poster_path"], prod["name"], prod["vote_average"]])

    return info


"""
sends request and check the oldest production within type

:param what: type of production - movie or tv
:return: year of the oldest production
"""


def get_oldest_release_year(what):
    if what == "movie":
        url = "https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEY + \
              "&language=en-US&sort_by=primary_release_date.asc&include_adult=false&include_video=false&page=1&vote_count.gte=" + MIN_VOTES_MOVIE
    elif what == "tv":
        url = "https://api.themoviedb.org/3/discover/tv?api_key=" + API_KEY + \
              "&language=en-US&sort_by=first_air_date.asc&page=1&include_null_first_air_dates=false&vote_count.gte=" + MIN_VOTES_TV

    response = reqs.get(url)
    response_dict = json.loads(response.text)

    if what == "movie":
        return response_dict["results"][0]["release_date"][:4]
    elif what == "tv":
        return response_dict["results"][0]["first_air_date"][:4]


"""
chooses most important info about top productions from specific year

:param what: type of production - movie or tv
:param year: demanded year of release
:param how_many: demanded number of productions
:param reverse: boolean, chooses reverse order of results
:return: list with most important info about productions
"""


def get_top_year(what, year, how_many, reverse):
    productions = get_productions(what)
    correct = []

    for prod in productions:
        if what == "movie":
            if prod["release_date"][:4] == str(year):
                correct.append(prod)
        elif what == "tv":
            if prod["first_air_date"][:4] == str(year):
                correct.append(prod)

    correct = sorted(correct, key=lambda k: (k["vote_average"], k["popularity"]), reverse=reverse)[:how_many]

    info = []
    for prod in correct:
        if what == "movie":
            info.append(["movie", prod["id"], prod["poster_path"], prod["title"], prod["vote_average"]])
        elif what == "tv":
            info.append(["tv", prod["id"], prod["poster_path"], prod["name"], prod["vote_average"]])

    return info


"""
create file with most important info about top productions from specific year if required 
or read that info from existing file

:param what: type of production - movie or tv
:param year: demanded year of release
:param how_many: demanded number of productions
:param reverse: boolean, chooses reverse order of results
:return: list with most important info about productions
"""


def get_top_year_config_file(what, year, how_many, reverse):

    def save_to_file(name, object):
        with open(name, 'wb') as file:
            pickle.dump(object, file)

    def load_from_file(name):
        with open(name, 'rb') as file:
            return pickle.load(file)

    today = str(date.today())
    name = "config_" + what + "_" + today + ".txt"
    correct = ""
    for file_name in os.listdir(os.getcwd()):
        if file_name.startswith("config_" + what):
            correct = file_name

    if len(correct) == 0:
        info = get_top_year(what, year, how_many, reverse)
        save_to_file(name, info)
    else:
        if correct != name:
            os.remove(correct)
            info = get_top_year(what, year, how_many, reverse)
            save_to_file(name, info)
            return info

        info = load_from_file(name)

    return info


"""
add new production to history file and refresh displayed history

:param what: type of production - movie or tv
:param id: id of production
"""


def write_history(what, id):
    global ACTUAL_HISTORY_OBJECT, ACTUAL_HISTORY_OBJECT_MASTER
    if not INCOGNITO:
        lines = ""
        my_line = what + " " + str(id) + "\n"
        if os.path.exists("history.txt"):
            with open("history.txt", "r") as file:
                for line in file.readlines():
                    if line != my_line:
                        lines += line
        else:
            ACTUAL_HISTORY_OBJECT_MASTER.grid(column=0, row=2, pady=30, sticky='w', padx=30)
        lines += my_line
        with open("history.txt", "w") as file:
            file.write(lines)

        if ACTUAL_HISTORY_OBJECT is not None:
            ACTUAL_HISTORY_OBJECT = ""

        ACTUAL_HISTORY_OBJECT = StartViewSection(ACTUAL_HISTORY_OBJECT_MASTER, "last")


"""
reads file with history and takes max 10 elements

:return: list with info about productions from history and number how many to display
"""


def read_history():
    info = []
    with open("history.txt", "r") as file:
        lines = []
        for line in file.readlines():
            words = line.split(" ")
            words_to_add = []
            for word in words:
                words_to_add.append(word.replace("\n", ""))
            lines.append(words_to_add)
        if len(lines) != 0 and len(lines) <= 10:
            lines.reverse()
            how_many_last = len(lines)
        else:
            lines = lines[-10:]
            lines.reverse()
            how_many_last = 10

        for line in lines:
            details = get_info_about(line[0], line[1], True)
            if line[0] == "movie":
                poster = details[3]
            elif line[0] == "tv":
                poster = details[4]
            info.append([line[0], line[1], poster, details[0], details[-1]])

        return info, how_many_last


"""
deletes file with history 
"""

def delete_history():
    if os.path.exists("history.txt"):

        for widget in ACTUAL_HISTORY_OBJECT_MASTER.winfo_children():
            widget.grid_forget()
        ACTUAL_HISTORY_OBJECT_MASTER.grid_forget()
        os.remove("history.txt")
        global ACTUAL_HISTORY_OBJECT
        ACTUAL_HISTORY_OBJECT = None


"""
creates file with configuration info if required 
or read that info from existing file

:param name: name of config file
"""


def read_config_file(name):
    config_dict = { "MIN_VOTES_MOVIE": str(2500),
                    "MIN_VOTES_TV": str(500),
                    "API_KEY": "e4e6acdc6a73d9fbd3d5033d86283840",
                    "INCOGNITO": False,
                    "BG_COLOR": "#FFFFFF",
                    "FONT": "Century Gothic",
                    "FONT_COLOR": "#161616",
                    "SECOND_COLOR": "#FF2D55",
                    "THIRD_COLOR": "#008898"}

    if os.path.exists(name):
        with open(name, 'r') as file:
            for line in file.readlines():
                words = line.split("=")
                config_dict[words[0]] = words[1].replace("\n", "")
    else:
        with open(name, 'w') as file:
            for key, value in config_dict.items():
                file.write(str(key) + "=" + str(value) + "\n")

    global MIN_VOTES_MOVIE, MIN_VOTES_TV, API_KEY, INCOGNITO, BG_COLOR, FONT, FONT_COLOR, SECOND_COLOR, THIRD_COLOR, ICONS_PATH
    MIN_VOTES_MOVIE = config_dict["MIN_VOTES_MOVIE"]
    MIN_VOTES_TV = config_dict["MIN_VOTES_TV"]
    API_KEY = config_dict["API_KEY"]
    INCOGNITO = True if config_dict["INCOGNITO"] == "True" else False
    BG_COLOR = config_dict["BG_COLOR"]
    FONT = config_dict["FONT"]
    FONT_COLOR = config_dict["FONT_COLOR"]
    SECOND_COLOR = config_dict["SECOND_COLOR"]
    THIRD_COLOR = config_dict["THIRD_COLOR"]
