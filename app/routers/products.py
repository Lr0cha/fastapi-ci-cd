from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models import Product, ProductCategory, UpdateProduct
from app import crud

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)

@router.get("/", response_model=List[Product])
async def get_all_products():
    return crud.get_all_products()

@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id:int):
    product = crud.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
                status_code=404,
                detail=f"Não foi possível encontrar o produto com ID: {product_id}"
            )
    return product


@router.post("/", response_model=Product, status_code=201)
async def create_product(product: Product):
    return crud.create_product(product)

@router.put("/{product_id}", response_model=int)
async def update_product(product_id: int, product_update: UpdateProduct):
    updated_product = crud.update_product(product_id, product_update)

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Não foi possível encontrar o produto com ID: {product_id}"
        )
    
    return updated_product.id

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int):
    if not crud.delete_product(product_id):
        raise HTTPException(
            status_code=404,
            detail=f"Falha ao deletar produto, ID {product_id} não encontrado."
        )

@router.get("/search", response_model=List[Product])
async def search_products(
    category: Optional[ProductCategory] = Query(None),
    in_stock: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None),
):
    return crud.search_products(category=category, in_stock=in_stock, min_price=min_price)
