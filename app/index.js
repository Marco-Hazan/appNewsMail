const express = require('express')
const pg = require('pg');
const fs = require('fs');
const fsPromises = fs.promises;
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

const sql = "select S.username AS publisher,N.msgid,N.title,N.body,N.htmlbody,N.creation_date FROM newsmail AS N JOIN appuser AS S ON S.id = N.sender JOIN SENTON AS SO ON SO.newsmail = N.msgid JOIN channel AS C ON C.code = SO.channel WHERE C.name = $1 AND SO.enable = TRUE AND C.is_active = TRUE AND N.expiration_date > $2 ";

const client = new pg.Client(config_db);

client.connect(err => {
    if (err) throw err;
});

client.query("SET search_path TO 'newsmail';");

async function listDir(path) {
  try {
    let names = await fsPromises.readdir(path);
    return names;
  } catch (err) {
    console.error('Error occured while reading directory!', err);
  }
}

function queryChannel(channel,callback) {
    let date_ob = new Date();
    let year = date_ob.getFullYear();
    let month = ("0" + (date_ob.getMonth() + 1)).slice(-2);
    let days = ("0" + date_ob.getDate()).slice(-2);
    let date = year + "-" + month + "-" + days;
    console.log(`Running query to PostgreSQL server: ${config_db.host}`);
    values = [channel,date];
    client.query(sql,values)
        .then(res => {
            if(res.rowCount == 0){
              return callback({status: 'Disabled or not exists'});
            }
            oggetto_channel = {
              status: "published",
              totalResults: res.rowCount,
              channel: channel,
              url: "localhost:3000/"+ channel
            }
            var rows = res.rows;
            oggetto_channel.articles = rows;
            return callback(oggetto_channel);
        })
        .catch(err => {
            console.log(err);
        });
}

app.get('/',function (req, res){
  //res.send(config.database);
  res.setHeader('Content-Type', 'application/json');
  queryDatabase(function(obj){
    res.send(JSON.stringify(obj));
  })
})

app.get('/:channel',(req,res) => {
  res.setHeader('Content-Type', 'application/json');
  queryChannel(req.params.channel,async function(obj){
      for(i=0;i<obj.articles.length;i++){
        obj.articles[i].attachments = [];
        names = await listDir(config.attachments_path+"/"+obj.articles[i].msgid);
        if(names != undefined){
          for(const file of names){
            obj.articles[i].attachments.push(config.attachments_path+"/"+obj.articles[i].msgid+"/"+file);
          }
        }
      }
      res.send(JSON.stringify(obj));
  })
})



app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
