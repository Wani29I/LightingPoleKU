from pymongo import MongoClient
client = MongoClient('mongodb+srv://Wani29:Ice.31458@cluster0.wydzb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

userDb = client.EventKU.User
eventDb = client.EventKU.Event


