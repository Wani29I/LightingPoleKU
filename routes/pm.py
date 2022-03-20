from datetime import datetime
from fastapi import APIRouter, HTTPException

from config.db import pmDb
from models.pm import PmStatus
from bson import ObjectId
from schemas.utils import serializeDict, serializeList

pm = APIRouter(prefix='/pm')

@pm.get('/{id}')
async def find_pm_status(id):
    try:
        return serializeList(pmDb.find({"poleId":ObjectId(id)}))
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@pm.post('/{id}')
async def create_pm_status(id, pmStatus : PmStatus):
    try:
        pmData = {
            **dict(pmStatus),
            'poleId': id,
            'timestamp': datetime.timestamp(datetime.now())
        }
        _id = pmDb.insert_one(pmData).inserted_id
        pmData['_id'] = str(_id)
        return {
        'message': 'created succesfully',
          'data': pmData
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")
