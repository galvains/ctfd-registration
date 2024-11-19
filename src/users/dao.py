from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from src.teams.models import Additional

from src.database import session_factory
from src.utils import generate_username, hash_password


def db_register_user(**filter_by):
    from src.users.models import Users
    try:
        with session_factory() as session:
            username = generate_username()
            hashed_password = hash_password(filter_by['password'])

            user = Users(
                name=username,
                password=hashed_password,
                email=filter_by['email'],
                website=filter_by['website'],
                type="user"
            )
            __data = Additional(
                username=username,
                full_name=filter_by['credentials'],
                email=filter_by['email'],
                age=filter_by['age']
            )

            session.add(user)
            session.add(__data)
            session.commit()
            return user
    except SQLAlchemyError as ex:
        session.rollback()
        return ex


def db_get_user(**filter_by):
    from src.users.models import Users

    try:
        with session_factory() as session:
            stmt = session.execute(select(Users).filter_by(**filter_by)).unique()
            user = stmt.scalars().one_or_none()

            if user:
                return user
            return False
    except SQLAlchemyError as ex:
        session.rollback()
        return ex
