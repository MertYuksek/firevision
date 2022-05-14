# First create Virtual Environment for project.
# py -3 -m venv fire_vision_env
# Second install fast api.
# pip install fastapi[all]

from fastapi import Depends, FastAPI, WebSocket, File
from .serivices import analyze_data, notify, save_analysis
from .dependents import get_fire_message
from sqlalchemy.orm import Session
from .database import get_db, engine
from .schemas import PostInfo
from . import models


fire_message = get_fire_message()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/image")
async def send_image(data: PostInfo = Depends(PostInfo.as_form), file: bytes = File(...), db: Session = Depends(get_db)):
    analyze_result = analyze_data(data, file)
    notify(analyze_result)
    save_analysis(analyze_result, db)
    return analyze_result


@app.websocket("/warning")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await fire_message.fire_event.wait()
        await websocket.send_json(fire_message.message)
        fire_message.clear_event()

    


    

