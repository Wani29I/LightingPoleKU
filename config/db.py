from pymongo import MongoClient
from decouple import config

client = MongoClient(config('MONGO_URL'))

userDb = client.LightingPole.User
lightDb = client.LightingPole.LightStatus
pmDb = client.LightingPole.PmStatus
