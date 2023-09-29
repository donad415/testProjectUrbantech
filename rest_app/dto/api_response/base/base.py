from typing import Optional

from pydantic import BaseModel


class PaginationResponse(BaseModel):
    item_count: int


class BaseResponse(BaseModel):
    success: bool
    error: Optional[str] = None
