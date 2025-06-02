from typing import Optional

from pydantic import BaseModel, EmailStr


class ReaderSchema(BaseModel):
    name: str
    email: EmailStr
    model_config = {
        "from_attributes": True
    }

class ReaderUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None