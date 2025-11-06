from typing import List
from uuid import uuid4
from .models import Product, ProductCategory

# In memory
db: List[Product] = [
    Product(
        id=1,
        name="Smartphone Model X",
        description="Um celular de última geração.",
        price=10000.99,
        category=ProductCategory.electronics,
        in_stock=True,
    ),
    Product(
        id=2,
        name="Diário de um Banana",
        description="Vários livros divertidos.",
        price=30.50,
        category=ProductCategory.books,
        in_stock=True,
    ),
    Product(
        id=3,
        name="Camiseta Azul",
        description="Camiseta básica de algodão.",
        price=25.00,
        category=ProductCategory.clothing,
        in_stock=False,
    ),
    Product(
        id=4,
        name="Engenharia de Software",
        description="Livro falando sobre diagramas.",
        price=45.00,
        category=ProductCategory.books,
        in_stock=True,
    ),
]
