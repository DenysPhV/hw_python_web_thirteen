from datetime import date

from sqlalchemy import ForeignKey, String, Integer, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[int] = mapped_column(String, index=True)
    birthday: Mapped[date] = mapped_column(DateTime)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)
    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user: Mapped[str] = relationship('User', backref='contacts')


class Note(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey('contacts.id'), nullable=False)
    text: Mapped[str] = mapped_column(String)
    contact: Mapped[str] = relationship("Contact", backref='notes')
    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user: Mapped[str] = relationship('User', backref='notes')


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
