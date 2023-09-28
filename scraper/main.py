from cineplexx import cineplexx
from cineGrand import cineGrand
from vilinGrad import vilinGrad
import psycopg

def writeMoviesToDatabase(movies, cinemaName):
    for item in movies:
        try:
            # movies table
            query = 'INSERT INTO movies (title, originaltitle, runningtime, genre, countryoforigin, director, "cast") VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (originaltitle) DO UPDATE SET (runningtime) = ROW(EXCLUDED.runningtime)'
            params = (item.title, item.originalTitle, int(item.runningTime), item.genre, item.countryOfOrigin, item.director, item.cast)
            cursor.execute(query, params)
            connection.commit()
            print(f"{item.title} | {item.originalTitle} | {item.runningTime} | {item.countryOfOrigin} | {item.director} | {item.cast} | {item.href} | {item.genre}")
        except Exception as error:
            print(f"{item.title} - movies table error: {error}")

        try:
            # movielinks table
            query = "INSERT INTO movielinks (movieid, cinemaid, link) VALUES (%s, %s, %s) ON CONFLICT (movieid, cinemaid) DO NOTHING"
            movieID = cursor.execute(f"SELECT id FROM movies WHERE originaltitle = '{item.originalTitle}'").fetchone()[0]
            cinemaID = cursor.execute(f"SELECT id FROM cinemas WHERE name = '{cinemaName}'").fetchone()[0]
            params = (movieID, cinemaID, item.href)

            cursor.execute(query, params)
            connection.commit()
        except Exception as error:
            print(f"{item.title} - movielinks table error: {error}")

        for ticket in item.tickets:
            try:
                # projections table
                query = "INSERT INTO projections (movieid, cinemaid, time, auditorium, projectiontype, link, status) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (movieid, cinemaid, time) DO NOTHING"
                params = (movieID, cinemaID, ticket.projectionTime, ticket.auditorium, ticket.projectionType, ticket.link, ticket.status)
                cursor.execute(query, params)
                connection.commit()
                print(f"{ticket.projectionTime} | {ticket.projectionType} | {ticket.auditorium} | {ticket.link} | {ticket.status}")
            except Exception as error:
                print(f"{ticket.projectionTime} - projections table error: {error}")

try:
    connection = psycopg.connect(
        host = "localhost",
        dbname = "dima",
        user = "dima",
        password = "dima",
        port = "5432")
    
    cursor = connection.cursor()
    print('Connected to the database. PostgreSQL database version: ' + str(cursor.execute("SELECT version()").fetchone()))

    writeMoviesToDatabase(cineplexx(), "Cineplexx")
    writeMoviesToDatabase(cineGrand(), "CineGrand")
    writeMoviesToDatabase(vilinGrad(), "Vilingrad")

except Exception as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print("Database connection terminanted.")
