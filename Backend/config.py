# config information
# 
import couchdb

USERNAME = 'admin'
PASSWORD = 'admin'
HOSTIP = '172.26.134.133'
PORT = '5984'

DB_URI = "http://{}:{}@{}:{}".format(USERNAME, PASSWORD, HOSTIP, PORT)

remote_server = couchdb.Server(DB_URI)

SWAGGER_TITLE = "CCC_API"
SWAGGER_DESC = "backend api for ccc project2, called by frontend to collect data"
SWAGGER_HOST = "localhost:6666"