from src.repositories.sql_alchemy import SQLAlchemyRepository
from src.models.user import User




class UserRepository(SQLAlchemyRepository):

    model: User = User