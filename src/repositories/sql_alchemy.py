from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from config import env_config
import logging
from src.repositories.base import AbstractRepository


logging.basicConfig(level=env_config.LOG_LEVEL)
logger = logging.getLogger(__name__)


class SQLAlchemyRepository(AbstractRepository):

    model = None

    @classmethod
    async def add(
        self,
        session: AsyncSession,
        **data: dict,
    ):
        try:
            stmt = (
                insert(self.model)
                .values(**data)
                .returning(self.model.__table__.columns)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при добавлении записи в базу данных",
                extra={"данные": data, "ошибка": e},
            )
            raise e


    @classmethod
    async def find_one_or_none(
        self,
        session: AsyncSession,
        **filter_by,
    ):
   
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при добавлении записи в базу данных",
                extra={"ошибка": e},
            )
            raise e
        

    @classmethod
    async def find_all(self, session: AsyncSession, **filter_by):
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                f"Ошибка при поиске всех значений в базе данных", extra={"ошибка": e}
            )
            raise e
        

    @classmethod
    async def delete(self, session: AsyncSession, id: int):
        try:
            stmt = delete(self.model).filter_by(id=id).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при удалении значения из базы данных', extra={'ошибка': e})
            return e
        


    @classmethod
    async def update(self, session: AsyncSession, id: int, **data):
        try:
            stmt = update(self.model).filter_by(id=id).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при обновлении значения из базы данных', extra={'ошибка': e})
            return e