from pydantic import BaseModel, validator, Field, EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    @validator('confirm_password')
    def password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    model_config = {
        "from_attributes": True
    }