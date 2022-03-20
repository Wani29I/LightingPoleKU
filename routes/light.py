from fastapi import APIRouter, Depends, HTTPException

from config.db import lightDb
from models.light import LightStatus
from bson import ObjectId
from models.user import User
from schemas.user import get_current_active_user

from schemas.utils import serializeDict, serializeList

light = APIRouter(prefix='/light')

async def update_light(id: str,lightStatus: LightStatus):
    try: 
        lightDb.update_one({"poleId":id},{ '$set' :dict(lightStatus)})
        return {
          'message': 'updated succesfully',
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")

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
        oldLight = lightDb.find_one({'poleId': id})
        if(oldLight):
            return update_light(id,lightStatus)
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
async def update_light_status(id: str,lightStatus : LightStatus):
    return update_light(id,lightStatus)
    
@light.post("/toggle/{id}")
async def toggle_light_by_admin(id,current_user: User = Depends(get_current_active_user)):
    try:
        if(current_user.permission == 0):
            raise HTTPException(status_code=403, detail="no permission")
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
