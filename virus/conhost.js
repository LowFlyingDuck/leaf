const fs = require('fs');
const { exec } = require('child_process');
const http = require('http');
const crypto = require('crypto');
const user = crypto.randomBytes(8).toString('base64') + '---' + process.env.USER;

function output(err, stdout, stderr) {
  let r = http.request({
    host: 'localhost',
    method: 'POST'
  });
  err && r.write('ERROR: ' + err);
  stdout && r.write(stdout);
  stderr && r.write(stderr);
}
let child = exec('dir', {
  cwd: 'C:/'
}, output);

// setInterval(() => {
//   let r = new XMLHttpRequest();
//   r.open('GET', user);
// }, 3000)
console.log(user);