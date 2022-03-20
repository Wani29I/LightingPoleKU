from fastapi import APIRouter, Depends, HTTPException

from config.db import lightDb
from models.light import LightStatus
from bson import ObjectId
from models.user import User
from schemas.user import get_current_active_user

from schemas.utils import serializeDict, serializeList

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
        lightData = {
            **dict(lightStatus),
            'poleId': id,
        }
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
    
@light.post("/toggle/{id}")
async def read_users_data(id,current_user: User = Depends(get_current_active_user)):
    try:
        poleData = lightDb.find_one({"poleId":id})
        if not poleData:
            raise Exception('error')
        if poleData['status']:
            poleData['status'] = 0
        else:
            poleData['status'] = 1
        lightDb.update_one({"poleId":id},poleData)
    except:
        raise HTTPException(status_code=400, detail="could find pole")
