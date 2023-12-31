from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from src.database.models import Note, User
from src.schemas import NoteModel


async def create(body: NoteModel, db: AsyncSession):
    note = Note(**body.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_all(user: User, db: AsyncSession):
    notes = db.query(Note).filter(Note.user_id == user.id).all()
    return notes


async def get_one(note_id, user: User, db: AsyncSession):
    note = await db.query(Note).filter(and_(Note.user_id == user.id, Note.id == note_id)).first()
    return note


async def update(note_id, body: NoteModel, user: User, db: AsyncSession):
    note = await get_one(note_id, user, db)
    if note:
        note.text = body.text
        await db.commit()
    return note


async def delete(note_id, user: User, db: AsyncSession):
    note = await get_one(note_id, user, db)
    if note:
        await db.delete(note)
        await db.commit()
    return note
