from fastapi import Depends, Request, HTTPException, Query, Header
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.responses import Response

from backend.core.postgres import DBWork
from backend.core.postgres_engine import get_db_work
from backend.endpoints.routers import calories_router, stats_router
from backend.models.calories import Calories
from backend.models.user import User
from backend.schemas.calories import CaloriesCreate, CaloriesStats
from backend.utils.decorators import handle_domain_exceptions


async def get_user_from_id(user_from_id: str = Header(...)):
    if not user_from_id:
        raise HTTPException(status_code=400, detail="Missing user_from_id header")
    return user_from_id


@calories_router.post('')
@handle_domain_exceptions
async def add_calories(
    request: Request,
    body: CaloriesCreate,
    user_from_id: str = Header(...),
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    user_id = int(user_from_id)
    
    user = await db_work.get_obj(model=User, where={'id': user_id})
    if not user:
        user = await db_work.create_obj(User, data_for_create={'id': user_id})
    else:
        user = user[0]
        user_chat_id = request.headers.get('user_chat_id')
        if user_chat_id is not None:
            if not user.chat_id:
                await db_work.update_obj(
                    User,
                    where={'id': user_id},
                    for_set={'chat_id': int(user_chat_id)}
                )

    await db_work.create_obj(
        Calories, {
            'user_id': user_id,
            'amount': body.amount,
            'timestamp': body.timestamp,
            'timezone_offset': user.timezone_offset
        })
    return Response(status_code=status.HTTP_201_CREATED)


@stats_router.get('', response_model=CaloriesStats)
async def get_calories_stats(
    request: Request,
    period: str = Query(..., description="Период для статистики (например, 'day', 'week', 'month')"),
    user_from_id: str = Header(...),
    db_work: DBWork = Depends(get_db_work),
) -> ORJSONResponse:
    user_id = int(user_from_id)
    
    user = await db_work.get_obj(model=User, where={'id': user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    stats = await db_work.get_stats(user_id, period)
    return ORJSONResponse(content=stats)
