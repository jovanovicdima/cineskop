const cors = require("cors")

const express = require('express');
const app = express();

app.use(cors())

const database = require('pg');

const client = new database.Client({
    host: "localhost",
    user: "dima",
    port: 5432,
    password: "dima",
    database: "dima"
});

client.connect();

app.get('/', async (req, res) => {
    // const version = await client.query("SELECT version()");
    const items = await client.query("SELECT * FROM movies")
    res.json(items.rows);
});

app.get('/:id', (req, res) => {
    console.log(req.params.id);
});



app.listen(3000);