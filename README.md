# TV Maniac
### Python desktop application connecting via API to https://www.themoviedb.org/ (GUI made in tkinter)

### Functionalities:
- getting data from a configuration file
- displaying the most popular movies and TV series of the previous year
- searching for movies and series using filtering and sorting
- displaying details of each production
- keeping and displaying history of recently viewed productions
- switching the incognito mode, in which the browsing history is not saved
- clearing browsing history

### Installation and launching:
1. Install required modules:
```
pip install requests
pip install pillow
```
2. Edit the configuration file (config_file.txt) as needed
3. Start application
```
py main_app.py
```
4. Start view schould look like this:\
![Start view image](https://github.com/klaudial99/tv-maniac/raw/master/images/start-view.jpg)

#### Remark
The application was supposed to perform all operations on data sets itself, so it uses only the basic API features. Hence, the application does not run fast.\
During the first run on a given day, configuration files are updated, thanks to which the application loads faster on subsequent launchings.
