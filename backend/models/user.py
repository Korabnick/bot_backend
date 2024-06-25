from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.meta import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timezone_offset: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=True)
    notification_hour: Mapped[int] = mapped_column(Integer, nullable=True)
    notification_minute: Mapped[int] = mapped_column(Integer, nullable=True)
