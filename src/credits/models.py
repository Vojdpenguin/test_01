from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, nullable=False)
    registration_date = Column(Date, nullable=False)

    credits = relationship("Credit", back_populates="user")


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issuance_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    body = Column(Float, nullable=False)
    percent = Column(Float, nullable=False)

    user = relationship("User", back_populates="credits")
    payments = relationship("Payment", back_populates="credit")


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    plans = relationship("Plan", back_populates="category")
    payments = relationship("Payment", back_populates="type")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(Date, nullable=False)
    sum = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)

    category = relationship("Dictionary", back_populates="plans")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sum = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    credit_id = Column(Integer, ForeignKey("credits.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("dictionary.id"), nullable=False)

    credit = relationship("Credit", back_populates="payments")
    type = relationship("Dictionary", back_populates="payments")
