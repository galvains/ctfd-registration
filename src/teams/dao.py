from typing import Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, select

from src.config import get_team_size
from src.teams.models import Teams
from src.users.models import Users

from src.database import session_factory
from src.utils import verify_password, hash_password

MAX_TEAM_SIZE = get_team_size()


def db_get_team(team_id):
    try:
        with session_factory() as session:
            stmt = session.execute(select(Teams).filter_by(id=team_id)).unique()
            team = stmt.scalars().one_or_none()

            if team:
                return team
            return False
    except SQLAlchemyError as ex:
        session.rollback()
        return ex


def db_create_team(**filter_by):
    captain_id = filter_by['current_user_id']

    try:
        with session_factory() as session:

            hashed_password = hash_password(filter_by['password'])
            team_affiliation: Callable[[str], str | None] = lambda aff: aff if aff else None

            team = Teams(
                name=filter_by['team_name'],
                country=filter_by['team_city'],
                affiliation=team_affiliation(filter_by['team_affiliation']),
                password=hashed_password,
                captain_id=captain_id
            )

            session.add(team)
            session.commit()

            stmt = update(Users).values(team_id=team.id).where(Users.id == str(captain_id))
            session.execute(stmt)
            session.commit()

            return True

    except SQLAlchemyError as ex:
        session.rollback()


def db_join_team(**filter_by):
    try:
        with session_factory() as session:

            stmt = session.execute(select(Teams).filter_by(name=filter_by['team_name']))
            current_team = stmt.scalars().first()

            if current_team:
                valid_password = verify_password(filter_by['team_pwd'], current_team.password)
                check_size = check_count_users_on_team(team_id=current_team.id)

                if valid_password and check_size:
                    session.execute(
                        update(Users).where(Users.id == str(filter_by['current_user_id'])).values(
                            team_id=current_team.id))
                    session.commit()
                    return True
                elif not valid_password:
                    return False
                elif not check_size:
                    return "size_error"

            return False

    except SQLAlchemyError as ex:
        session.rollback()


def check_count_users_on_team(team_id: int) -> bool:
    try:
        with session_factory() as session:
            count_users = session.query(Users).filter_by(team_id=team_id).count()
            return count_users < MAX_TEAM_SIZE
    except SQLAlchemyError as ex:
        session.rollback()


def db_team_exists(team_name):
    try:
        with session_factory() as session:
            stmt = select(Teams).filter_by(name=team_name)
            result = session.execute(stmt).scalars().first()
            return result is not None
    except SQLAlchemyError:
        session.rollback()
        return False
