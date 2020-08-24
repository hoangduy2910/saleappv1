from saleapp import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    use_role = Column(Enum(UserRole), default=UserRole.USER)
    products = relationship('Product', backref='user', lazy=True)


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    image = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    create_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    creator = Column(Integer, ForeignKey(User.id), nullable=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(DateTime, default=datetime.now())
    update_date = Column(DateTime, default=datetime.now())


class ReceiptDetail(db.Model):
    product_id = Column(Integer, ForeignKey(Product.id), primary_key=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == "__main__":
    db.create_all()