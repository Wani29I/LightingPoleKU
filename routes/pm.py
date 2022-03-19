from datetime import datetime
from fastapi import APIRouter, HTTPException

from config.db import pmDb
from models.pm import PmStatus
from schemas.user import serializeDict
from bson import ObjectId

pm = APIRouter(prefix='/pm')

@pm.get('/{id}')
async def find_light_status():
    try:
        return serializeDict(pmDb.find_one({"_id":ObjectId(id)}))
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@pm.post('/{id}')
async def create_light_status(pmStatus : PmStatus):
    try:
        pmData = dict(pmStatus)
        pmData['poleId'] = id 
        pmData['timestamp'] = datetime.timestamp(datetime.now())
        pmDb.insert_one(pmData)
        return {"message":"create successfully"}
    except:
        raise HTTPException(status_code=400, detail="wrong format")
