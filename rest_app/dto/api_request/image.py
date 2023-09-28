from pydantic import BaseModel, Field

from rest_app.dto.api_request.base.base import PaginationRequest


class UploadImageRequest(BaseModel):
    description: str = Field(None, max_length=200)


class GetImagesRequest(PaginationRequest, BaseModel):
    pass
