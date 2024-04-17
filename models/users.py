from db import db
from sqlalchemy import Column, Integer, String

class UserModel(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    favorite_quote = Column(String(500), nullable=False)

    