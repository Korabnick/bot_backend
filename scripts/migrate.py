import asyncio

from backend.core.postgres_engine import engine
from backend.models import meta


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.drop_all)
        await conn.run_sync(meta.metadata.create_all)

asyncio.run(main())
