const cors = require("cors")

const express = require('express');
const app = express();

app.use(cors());

const database = require('pg');

const client = new database.Client({
    host: "localhost",
    user: "",
    port: 5432,
    password: "",
    database: ""
});

client.connect();

app.get('/', async (_, res) => {
    // const version = await client.query("SELECT version()");
  const items = await client.query(`SELECT distinct movies.id, movies.title, movies.originaltitle, movies.genre,
    ( SELECT ARRAY_AGG(projections.time)
      FROM projections 
      WHERE projections.movieid = movies.id 
      AND projections.time > NOW()
    ) AS projectiontimes FROM movies inner join projections on movies.id = projections.movieid where projections.time > NOW()`)
    res.json(items.rows);
});

app.get('/movie/:id', async (req, res) => {
    req.params.id = Number.parseInt(req.params.id);
    if(isNaN(req.params.id)) {
        res.status(400).send("Bad request.");
        return;
    }
    console.log(req.params.id);
    const items = await client.query(`select id, title, originaltitle, runningtime, synopsis, genre, countryoforigin, director, "cast", trailerlink from movies where id = ${req.params.id}`);
    res.json(items.rows);
});

app.get('/projection/:id', async (req, res) => {
    req.params.id = Number.parseInt(req.params.id);
    if(isNaN(req.params.id)) {
        res.status(400).send("Bad request.");
        return;
    }
    console.log(req.params.id);
    const items = await client.query(`SELECT cinemas.name, projections.time, projections.auditorium, projections.projectiontype, projections.price, projections.link FROM projections INNER JOIN cinemas ON projections.cinemaid = cinemas.id WHERE projections.movieid = ${req.params.id} AND projections.time > NOW() ORDER BY projections.time ASC`);
    res.json(items.rows);
});

app.listen(3000);
