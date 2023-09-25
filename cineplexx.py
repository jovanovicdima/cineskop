from movie import Movie, TicketInfo
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime

def getMovie(movieURL, pageInstance):
    pageInstance.goto(movieURL)
    pageInstance.locator('select.select2-offscreen').select_option("615") # 615 - "Cineplexx Niš"
    request = pageInstance.inner_html("body", timeout=5000)
    html = BeautifulSoup(request, 'html.parser')

    movie = Movie(html.find("h1").findNext("h1").text, pageInstance.url) # movie name
    html = item = html.find("tr") # original name
    movie.originalTitle = item.findNext("td").findNext("td").text
    item = item.findNext("tr").findNext("tr") # running time
    if item.findNext("td").text == "Dužina trajanja filma:": # some movies dont have running time info
        movie.runningTime = item.findNext("td").findNext("td").text[:-4]
        item = item.findNext("tr") # country of origin
    else:
        movie.runningTime = 0
    movie.countryOfOrigin = item.findNext("td").findNext("td").text[:-5]
    item = item.findNext("tr") # genre
    movie.genre = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # cast
    movie.cast = item.findNext("td").findNext("td").text
    item = item.findNext("tr") # director
    movie.director = item.findNext("td").findNext("td").text

    item = html.findNext("div", class_ = "span9")
    if item == None: return [] # no projections

    # ticket info    
    item = item.find(class_ = "span3")
    while item != None:
        date = item.find("a")["data-link"]
        date = date[date.find("/date/") + 6:date.find("/program/")]
        time = item.find("p", class_ = "time-desc").text
        projectionTime = datetime.strptime(date + time, "%Y-%m-%d %H:%M ")

        ticketStatus = item.find("span", class_ = "icon_20px_Ticket")["class"][1]
        if "green-font" in ticketStatus: # purchasable online, reservation available
            ticketStatus = 0
        elif "orange-font" in ticketStatus: # purchasable online, reservation not available
            ticketStatus = 1
        elif "red-font" in ticketStatus: # only purchasable in person
            ticketStatus = 3
        else: # reservations not available
            ticketStatus = 4 
        

        ticketLink = item.find("a")["href"]
        auditorium = item.find("p", class_ = "room-desc").text.strip()
        projectionType = item.find("p", class_ = "mode-desc").text.strip()
        if projectionType == "":
            projectionType = "Digital 2D"

        movie.tickets.append(TicketInfo(projectionTime, projectionType, auditorium, ticketStatus, ticketLink))

        item = item.findNext(class_ = "span3")
        
    return movie

def cineplexx():
    movies = []
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True, slow_mo=300)
        page = browser.new_page()

        for i in range(12):
            page.goto("https://www.cineplexx.rs/filmovi/repertoar/")
            page.locator('select.isset[name=centerId]').select_option("615")
            try:
                page.locator('select.isset[name="date"]').select_option(index=i, timeout=300) # timeout is set to >=300ms so ticketStatus can be determined
            except:
                continue
            request = page.inner_html("div.container", timeout=5000)
            html = BeautifulSoup(request, 'html.parser')
            item = html.find(class_ = "span6")
            item = item.find("h2")

            while item != None:
                link = "https:" + item.find("a")["href"]
                if(not(any(link == movie.href for movie in movies))):
                    print(link)
                    movies.append(getMovie(link, page))
                item = item.findNext("h2")
    
    return movies