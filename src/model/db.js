var mysql = require('mysql')
var pool = mysql.createPool({
    connectionLimit: 100,
    host: 'localhost',
    user:'root',
    password:'password',
    database:'nosql'
  })

module.exports = pool;