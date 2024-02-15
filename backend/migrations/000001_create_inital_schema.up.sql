CREATE TABLE IF NOT EXISTS cinemas
(
    id serial NOT NULL,
    name text NOT NULL,
    link text NOT NULL,
    CONSTRAINT "cinemas_pkey" PRIMARY KEY (id),
    CONSTRAINT "name_ukey" UNIQUE (name)
);


CREATE TABLE IF NOT EXISTS movies
(
    id serial NOT NULL,
    title text NOT NULL,
    originaltitle text NOT NULL,
    runningtime smallint DEFAULT 0,
    synopsis text NOT NULL,
    genre text NOT NULL,
    countryoforigin text NOT NULL,
    director text NOT NULL,
    "cast" text NOT NULL,
    trailerlink text NOT NULL,
    CONSTRAINT "movies_pkey" PRIMARY KEY (id),
    CONSTRAINT "originaltitle_ukey" UNIQUE (originaltitle)
);

CREATE TABLE IF NOT EXISTS movielinks
(
    id serial NOT NULL,
    movieid integer NOT NULL,
    cinemaid integer NOT NULL,
    link text NOT NULL,
    CONSTRAINT "movielinks_pkey" PRIMARY KEY (id),
    CONSTRAINT "movielinks_ukey" UNIQUE (movieid, cinemaid),
    CONSTRAINT "cinemaid" FOREIGN KEY (cinemaid)
        REFERENCES cinemas (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "movieid" FOREIGN KEY (movieid)
        REFERENCES movies (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS projections
(
    id serial NOT NULL,
    movieid integer NOT NULL,
    cinemaid integer NOT NULL,
    "time" timestamp without time zone NOT NULL,
    auditorium text NOT NULL,
    projectiontype text NOT NULL,
    link text NOT NULL,
    status smallint NOT NULL,
    price smallint NOT NULL,
    CONSTRAINT "projections_pkey" PRIMARY KEY (id),
    CONSTRAINT "projection_ukey" UNIQUE (movieid, cinemaid, "time"),
    CONSTRAINT "cinemaid" FOREIGN KEY (cinemaid)
        REFERENCES cinemas (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "movieid" FOREIGN KEY (movieid)
        REFERENCES movies (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

INSERT INTO cinemas(name, link)	VALUES 
    ('Cineplexx', 'https://www.cineplexx.rs/'),
    ('CineGrand', 'http://nis.cinegrand-mcf.rs/'),
    ('Vilingrad', 'http://vilingrad.rs/') 
    ON CONFLICT (name) DO NOTHING;

SET timezone TO 'Europe/Belgrade';
