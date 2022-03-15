from app.database import SessionLocal
from fastapi import APIRouter, FastAPI, status, HTTPException, Response
from typing import Optional, List
from pydantic import BaseModel
import app.models as models
import app.schemas as schemas
import app.main as main
from passlib.context import CryptContext


router = APIRouter(tags=["users"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/user', response_model=schemas.ShowUser)
def create_user(user: schemas.User):
    hashed_pass = pwd_context.hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pass,
    )

    main.db.add(new_user)
    main.db.commit()
    main.db.refresh(new_user)
    return new_user


@router.get('/users/{user_id}', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_a_user(user_id: int, response: Response):
    user = main.db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} is not Available")
    return user
