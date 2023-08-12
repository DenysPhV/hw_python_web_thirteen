from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Note, User
from src.schemas import NoteModel


async def create(body: NoteModel, db: Session):
    note = Note(**body.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def get_all(user: User, db: Session):
    notes = db.query(Note).filter(Note.user_id == user.id).all()
    return notes


async def get_one(note_id, user: User, db: Session):
    note = db.query(Note).filter(and_(Note.user_id == user.id, id=note_id)).first()
    return note


async def update(note_id, body: NoteModel, user: User, db: Session):
    note = await get_one(note_id, user, db)
    if note:
        note.text = body.text
        db.commit()
    return note


async def delete(note_id, user: User, db: Session):
    note = await get_one(note_id, user, db)
    if note:
        db.delete(note)
        db.commit()
    return note