from fastapi import FastAPI

from routes.pm import pm
from routes.light import light

app = FastAPI()
app.include_router(pm)
app.include_router(light)

@app.get("/")
async def check_app():
    return {"message": "API is running."}
