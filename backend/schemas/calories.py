from pydantic import BaseModel, Field
from datetime import datetime


class CaloriesCreate(BaseModel):
    amount: float = Field(..., gt=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    timezone_offset: int


class CaloriesStats(BaseModel):
    total: float
    daily_average: float

    class Config:
        schema_extra = {
            "example": {
                "total": 2000,
                "daily_average": 500.0
            }
        }