from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True, name="Email")
    password = Column(String(200), nullable=False, name="Password")
    user_type = Column(String(50), nullable=False, name="UserType")
    company_id = Column(Integer, ForeignKey('Company.Id'))
    should_update_password = Column(Boolean, nullable=False, name="ShouldUpdatePassword")

    def __init__(self, email, password, company_id=1, user_type="Regular", should_update_password=True):
        self.email = email
        self.password = password
        self.user_type = user_type
        self.company_id = company_id
        self.should_update_password = should_update_password

    def __repr__(self):
        return f'{{ email: {self.email}, \
password: {self.password}, type : {self.user_type} }}'

    def __getitem__(self, item=""):
        return {"email": self.email,
                "type": self.user_type,
                "id": self.id}


class PaymentTransaction(Base):
    __tablename__ = 'PaymentTransaction'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    payment_id = Column(String(50), nullable=False)
    amount = Column(String(50), nullable=False)
    dollar_amount = Column(String(50))

    def __init__(self, email, payment_id, amount, dollar_amount):
        self.email = email
        self.payment_id = payment_id
        self.amount = amount
        self.dollar_amount = dollar_amount


class Company(Base):
    __tablename__ = 'Company'

    id = Column(Integer, primary_key=True, name='Id')
    email = Column(String(50), nullable=False, name='Email', unique=True)
    name = Column(String(50), nullable=False, name='Name')
    password = Column(String(200), nullable=False, name="Password")
    country_id = Column(String(50), nullable=False, name='CountryId')
    date_joined = Column(DateTime, nullable=False, name='DateJoined')
    country = Column(String(50), nullable=False, name='Country')
    users = relationship("User")

    def __init__(self, email, name, password, country_id, country):
        self.email = email
        self.name = name
        self.password = password
        self.country_id = country_id
        self.country = country
        self.date_joined = datetime.now()

