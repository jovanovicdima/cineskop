import requests
from bs4 import BeautifulSoup


class Movie:
    def __init__(self, age):
        self.age = age
        self.originalName = ""




url = "http://vilingrad.rs/na-repertoaru?ScreeningDate=2023-05-05"

html = requests.get(url)
s = BeautifulSoup(html.content, "html.parser")
results = s.find(class_="projection-page content-item")

imena = []
# ovo su imena fimlova po naski
x = s.find_all("h1")
for item in x:
    imena.append(item.text)
imena.pop(0)
imena.pop(0)

originalnaImena = []
# ovo su originalna imena filmova
names = results.find_all('p', "text-field text-field-originalname")
for name in names:
    originalnaImena.append(name.findNext("span", "value").text[1:])

duzinaTrajanja = []
# ovo su duzine trajanja filmova
duration = results.find_all('p', "numeric-field numeric-field-lengthminutes")
for item in duration:
    duzinaTrajanja.append(item.findNext("span", "value").text)

releaseDate = []
ostalo = results.find_all(class_="numeric-field numeric-field-lengthminutes")
for item in ostalo:
    releaseDate.append(item.findNext(class_="value").findNext(class_="value").text[1:-1])

countryOfOrigin = []
for item in ostalo:
    countryOfOrigin.append(item.findNext(class_="value").findNext(class_="value").findNext(class_="value").text[1:])

directors = []
for item in ostalo:
    directors.append(
        item.findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(class_="value").text[
        1:])

actors = []
for item in ostalo:
    actors.append(item.findNext(class_="value").findNext(class_="value").findNext(class_="value").findNext(
        class_="value").findNext(class_="value").text[1:])

# stampanje
for item in imena:
    print(item)
for item in originalnaImena:
    print(item)
for item in duzinaTrajanja:
    print(item)
