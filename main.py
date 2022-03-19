from fastapi import FastAPI

from routes.pm import pm
from routes.light import light

app = FastAPI(
    title="LigthingPoleApp"
)
app.include_router(pm,tags=['pm'])
app.include_router(light,tags=['light'])

@app.get("/",tags=['check'])
async def check_app():
    return {"message": "API is running."}
