import pymongo, os

config = {
    "username": "jump2digital",
    "password": "17112023",
    "host": "mongo",
    "port": "27017"
}

connector = "mongodb://{username}:{password}@{host}:{port}/?authSource=admin".format(**config)
client = pymongo.MongoClient(connector)

db = client["J2D"]

skins = db['skins']
users = db['users']