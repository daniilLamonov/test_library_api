from email.policy import default

from pydantic import BaseModel, Field
from typing import Optional


class BookAddSchema(BaseModel):
    title: str
    author: str
    year_of_publish: Optional[str] = Field(default=None)
    isbn: Optional[str] = Field(default=None)
    count: int = Field(default=1, ge=1)
    model_config = {
        "from_attributes": True
    }

class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year_of_publish: Optional[str] = None
    isbn: Optional[str] = None
    count: Optional[int] = Field(default= None, ge=1)