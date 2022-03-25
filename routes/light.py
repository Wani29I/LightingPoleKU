from fastapi import APIRouter, Depends, HTTPException

from config.db import poleDb, pmDb
from models.light import LightStatus, LightingPole
from bson import ObjectId
from models.user import User
from schemas.user import get_current_active_user

from schemas.utils import serializeDict, serializeList

light = APIRouter(prefix='/light')

@light.get('/')
async def find_all_pole():
    try:
        return serializeList(poleDb.find())
    except:
        raise HTTPException(status_code=400, detail="some error")

@light.get('/{poldId}')
async def find_one_pole(poldId):
    try:
        poleData = serializeDict(poleDb.find_one({"_id":ObjectId(poldId)}))
        poleData['pm'] = serializeDict(pmDb.find({"poleId":poldId}).limit(1).sort([('$natural',-1)])[0])
        return poleData
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@light.post('/')
async def create_pole(lightingPole: LightingPole):
    try:
        lightData = dict(lightingPole)
        _id = poleDb.insert_one(lightData).inserted_id
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
    try: 
        poleDb.update_one({"_id": ObjectId(id)},{ '$set' :dict(lightStatus)})
        return {
          'message': 'updated succesfully',
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")
    
@light.patch("/toggle/{id}")
async def toggle_light_by_admin(id,current_user: User = Depends(get_current_active_user)):
    try:
        if(current_user.permission == 0):
            raise HTTPException(status_code=403, detail="no permission")
        poleData = poleDb.find_one({"_id":ObjectId(id)})
        if not poleData:
            raise Exception('error')
        if poleData['status']:
            poleData['status'] = 0
        else:
            poleData['status'] = 1
        poleDb.update_one({"_id":ObjectId(id)},poleData)
    except:
        raise HTTPException(status_code=400, detail="could find pole")
