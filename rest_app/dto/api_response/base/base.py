from pydantic import BaseModel


class PaginationResponse(BaseModel):
    item_count: int
