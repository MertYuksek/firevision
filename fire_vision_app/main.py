# First create Virtual Environment for project.
# py -3 -m venv fire_vision_env
# Second install fast api.
# pip install fastapi[all]

import asyncio
import time
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect, WebSocketDisconnect, File
from .serivices import analyze_data, send_message_to_mobile, save_analysis
from .dependents import get_manager
from sqlalchemy.orm import Session
from .database import get_db, engine
from .schemas import PostInfo
from . import models
from fastapi.middleware.cors import CORSMiddleware
import threading


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/image")
async def send_image(data: PostInfo = Depends(PostInfo.as_form), file: bytes = File(...), db: Session = Depends(get_db)):
    analyze_result = analyze_data(data, file)
    save_analysis(analyze_result, db)
    _thread = threading.Thread(target=send_message_to_mobile, args=(analyze_result, ))
    _thread.start()
    return analyze_result


manager = get_manager()
@app.websocket("/ws/warning/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)




    

