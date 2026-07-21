from pydantic import BaseModel

class DocumentModel(BaseModel):
    rawtext: str