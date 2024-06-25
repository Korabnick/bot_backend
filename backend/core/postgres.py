from typing import Any, Dict

from sqlalchemy import select, delete, desc, func
from sqlalchemy.sql import and_
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

from backend.metrics import async_integrations_timer
from backend.utils.exceptions import NotFoundException
from backend.models import Calories


class DBWork:

    def __init__(self, session):
        self.session = session

    @staticmethod
    async def get_filter(model, field_to_value: dict[str, Any]) -> list[bool]:
        filters = []
        for column_name, column_value in field_to_value.items():
            if isinstance(column_value, list):
                filters.append(getattr(model, column_name).contains(column_value))
            else:
                filters.append(getattr(model, column_name) == column_value)
        return filters

    @async_integrations_timer
    async def get_obj(
            self,
            model, where: dict[str, Any] = None,
            field_for_load: str = None,
            field_for_order: str = None,
            limit: int = 10,
            offset: int = 0,
    ):
        query = select(model)
        if field_for_load:
            query = query.options(selectinload(getattr(model, field_for_load)))
        if where:
            query = query.filter(and_(*await self.get_filter(model, where)))
        if field_for_order:
            query = query.order_by(desc(getattr(model, field_for_order)))
        query = query.limit(limit).offset(offset)
        return (await self.session.scalars(query)).all()

    @async_integrations_timer
    async def create_obj(self, model, data_for_create: dict[str, Any]):
        obj = model(**data_for_create)
        self.session.add(obj)
        await self.session.commit()
        return obj

    @async_integrations_timer
    async def delete_obj(self, model, where: dict[str, Any]) -> None:
        query = delete(model).where(and_(*await self.get_filter(model, where)))
        await self.session.execute(query)
        await self.session.commit()

    @async_integrations_timer
    async def update_obj(self, model, where: dict, for_set: dict) -> None:
        obj = (await self.get_obj(model, where))
        if not obj:
            raise NotFoundException(f'{model} object with {where.keys()} - {where.values()} does not exist')
        obj = obj[0]
        for attr, new_value in for_set.items():
            setattr(obj, attr, new_value)
        await self.session.commit()
    
    @async_integrations_timer
    async def get_stats(self, user_id: int, period: str) -> Dict[str, Any]:
        from datetime import datetime, timedelta

        period_map = {
            'day': timedelta(days=1),
            'week': timedelta(weeks=1),
            'month': timedelta(days=30)
        }

        if period not in period_map:
            raise ValueError(f"Invalid period: {period}")

        end_date = datetime.utcnow()
        start_date = end_date - period_map[period]

        query = select(
            func.sum(Calories.amount).label('total'),
            func.avg(Calories.amount).label('daily_average')
        ).where(
            and_(
                Calories.user_id == user_id,
                Calories.timestamp.between(start_date, end_date)
            )
        )

        result = await self.session.execute(query)
        stats = result.fetchone()

        return {
            "total": stats.total or 0,
            "daily_average": stats.daily_average or 0.0
        }
