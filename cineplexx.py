from movie import Movie
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def getProjectionTime(movieURL, page):
    page.goto(movieURL)
    page.locator('select.select2-offscreen').select_option("615")
    request = page.inner_html("body", timeout=5000)
    html = BeautifulSoup(request, 'html.parser')

    movie = Movie(html.find("h1").findNext("h1").text, page.url) # movie name
    html = item = html.find("tr") # original name
    movie.originalTitle = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # release date
    movie.releaseDate = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # running time
    movie.runningTime = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # country of origin
    movie.countryOfOrigin = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # genre
    # movie.genre = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # cast
    movie.cast = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # director
    movie.director = item.findNext("td").findNext("td").text

    item = html.findNext("div", class_ = "span9")
    if item == None: return [] # no projections

    item = item.find(class_ = "span3")
    while item != None:
        date = item.find("a")["data-link"]
        date = date[date.find("/date/") + 6:date.find("/program/")]
        time = item.find("p", class_ = "time-desc").text
        movie.projectionTimes.append(datetime.strptime(date + time, "%Y-%m-%d %H:%M "))
        item = item.findNext(class_ = "span3")

    return movie


movies = []

with sync_playwright() as playwright:
    browser = playwright.firefox.launch(headless=False, slow_mo=100)
    page = browser.new_page()

    for i in range(7):
        page.goto("https://www.cineplexx.rs/filmovi/repertoar/")
        page.locator('select.isset[name=centerId]').select_option("615")
        date = (datetime.today() + timedelta(i)).strftime("%Y-%m-%d")
        page.locator('select.isset[name="date"]').select_option(date)
        request = page.inner_html("div.container", timeout=5000)
        html = BeautifulSoup(request, 'html.parser')
        item = html.find(class_ = "span6")

        item = item.find("h2")

        while item != None:
            link = "https:" + item.find("a")["href"]
            if(any(link == movie.href for movie in movies)):
                item = item.findNext("h2")
                continue
            movies.append(getProjectionTime(link, page))

            item = item.findNext("h2")

for item in movies:
    print(item.title + " | " + item.originalTitle + " | " + item.runningTime + " min | year " + item.releaseDate + " | " + item.countryOfOrigin + " | " + item.director + " | " + item.cast)
    # print(item.title + " | " + item.href)
    for time in item.projectionTimes:
        print(time)        