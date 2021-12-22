const express = require('express')
const pg = require('pg');
const fs = require('fs');
const yaml = require('js-yaml');
const app = express();
const port = 3000;
const file_config = fs.readFileSync('../config.yaml', 'utf8');
const config = yaml.load(file_config);
const config_db = {
  user: config.database.user_db,
  database: config.database.db_name,
  password: config.database.password_db,
  port: config.database.port,
  host: config.database.host
}

const sql = "select C.name,N.title,N.body,N.htmlbody,N.creation_date FROM newsmail AS N JOIN appuser AS S ON S.id = N.sender JOIN SENTON AS SO ON SO.newsmail = N.msgid JOIN channel AS C ON C.code = SO.channel JOIN cansendon AS CSO ON CSO.appuser = N.sender AND SO.channel = CSO.channel WHERE C.name = $1 AND SO.enable = TRUE AND C.is_active = TRUE AND N.expiration_date > '2021-12-21' ";

const client = new pg.Client(config_db);

client.connect(err => {
    if (err) throw err;
});

client.query("SET search_path TO 'newsmail';");


function queryChannel(channel,callback) {

    console.log(`Running query to PostgreSQL server: ${config_db.host}`);
    values = [channel];
    client.query(sql,values)
        .then(res => {
            const rows = res.rows;
            return callback(rows);
        })
        .catch(err => {
            console.log(err);
        });
}

app.get('/',function (req, res){
  //res.send(config.database);
  res.setHeader('Content-Type', 'application/json');
  queryDatabase(function(rows){
    res.send(JSON.stringify(rows));
  })
})

app.get('/:channel',(req,res) => {
  res.setHeader('Content-Type', 'application/json');
  queryChannel(req.params.channel,function(rows){
    res.send(JSON.stringify(rows));
  })
})



app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
