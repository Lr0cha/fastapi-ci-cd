from fastapi import FastAPI
from app.routers import products

tags_metadata = [
    {
        "name": "Products",
        "description": "Operações para gerenciamento de produtos — criação, listagem, atualização e remoção.",
    }
]

app = FastAPI(
    title="Product Management API",
    description="API exemplo para gerenciamento de produtos.",
    version="1.0",
    openapi_tags=tags_metadata,
)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Gerenciamento de Produtos!"}

app.include_router(products.router)
