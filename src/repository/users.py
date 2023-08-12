import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserModel
from src.database.models import User


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    sq = select(User).filter_by(email=email)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    logging.info(user)
    return user


async def create_user(body: UserModel, db: AsyncSession) -> User:
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()
