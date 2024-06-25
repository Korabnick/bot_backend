from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.meta import Base


class Calories(Base):
    __tablename__ = 'calories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    timezone_offset: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
