from fastapi import Depends, Request
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.responses import Response

from backend.core.postgres import DBWork
from backend.core.postgres_engine import get_db_work
from backend.endpoints.routers import user_router
from backend.models.user import User
from backend.schemas.user import TimezoneOffset, UserItems, NotificationTime
from backend.utils.decorators import handle_domain_exceptions


@handle_domain_exceptions
@user_router.post('')
async def change_timezone(
    request: Request,
    body: TimezoneOffset,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    user_id = int(request.headers.get('user_from_id'))
    if not await db_work.get_obj(model=User, where={'id': user_id}):
        await db_work.create_obj(User, data_for_create={'id': user_id})
    await db_work.update_obj(model=User, where={'id': user_id}, for_set={'timezone_offset': body.offset})
    return Response(status_code=status.HTTP_200_OK)


@user_router.get('/chats')
async def get_chat_ids(
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    users = await db_work.get_obj(model=User)
    data = {'items': []}
    for user in users:
        if user.chat_id:
            data['items'].append({'chat_id': user.chat_id, 'user_id': user.id})
    return ORJSONResponse(content=UserItems(**data).model_dump(mode='json'))


@user_router.post('/notification_time')
async def change_notification_time(
    request: Request,
    body: NotificationTime,
    db_work: DBWork = Depends(get_db_work),
) -> Response:
    user_id = int(request.headers.get('user_from_id'))
    if not await db_work.get_obj(model=User, where={'id': user_id}):
        await db_work.create_obj(User, data_for_create={'id': user_id})
    await db_work.update_obj(model=User, where={'id': user_id}, for_set={
        'notification_hour': body.hour,
        'notification_minute': body.minute
    })
    return Response(status_code=status.HTTP_200_OK)