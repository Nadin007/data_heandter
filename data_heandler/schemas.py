from enum import Enum
from typing import List, Union

from pydantic import BaseModel, EmailStr, root_validator, validator


def normalize(name: str) -> str:
    return ' '.join(word.capitalize() for word in name.strip().split())


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    nonbinary = 'non binary'


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[EmailStr, None] = None


class LoginData(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    '''
    Model that have common attributes while creating or reading data.
    '''

    email: EmailStr
    name: str
    last_name: str

    _normalize_name = validator('name', allow_reuse=True)(normalize)
    _normalize_last_name = validator('last_name', allow_reuse=True)(normalize)


class UserCreate(UserBase):
    '''
    Inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
    '''

    password: str


class User(UserBase):
    ''''
    Model that will be used when reading a user (returning it from the API)
    '''

    id: int
    gender: Gender = Gender.nonbinary
    is_active: bool
    role: UserRole = UserRole.USER

    class Config:
        orm_mode = True


class ServiceCompanyBase(BaseModel):
    '''
    Model that have common attributes while creating or reading data.
    '''

    company_id: int
    service_id: int
    cost: Union[int, None] = None


class CreateServiceCompany(ServiceCompanyBase):
    '''
    Inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
    '''
    pass


class ServiceCompany(ServiceCompanyBase):
    ''''
    Model that will be used when reading a user (returning it from the API)
    '''

    id: int

    class Config:
        orm_mode = True


class ServicesBase(BaseModel):
    '''
    Model that have common attributes while creating or reading data.
    '''

    name: str


class CreateServices(ServicesBase):
    '''
    Inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
    '''

    pass


class Services(ServicesBase):
    ''''
    Model that will be used when reading a user (returning it from the API)
    '''

    id: int
    company: List[ServiceCompany] = []
    description: Union[str, None] = None
    url: Union[str, None] = None

    class Config:
        orm_mode = True


class CompaniesBase(BaseModel):
    '''
    Model that have common attributes while creating or reading data.
    '''

    name: str
    description: Union[str, None] = None
    url: Union[str, None] = None


class CreateCompanies(CompaniesBase):
    '''
    Inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.
    '''

    pass


class Companies(CompaniesBase):
    ''''
    Model that will be used when reading a user (returning it from the API)
    '''

    id: int
    service: List[ServiceCompany] = []

    class Config:
        orm_mode = True
