import asyncio
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


class Fire_Message():

    def __init__(self) -> None:
        self.fire_event = asyncio.Event()
        self.message = None


    def set_event(self, message):
        self.fire_event.set()
        self.message = message


    def clear_event(self):
        self.fire_event.clear()
        self.message = None


fire_model = Fire_Vision()
fire_message = Fire_Message()


def get_fire_model():
    return fire_model

def get_fire_message():
    return fire_message