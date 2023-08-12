from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime

from src.schemas import ContactModel
from src.database.models import Contact, User


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_all(user: User, db: Session):
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def get_one(contact_id, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, id=contact_id)).first()
    return contact


async def update(contact_id, body: ContactModel, user: User, db: Session):
    contact = await get_one(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete(contact_id, user: User, db: Session):
    contact = await get_one(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def find_by_name(contact_name, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, first_name=contact_name)).first()
    return contact


async def find_by_lastname(lastname, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, last_name=lastname)).first()
    return contact


async def find_by_email(email, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, email=email)).first()
    return contact


async def find_birthday7day(user: User, db: Session):
    contacts = []
    db_contacts = await get_all(user, db)
    today = date.today()
    for db_contact in db_contacts:
        birthday = db_contact.birthday
        shift = (datetime(today.year, birthday.month, birthday.day).date() - today).days
        if shift < 0:
            shift = (datetime(today.year + 1, birthday.month, birthday.day).date() - today).days
        if shift <= 7:
            contacts.append(db_contact)
    return contacts
