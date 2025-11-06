from typing import Optional
from pydantic import BaseModel
from enum import Enum

class ProductCategory(str, Enum):
    electronics = "eletrônicos"
    books = "livros"
    clothing = "roupas"

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    category: ProductCategory
    in_stock: bool = True

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[ProductCategory] = None
    in_stock: Optional[bool] = None
