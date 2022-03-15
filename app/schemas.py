from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:  # serialize our sql obj to json
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    products: List[Product] = []

    class Config:  # serialize our sql obj to json
        orm_mode = True


class ShowProduct(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # required
    price: float  # int
    tax: Optional[float] = None
    owner: ShowUser

    class Config:  # serialize our sql obj to json
        orm_mode = True


class AuthDetails(BaseModel):
    username: str
    password: str