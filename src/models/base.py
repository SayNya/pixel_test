from pydantic import BaseModel


class InternalModel(BaseModel):
    class Config:
        from_attributes = True
