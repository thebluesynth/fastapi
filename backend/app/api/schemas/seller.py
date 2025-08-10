from pydantic import BaseModel, EmailStr, Field


class BaseSeller(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class SellerRead(BaseSeller):
    pass

class SellerCreate(BaseSeller):
    password: str
    