from fastapi import APIRouter, Depends
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
form_data_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def authentica_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post('/token')
async def login_for_access_token(form_data: form_data_dependency, db: db_dependency):
    user = authentica_user(form_data.username, form_data.password, db)

    if not user:
        return 'Failed Authenticated'
    return 'Successful Authenticated'
