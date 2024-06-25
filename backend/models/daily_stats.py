from sqlalchemy import Integer, ForeignKey, Date, Float
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.meta import Base


class DailyStats(Base):
    __tablename__ = 'daily_stats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    total_calories: Mapped[float] = mapped_column(Float, nullable=False)
