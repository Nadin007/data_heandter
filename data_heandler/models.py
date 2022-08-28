from enum import Enum

from sqlalchemy import (Boolean, CheckConstraint, Column, Float, ForeignKey,
                        Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship

from .database import Base


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    nonbinary = 'non binary'


class UserRole:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


ROLE_CHOICES = (
    (UserRole.USER, "user"),
    (UserRole.MODERATOR, "moderator"),
    (UserRole.ADMIN, "admin"),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False, default=UserRole.USER)
    gender = Column(String, nullable=False, default=Gender.nonbinary)

    __table_args__ = (
        CheckConstraint('name = me', name='User can be called \'me\'!'), )

    def __repr__(self) -> str:
        return 'UserModel(name=%s, last_name=%s,role=%s,email=%s)' % (self.name, self.last_name, self.role, self.email)


class Companies(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    description = Column(String(60), index=True)
    url = Column(String(200))

    service = relationship("ServiceCompany", back_populates="company")

    __table_args__ = (UniqueConstraint('name'), )

    def __repr__(self) -> str:
        return 'CompaniesModel(name=%s, description=%s,service=%s)' % (self.name, self.description, self.service)


class Services(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String(200), index=True)
    url = Column(String(200))

    company = relationship("ServiceCompany", back_populates="service")

    def __repr__(self) -> str:
        return 'ServicesModel(name=%s, cost=%s,id=%s)' % (self.name, self.cost, self.id)


class ServiceCompany(Base):
    __tablename__ = "service_company"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    cost = Column(Float, default=None)

    company = relationship("Companies", back_populates="service")
    service = relationship("Services", back_populates="company")

    def __repr__(self) -> str:
        return 'ServiceCompanyModel(company_id=%s, service_id=%s,id=%s)' % (self.company_id, self.service_id, self.id)
