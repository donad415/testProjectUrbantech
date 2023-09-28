from typing import List

from flasgger import Schema
from pydantic import BaseModel

from rest_app.dto.api_response.base.base import PaginationResponse


class ImageInfo(BaseModel):
    id: int
    time: str
    description: str


class GetImagesResponse(PaginationResponse, BaseModel):
    list: List[ImageInfo]
