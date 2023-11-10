class Movie:
    def __init__(self, title, href):
        self.title = title
        self.originalTitle = ""
        self.runningTime = ""
        self.countryOfOrigin = ""
        self.director = ""
        self.cast = ""
        self.href = href
        self.genre = ""
        self.tickets = []
        self.trailerLink = ""

class TicketInfo:
    def __init__(self, projectionTime, projectionType, auditorium, status, ticketLink):
        self.projectionTime = projectionTime
        self.projectionType = projectionType
        self.auditorium = auditorium
        self.link = ticketLink
        self.status = status
        # status 0 - purchasable online, reservation available
        # status 1 - purchasable online, reservation not available
        # status 2 - not purchasable online, reservations availabe
        # status 3 - only purchasable in person
        # status 4 - reservations not available