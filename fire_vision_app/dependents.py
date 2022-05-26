import time
from typing import List
from fastapi import WebSocket
import torch


class Fire_Vision():

    def __init__(self):
        self.fire_model = self.__get_fire_model()
        self.yolo_model = self.__get_yolo_model()

    def __get_fire_model(self, path="fire_vision_app\\best.pt"):
        fire_model = torch.hub.load('ultralytics/yolov5', 'custom', path=path, force_reload=True)
        return fire_model

    def __get_yolo_model(self, path="fire_vision_app\\yolov5s.pt"):
        yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path=path, force_reload=True)
        return yolo_model
       
    def model(self, image: bytes):
        results = \
            self.fire_model(image).pandas().xyxy[0].values.tolist() + \
            self.yolo_model(image).pandas().xyxy[0].values.tolist()
        return results


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


fire_model = Fire_Vision()
manager = ConnectionManager()


def get_fire_model():
    return fire_model


def get_manager():
    return manager