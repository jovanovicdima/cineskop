import os
import requests
from movie import Movie, TicketInfo
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime

def getMovie(movieURL, pageInstance):
    pageInstance.goto(movieURL)
    pageInstance.locator('select.select2-offscreen').select_option("615") # 615 - "Cineplexx Niš"
    request = pageInstance.inner_html("body", timeout=5000)
    html = BeautifulSoup(request, 'html.parser')

    movie = Movie(html.find("h1").findNext("h1").text.strip(), pageInstance.url) # movie name
    item = html.find("tr") # original name
    movie.originalTitle = item.findNext("td").findNext("td").text.strip()
    item = item.findNext("tr").findNext("tr") # running time
    if item.findNext("td").text == "Dužina trajanja filma:": # some movies dont have running time info
        movie.runningTime = item.findNext("td").findNext("td").text[:-4].strip()
        item = item.findNext("tr") # country of origin
    else:
        movie.runningTime = 0
    movie.countryOfOrigin = item.findNext("td").findNext("td").text[:-5].strip()
    item = item.findNext("tr") # genre
    movie.genre = item.findNext("td").findNext("td").text.strip()
    item = item.findNext("tr") # cast
    movie.cast = item.findNext("td").findNext("td").text.strip()
    item = item.findNext("tr") # director
    movie.director = item.findNext("td").findNext("td").text.strip()

    imgName = os.path.basename(movie.originalTitle) + ".jpeg"
    if os.path.exists(f"../frontend/images/{imgName}"):
        print(f"Image {imgName} already downloaded.")
    else:
        imgData = requests.get("https://www.cineplexx.rs" + html.find("a", class_ = "pull-left").findNext("img")["src"]).content
        with open(os.path.join("..", "frontend", "images", imgName), 'wb') as f:
            f.write(imgData)
            print(f"Image {imgName} downloaded successfully.")

    item = item.findNext("div", class_ = "two-columns")
    synopsis = item.find_all("p")
    for x in synopsis:
        movie.synopsis += x.text + "\n"
    movie.synopsis = movie.synopsis.rstrip("\n")

    item = item.findNext("div", class_ = "span9")
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
        
        price = 0
        try:
            pageInstance.goto(ticketLink)
            pageInstance.wait_for_load_state('load');

            retryCount = 0
            maxRetries = 3
            while retryCount < maxRetries:
                try:
                    priceClicker = pageInstance.locator(f'img[title="Slobodno"]').nth(0)
                    priceClicker.click()
                    request = pageInstance.inner_html("span.uk-vertical-align-middle.priceunit", timeout=3000)
                    # Attempt to find the selector
                    if priceClicker is not None:
                        # Element found, break out of the loop
                        break
                except:
                    # Selector not found, wait and retry
                    retryCount += 1
                    print(f"Selector not found. Retrying {retryCount}/{maxRetries}...")

            html = str(BeautifulSoup(request, 'html.parser'))
            price = int(html[html.index("R") + 4:html.index(",")])
        except Exception as error:
            print(f"cineplexx price error: {error}")

        movie.tickets.append(TicketInfo(projectionTime, projectionType, auditorium, ticketStatus, price, ticketLink))

        item = item.findNext(class_ = "span3")
        
    return movie

def cineplexx():
    movies = []
    if not os.path.exists("../frontend/images"):
        os.makedirs("../frontend/images")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True, slow_mo=1000)
        page = browser.new_page()

        for i in range(12):
            page.goto("https://www.cineplexx.rs/filmovi/repertoar/")
            page.locator('select.isset[name=centerId]').select_option("615")
            try:
                page.locator('select[name="date"]').select_option(index=i + 1, timeout=300) # timeout is set to >=300ms so ticketStatus can be determined
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
