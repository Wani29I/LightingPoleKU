from fastapi import APIRouter, HTTPException

from config.db import lightDb
from models.light import LightStatus
from schemas.user import serializeDict, serializeList
from bson import ObjectId

light = APIRouter(prefix='/light')

@light.get('/')
async def find_all_light_status():
    try:
        return serializeList(lightDb.find_one())
    except:
        raise HTTPException(status_code=400, detail="some error")

@light.get('/{id}')
async def find_one_light_status():
    try:
        return serializeDict(lightDb.find_one({"_id":ObjectId(id)}))
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@light.post('/{id}')
async def create_light_status(lightStatus : LightStatus):
    try:
        lightData = dict(lightStatus)
        lightData.update({'poleId': id}) 
        return lightDb.insert_one(lightData)
    except:
        raise HTTPException(status_code=400, detail="wrong format")

@light.patch('/{id}')
async def update_light_status(lightStatus : LightStatus):
    try: 
        return lightDb.update_one({"poleId":id},lightStatus)
    except:
        raise HTTPException(status_code=400, detail="wrong format")
    