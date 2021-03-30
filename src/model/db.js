const dotenv = require('dotenv')
dotenv.config()

var mysql = require('mysql')

var pool = mysql.createPool({
    connectionLimit: 100,
    host: 'localhost',
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database:'nosql'
  })

module.exports = pool;