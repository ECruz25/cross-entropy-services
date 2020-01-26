from app.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {{ username: {self.username}, \
password: {self.password} }}'

class PaymentTransaction(Base):
    __tablename__ = 'PaymentTransaction'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    payment_id = Column(String(50), nullable=False)
    amount = Column(String(50), nullable=False)
    dollar_amount = Column(String(50))

    def __init__(self, username, payment_id, amount, dollar_amount):
        self.username = username
        self.payment_id = payment_id
        self.amount = amount
        self.dollar_amount = dollar_amount