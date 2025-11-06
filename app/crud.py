from typing import List, Optional
from .models import ProductCategory, Product, UpdateProduct
from .db import db

# Helper p/ gerar ID incremental
def _next_id() -> int:
    if not db:
        return 1
    return max(p.id for p in db if p.id is not None) + 1

# --- READ ---

def get_all_products() -> List[Product]:
    return db

def get_product_by_id(product_id: int) -> Optional[Product]:
    for product in db:
        if product.id == product_id:
            return product
    return None

# --- CREATE ---

def create_product(product: Product) -> Product:
    if product.id is None:
        product.id = _next_id()
    db.append(product)
    return product

# --- UPDATE ---

def update_product(product_id: int, product_update: UpdateProduct) -> Optional[Product]:
    for product in db:
        if product.id == product_id:
            update_data = product_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)
            return product
    return None

# --- DELETE ---

def delete_product(product_id: int) -> bool:
    for product in db:
        if product.id == product_id:
            db.remove(product)
            return True
    return False

# --- SEARCH ---

def search_products(
    category: Optional[ProductCategory] = None,
    in_stock: Optional[bool] = None,
    min_price: Optional[float] = None,
) -> List[Product]:
    
    filtered = db

    if category is not None:
        filtered = [p for p in filtered if p.category == category]

    if in_stock is not None:
        filtered = [p for p in filtered if p.in_stock == in_stock]

    if min_price is not None:
        filtered = [p for p in filtered if p.price >= min_price]

    return filtered
