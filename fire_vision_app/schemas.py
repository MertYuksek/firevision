import imp
from pydantic import BaseModel
from fastapi import Form


# https://stackoverflow.com/questions/69292855/why-do-i-get-an-unprocessable-entity-error-while-uploading-an-image-with-fasta
class PostInfo(BaseModel):
    longitude: float
    latitude: float
    
    @classmethod
    def as_form(cls, longitude: float = Form(...), latitude: float = Form(...)) -> 'ItemForm':
        return cls(longitude=longitude, latitude=latitude)

