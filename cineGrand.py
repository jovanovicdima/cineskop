import requests
from movie import Movie
from bs4 import BeautifulSoup
from datetime import datetime

def getProjectionTime(movieURL):
    request = requests.get(movieURL)
    html = BeautifulSoup(request.content, "html.parser")
    dates = html.select('time[class*=date-time-field-time]')
    times = []
    for item in dates:
        date = datetime.strptime(item['datetime'][:10], "%Y-%m-%d").date() # converting parsed string to date format
        time = datetime.strptime(item['datetime'][11:] + ' ' + item['datetime'][10] + 'M', "%I:%M %p").time() # converting parsed string to time format
        times.append(datetime.combine(date, time))
    return times
        
url = "http://nis.cinegrand-mcf.rs/na-repertoaru?ScreeningDate=" + datetime.today().strftime("%Y-%m-%d")
request = requests.get(url)
html = BeautifulSoup(request.content, "html.parser")
results = html.find(class_="projection-page content-item")

movies = []

# movie titles - creating array of Movie objects
titles = html.find_all("h1")
for title in titles:
    movies.append(Movie(title.text, title.findNext('a', href = True)['href']))

# first two items are not movie titles
movies.pop(0)
movies.pop(0)

# original titles
originalTitles = results.find_all('p', "text-field text-field-originalname")
for i, originalTitle in enumerate(originalTitles):
    movies[i].originalTitle = originalTitle.findNext("span", "value").text[1:]

# running time
runningTimes = results.find_all('p', "numeric-field numeric-field-lengthminutes")
for i, runningTime in enumerate(runningTimes):
    movies[i].runningTime = runningTime.findNext("span", "value").text

others = results.find_all(class_="numeric-field numeric-field-lengthminutes")

#release date
for i, releaseDates in enumerate(others):
   movies[i].releaseDate = releaseDates.findNext(class_="value").findNext(class_="value").text[1:-1]

# country of origin
for i, countryOfOrigin in enumerate(others):
    movies[i].countryOfOrigin = countryOfOrigin.findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:]

# director
for i, directors in enumerate(others):
    movies[i].director = directors.findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:]

# movie cast
for i, movieCast in enumerate(others):
    movies[i].cast = movieCast.findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:]

# movie projection 
for item in movies:
    item.projectionTimes = getProjectionTime("http://vilingrad.rs/" + item.href)

# printing
for item in movies:
    print(item.title + " | " + item.originalTitle + " | " + item.runningTime + " min | year " + item.releaseDate + " | " + item.countryOfOrigin + " | " + item.director + " | " + item.cast)
    # print(item.title + " | " + item.href)
    for time in item.projectionTimes:
        print(time)
