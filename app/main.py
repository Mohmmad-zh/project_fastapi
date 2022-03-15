from app.database import engine,SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails
from typing import List
import app.schemas as schemas
import app.routes.products as products, app.routes.users as users
import app.models as models
from passlib.context import CryptContext
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(products.router)
app.include_router(users.router)
db = SessionLocal()
auth_handler = AuthHandler()
users = []

@app.get('/products', response_model=List[schemas.Product], status_code=200, tags=["products"])
def get_all_product():
    return products.get_all()


@app.post('/protected/products', response_model=schemas.Product, tags=["products"])
def create_a_product(product: schemas.Product,username= Depends(auth_handler.auth_wrapper)):

    return products.create_product(product)


@app.get('/product/{product_id}', response_model=schemas.Product, tags=["products"])
def get_a_product(product_id: int):
    return products.get_an_product(product_id)


@app.put('/protected/product/{product_id}', response_model=schemas.Product, tags=["products"])
def update_a_product(product_id: int, product: schemas.Product,username= Depends(auth_handler.auth_wrapper)):
    return products.update()


@app.delete('/protected/product/{product_id}', tags=["products"])
def delete_product(product_id: int,username= Depends(auth_handler.auth_wrapper)):
    return products.delete_product()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@app.post('/register', status_code=201, tags=["auth"])
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return "user registered successfully"


@app.post('/login', tags=["auth"])
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }



# @app.get('/protected')
# def protected(username=Depends(auth_handler.auth_wrapper)):
#     return { 'name': username }

