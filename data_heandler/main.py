from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .logger.logger import logger

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


def get_current_user(db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    user = crud.get_current_user(db, token)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    scemas = crud.get_users(db, skip=skip, limit=limit)
    return scemas


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='User with this email already exist!')
    return crud.create_user(db=db, user=user)


@app.post('/login/', response_model=schemas.Token)
def login(data: schemas.LoginData, db: Session = Depends(get_db)):
    logger.info(f'{data.email} tried to log in.')
    user = crud.authenticate_user(db=db, email=data.email, password=data.password)
    if not user:
        logger.error('UNAUTHORIZED ACCESS.')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_token({'email': user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/services/", response_model=List[schemas.Services])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    scemas = crud.get_services(db, skip=skip, limit=limit)
    return scemas
