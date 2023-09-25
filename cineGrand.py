import requests
from movie import Movie, TicketInfo
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def getMovie(movieURL):
    request = requests.get(movieURL)
    html = BeautifulSoup(request.content, "html.parser")
    item = html.find("div", class_ = "col-md-4")

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

    item = html.find("span", class_ = "filmscreeningsTime")
    while item != None:
        status = 2
        try:
            ticketLink = item.find("a")["href"]
            if ticketLink == "#":
                status = 3
            else:
                status = 2
            
        except:
            item = item.findNext("span", class_ = "filmscreeningsTime")
            continue

        projectionTime = item.find("time")
        date = datetime.strptime(projectionTime['datetime'][:10], "%Y-%m-%d").date() # converting parsed string to date format
        time = datetime.strptime(projectionTime['datetime'][11:] + projectionTime['datetime'][10] + 'M', "%I:%M%p").time() # converting parsed string to time format
        projectionTime = datetime.combine(date, time)

        projectionType = item.find("span", class_ = "value").text

        auditorium = "unknown"
        try:
            auditoriumRequest = BeautifulSoup(requests.get(ticketLink).content, "html.parser")
            auditorium = auditoriumRequest.find("h3", class_ = "projectionHall").text
        except:
            status = 4 # no tickets left
        
        item = item.findNext("span", class_ = "filmscreeningsTime")

        movie.tickets.append(TicketInfo(projectionTime, projectionType, auditorium, status, ticketLink))

    return movie
    
def cineGrand():
    movies = []

    for i in range(7):
        url = "http://nis.cinegrand-mcf.rs/na-repertoaru?ScreeningDate=" + (datetime.now() + timedelta(i)).strftime("%Y-%m-%d")
        request = requests.get(url)
        html = BeautifulSoup(request.content, "html.parser")
        results = html.find(class_="projection-page content-item")

        item = results.find("h1")
        while item != None:
            item = item.findNext("a")
            if(not(any("http://nis.cinegrand-mcf.rs" + item["href"] == movie.href for movie in movies))):
                    if(item["href"] == "/uslovi-poslovanja"): return movies
                    movies.append(getMovie("http://nis.cinegrand-mcf.rs" + item["href"]))
                    print(item["href"])
            item = item.findNext("h1")

    return movies
