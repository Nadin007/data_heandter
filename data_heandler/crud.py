import datetime
from datetime import timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas
from .config import Config
from .logger.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = Config.SECRET_KEY


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        logger.info(f'User was not found with email - {email}')
        return False
    if not verify_password(password, user.hashed_password):
        logger.info('Can not verify password.')
        return False
    return user


def get_current_user(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        email = payload.get('email')
        token_data = schemas.TokenData(email=email)
        return get_user_by_email(db, token_data.email)
    except Exception:
        return None


def create_token(data: dict, expires_delta: Union[timedelta, None] = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": (datetime.datetime.utcnow() + expires_delta).timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password,
        name=user.name, last_name=user.last_name, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_company(db: Session, company_id: int):
    return db.query(models.Companies).filter(models.Companies.id == company_id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Companies).offset(skip).limit(limit).all()


def create_company(db: Session, company: schemas.CreateCompanies):
    db_company = models.Companies(name=company.name, description=company.description)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_service(db: Session, service_id: int):
    return db.query(models.Services).filter(models.Services.id == service_id).first()


def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Services).offset(skip).limit(limit).all()


def create_service(db: Session, service: schemas.CreateServices):
    db_service = models.Services(name=service.name)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_service_companies(db: Session, service_id: int):
    return db.query(models.ServiceCompany).filter(models.ServiceCompany.service_id == service_id).join(models.ServiceCompany.company).all()


def create_service_company(db: Session, service_company: schemas.CreateServiceCompany):
    db_service_company = models.ServiceCompany(
        company_id=service_company.company_id, cost=service_company.cost, service_id=service_company.service_id)
    db.add(db_service_company)
    db.commit()
    db.refresh(db_service_company)
    return db_service_company

# def create_user_item(db: Session, item: schemas.CreateCompanies):
#     db_item = models.Companies(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
