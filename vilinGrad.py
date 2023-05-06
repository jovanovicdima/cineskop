import requests
from bs4 import BeautifulSoup


class Movie:
    def __init__(self, title):
        self.title = title
        self.originalTitle = ""
        self.runningTime = ""
        self.releaseDate = ""
        self.countryOfOrigin = ""
        self.director = ""
        self.cast = []

# TODO - Create URL generator for target day
url = "http://vilingrad.rs/na-repertoaru?ScreeningDate=2023-05-05"

request = requests.get(url)
html = BeautifulSoup(request.content, "html.parser")
results = html.find(class_="projection-page content-item")


movies = []

# movie titles - creating array of Movie objects
titles = html.find_all("h1")
for runningTime in titles:
    movies.append(Movie(runningTime.text))

# first two items are not movie titles
movies.pop(0)
movies.pop(0)

# original titles
originalTitles = results.find_all('p', "text-field text-field-originalname")
i = 0
for originalTitle in originalTitles:
    movies[i].originalTitle = originalTitle.findNext("span", "value").text[1:]
    i = i + 1

# running time
runningTimes = results.find_all('p', "numeric-field numeric-field-lengthminutes")
i = 0
for runningTime in runningTimes:
    movies[i].runningTime = runningTime.findNext("span", "value").text
    i = i + 1

others = results.find_all(class_="numeric-field numeric-field-lengthminutes")

#release date
i = 0
for runningTime in others:
    movies[i].releaseDate = runningTime.findNext(class_="value").findNext(class_="value").text[1:-1]
    i = i + 1

# country of origin
i = 0
for runningTime in others:
    movies[i].countryOfOrigin = runningTime.findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:]
    i = i + 1

# director
i = 0
for runningTime in others:
    movies[i].director = runningTime.findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:]
    i = i + 1

# movie cast
i = 0
for runningTime in others:
    movies[i].cast = runningTime.findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:]
    i = i + 1

# stampanje
for runningTime in movies:
    print(runningTime.title + " | " + runningTime.originalTitle + " | " + runningTime.runningTime + " min | year " + runningTime.releaseDate + " | " + runningTime.countryOfOrigin + " | " + runningTime.director + " | " + runningTime.cast)