HEADER='Content-Type: application/json'
DATA='[{"name":"National Basketball Association", "abbreviation":"NBA", "sport":"basketball"}]'
URI='http://127.0.0.1:5000/leagues/'

# test delete
curl -X DELETE $URI

# test post
curl -H "$HEADER" -d "$DATA" $URI

# test get
curl -G $URI
