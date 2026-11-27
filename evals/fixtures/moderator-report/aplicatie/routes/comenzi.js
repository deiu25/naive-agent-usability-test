// Ecranul Comenzi: lista si cautarea.
const express = require('express');
const db = require('../db');
const router = express.Router();

router.get('/comenzi', async (req, res) => {
    const cautare = (req.query.q || '').trim();
    let rezultat;
    if (cautare !== '') {
        // Cautare dupa numarul comenzii: un singur numar.
        rezultat = await db.query('SELECT * FROM comenzi WHERE numar = $1 ORDER BY numar', [cautare]);
    } else {
        rezultat = await db.query("SELECT * FROM comenzi WHERE stare <> 'livrata' ORDER BY data_livrare LIMIT 200");
    }
    res.render('comenzi', { comenzi: rezultat.rows, cautare });
});

router.post('/comenzi/:numar/rezerva', async (req, res) => {
    await db.query('UPDATE comenzi SET rezervat = 1, modificat_de = $1, modificat_la = now() WHERE numar = $2',
        [req.session.user, req.params.numar]);
    res.json({ ok: true });
});

module.exports = router;
