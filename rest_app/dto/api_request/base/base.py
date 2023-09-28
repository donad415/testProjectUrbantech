from typing import Optional

from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    limit: Optional[int] = Field(1000, alias='list_amount')
    offset: Optional[int] = Field(0, alias='list_start')
