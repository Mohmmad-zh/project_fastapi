from app.database import SessionLocal
from fastapi import FastAPI, status, HTTPException, Response, APIRouter
from typing import Optional, List
from pydantic import BaseModel
import app.models as models
import app.schemas as schemas
import app.main as main
router = APIRouter(tags=["product"])


@router.get('/products', response_model=List[schemas.Product], status_code=200, tags=["products"])
def get_all_product():
    products = main.db.query(models.Product).all()
    return products


@router.post('/protected/products', response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_a_product(product: schemas.Product):
    db_product = main.db.query(models.Product).filter(
        models.Product.name == product.name).first()
    if db_product is not None:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = models.Product(
        name=product.name,
        price=product.price,
        description=product.description,
        tax=product.tax,
        owner_id=1)

    main.db.add(new_product)
    main.db.commit()
    return new_product


@router.get('/product/{product_id}', response_model=schemas.Product, status_code=status.HTTP_200_OK)
def get_a_product(product_id: int, response: Response):
    product = main.db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {product_id} is not Available")
    return product


@router.put('/protected/product/{product_id}', response_model=schemas.Product, status_code=status.HTTP_200_OK)
def update_a_product(product_id: int, product: schemas.Product):
    product_to_update = main.db.query(models.Product).filter(
        models.Product.id == product_id).first()
    product_to_update.name = product.name
    product_to_update.price = product.price
    product_to_update.description = product.description
    product_to_update.tax = product.tax

    main.db.commit()
    return product_to_update


@router.delete('/protected/product/{product_id}')
def delete_product(product_id: int):
    product_to_delete = main.db.query(models.Product).filter(
        models.Product.id == product_id).first()

    if product_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    main.db.delete(product_to_delete)
    main.db.commit()

    return product_to_delete
