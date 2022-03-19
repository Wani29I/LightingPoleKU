from fastapi import APIRouter, HTTPException

from models.user import User
from config.db import userDb, eventDb
from schemas.user import serializeDict, serializeList
from bson import ObjectId

user = APIRouter(prefix='/user')

@user.get('/')
async def find_all_users():
    return serializeList(userDb.find())

@user.get('/{id}')
async def find_one_users(id):
    try:
        return serializeDict(userDb.find_one({"_id":ObjectId(id)}))
    except:
        raise HTTPException(status_code=400, detail="object with the provided id could not be found")

@user.post('/')
async def creat_user(user: User):
    try:
        userDb.insert_one(dict(user))
        return {"message":"success"}
    except:
        return HTTPException(status_code=400, detail="some problem occured")

@user.put('/{id}')
async def update_user(id,user: User):
    try:
        userDb.find_one_and_update(
            {"_id":ObjectId(id)},
            {"$set":dict(user)})
        return {"message":"success"}
    except:
        return HTTPException(status_code=400, detail="some problem occured")

@user.delete('/{id}')
async def delete_user(id):
    try:
        userDb.find_one_and_delete({"_id":ObjectId(id)})
        return {"message":"success"}
    except:
        return HTTPException(status_code=400, detail="invalid input")
