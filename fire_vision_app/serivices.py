from .dependents import get_fire_message, get_fire_model
from sqlalchemy.orm import Session
from fastapi import File, Depends
from .database import get_db
import PIL.Image as Image
from . import models
import io


fire_model = get_fire_model()
fire_message = get_fire_message()


def analyze_data(data, image):
    analyze_result = analyze_image(image)
    analyze_result["longitude"] = data.longitude
    analyze_result["latitude"] = data.latitude
    return analyze_result


def analyze_image(image: File):  
    analyze_result = {}
    image = Image.open(io.BytesIO(image)).convert("RGB")
    results = fire_model.model(image)
    
    for result in results:
       analyze_result[result[-1]] = \
           analyze_result.get(result[-1], 0) + 1
    
    return analyze_result


def notify(analyze_result):
    num_fire = analyze_result.get("fire", 0)
    if num_fire > 0:
        fire_message.set_event(analyze_result)
        

def save_analysis(analyze_result: dict, db: Session):
    if len(analyze_result) > 2:
        save_all_content_object(analyze_result, db)
     

def save_content(analyze_result, db: Session):
    
    is_fire = False
    if analyze_result.get("fire", 0) != 0:
        is_fire = True
        
    new_content = models.Contents(
        is_fire=is_fire, 
        lon=analyze_result["longitude"],
        lat=analyze_result["latitude"])
    
    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return new_content


def save_object(object_name, db: Session):
    new_object = models.Objects(name=object_name)
    db.add(new_object)
    db.commit()
    db.refresh(new_object)
    return new_object


def save_all_content_object(analyze_result, db: Session):
    
    content = save_content(analyze_result, db)

    for object_name in analyze_result:
        
        if object_name != "longitude" and object_name != "latitude":
            
            object = db.query(models.Objects).filter(models.Objects.name == object_name).first()
            if object == None:
                object = save_object(object_name, db)

            content_object = {"content_id": content.id, "object_id": object.id, "count": analyze_result[object_name]}
            save_content_object(content_object, db)

            
def save_content_object(content_object: dict, db: Session):
    new_content_object = models.Contents_Objects(**content_object)
    db.add(new_content_object)
    db.commit()
    db.refresh(new_content_object)
    return content_object

    


