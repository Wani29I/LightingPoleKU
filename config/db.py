from pymongo import MongoClient
from decouple import config

client = MongoClient(config('MONGO_URL'))

userDb = client.EventKU.User
eventDb = client.EventKU.Event
