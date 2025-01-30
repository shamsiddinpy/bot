import datetime

from sqlalchemy import BIGINT, BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from config.base import engine, AbstractClass


class TelegramUser(AbstractClass):
    __tablename__ = 'telegram_user'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=True)


class User(AbstractClass):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    is_active: Mapped[bool] = mapped_column('is_active', nullable=False)
    last_name: Mapped[str] = mapped_column('last_name', nullable=False)
    first_name: Mapped[str] = mapped_column('first_name', nullable=False)
    avatar: Mapped[str] = mapped_column('avatar', nullable=False)
