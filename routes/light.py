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
async def find_one_light_status(id):
    try:
        return serializeDict(lightDb.find_one({"_id":ObjectId(id)}))
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@light.post('/{id}')
async def create_light_status(id,lightStatus : LightStatus):
    try:
        print(lightStatus)
        lightData = dict(lightStatus)
        lightData['poleId'] = id
        _id = lightDb.insert_one(lightData).inserted_id
        lightData['_id'] = str(_id)
        return {
          'message': 'created succesfully',
          'data': lightData
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")

@light.patch('/{id}')
async def update_light_status(id,lightStatus : LightStatus):
    try: 
        lightDb.update_one({"poleId":id},lightStatus)
        return {
          'message': 'updated succesfully',
        }
    except:
        raise HTTPException(status_code=400, detail="wrong format")
    