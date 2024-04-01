import requests
import os
from movie import Movie, TicketInfo
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def getMovie(movieURL):
    request = requests.get(movieURL)
    html = BeautifulSoup(request.content, "html.parser")
    # item = html.find("div", class_ = "col-md-4")
    item = html.find("div", class_ = "row")

    movie = Movie(item.findNext("h1").text, movieURL)
    item = item.findNext("li") # original title
    movie.originalTitle = item.text[item.text.find(":") + 1:].strip() 
    item = item.findNext("li") # running time
    movie.runningTime = item.text[item.text.find(":") + 1:].strip()
    item = item.findNext("li") 
    item = item.findNext("li") # country of origin
    movie.countryOfOrigin = item.text[item.text.find(":") + 1:].strip()
    item = item.findNext("li") # director
    movie.director = item.text[item.text.find(":") + 1:].strip()
    item = item.findNext("li") # cast
    movie.cast = item.text[item.text.find(":") + 1:].strip()
    item = item.findNext("p")
    movie.genre = item.text[item.text.find(":") + 1:].strip()
    movie.trailerLink = html.find("iframe")["src"]

    item = html.find("div", class_ = "descriptionFilm")
    item = item.find_all("p")
    for x in item:
        movie.synopsis += x.text + "\n"
    movie.synopsis = movie.synopsis.rstrip("\n")

    item = html.find("span", class_ = "filmscreeningsTime")
    while item != None:
        status = 3
        try:
            ticketLink = item.find("a")["href"]
            if ticketLink != "#":
                status = 2
            ticketLink = "http://vilingrad.rs" + ticketLink
            
        except:
            item = item.findNext("span", class_ = "filmscreeningsTime")
            continue

        projectionTime = item.find("time")
        date = datetime.strptime(projectionTime['datetime'][:10], "%Y-%m-%d").date() # converting parsed string to date format
        time = datetime.strptime(projectionTime['datetime'][11:] + projectionTime['datetime'][10] + 'M', "%I:%M%p").time() # converting parsed string to time format
        projectionTime = datetime.combine(date, time)

        projectionType = item.find("span", class_ = "value").text

        auditorium = "unknown"
        price = 0
        try:
            ticketLinkRequest = BeautifulSoup(requests.get("http://vgrez.gart.rs/Projection/FilmProjectionHall?projectionID=" + ticketLink[ticketLink.find("=") + 1:]).content, "html.parser")
            price = int(float(ticketLinkRequest.find("input", id="hidden-ticketPrice")["value"]))
            auditorium = ticketLinkRequest.find("h3", class_ = "projectionHall").text
        except:
            status = 4 # no tickets left
        
        item = item.findNext("span", class_ = "filmscreeningsTime")

        movie.tickets.append(TicketInfo(projectionTime, projectionType, auditorium, status, price, ticketLink))

    return movie
    
def vilinGrad():
    movies = []
    baseLink = "http://vilingrad.rs"
    imgPath = "../frontend/images"
    if not os.path.exists(imgPath):
        os.makedirs(imgPath)
    for i in range(7):
        url = "http://vilingrad.rs/na-repertoaru?ScreeningDate=" + (datetime.now() + timedelta(i)).strftime("%Y-%m-%d")
        request = requests.get(url)
        html = BeautifulSoup(request.content, "html.parser")
        results = html.find(class_="projection-page content-item")

        item = results.find("h1")
        while item != None:
            item = item.findNext("a")
            if(not(any(baseLink + item["href"] == movie.href for movie in movies))):
                    if(item["href"] == "/o-bioskopu"): return movies
                    movies.append(getMovie(baseLink + item["href"]))
                    print(item["href"])
                    item = item.findNext("img")
                    imgName = os.path.basename(movies[-1].originalTitle) + ".jpeg"
                    if os.path.exists(f"{imgPath}/{imgName}"):
                        print(f"Image {imgName} already downloaded.")
                    else:
                        imgData = requests.get(baseLink + item['src']).content
                        with open(os.path.join("..", "frontend", "images", imgName), 'wb') as f:
                            f.write(imgData)
                            print(f"Image {imgName} downloaded successfully.")
            item = item.findNext("h1")

    return movies
