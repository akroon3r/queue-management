var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"localhost"',
  API_URL: '"http://192.168.0.20:5000/api/v1"',
  SOCKET_URL: '"http://192.168.0.20:5000"',
  KEYCLOAK_JSON_URL: '"http://192.168.0.20:8080/static/keycloak.json"',
  REFRESH_TOKEN_SECONDS_LEFT: 180
})
