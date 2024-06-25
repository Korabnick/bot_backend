from .calories import Calories
from .daily_stats import DailyStats
from .user import User

__all__ = [
    "Calories",
    "DailyStats",
    "User",
]

from sqlalchemy.orm import configure_mappers

configure_mappers()
