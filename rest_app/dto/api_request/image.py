from pydantic import BaseModel, Field


class UploadImageRequest(BaseModel):
    description: str = Field(None, max_length=200, description='Описание изображения')
