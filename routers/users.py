from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Path, Depends
from starlette import status
from models import Users
from .auth import get_current_user
from database import SessionLocal
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PasswordRequest(BaseModel):
    password: str
    new_password: str


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependecy, db: db_dependency):
    if user is None:
        HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependecy, db: db_dependency, password: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentitacion Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(password.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Failed to change password')
    user_model.hashed_password = bcrypt_context.hash(password.new_password)
    db.add(user_model)
    db.commit()