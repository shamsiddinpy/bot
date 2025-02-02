from sqlalchemy import BIGINT, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import AbstractClass


class TelegramUser(AbstractClass):
    __tablename__ = 'telegram_user'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=True)
    language_code: Mapped[str] = mapped_column(String(3), nullable=True, default='uz')
