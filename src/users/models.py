from src.database import Base
import datetime

from sqlalchemy import Integer, String, Boolean, Column, UniqueConstraint, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from src.teams.models import FieldEntries
from src.users.dao import db_get_user


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("id", "oauth_id"), {})

    id = Column(Integer, primary_key=True)
    oauth_id = Column(Integer, unique=True)

    name = Column(String(128))
    password = Column(String(128))
    email = Column(String(128), unique=True)
    type = Column(String(80))
    secret = Column(String(128))

    website = Column(String(128))
    affiliation = Column(String(128))
    country = Column(String(32))
    bracket_id = Column(
        Integer, ForeignKey("brackets.id", ondelete="SET NULL")
    )
    hidden = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)

    team_id = Column(Integer, ForeignKey("teams.id"))

    field_entries = relationship(
        "UserFieldEntries",
        foreign_keys="UserFieldEntries.user_id",
        lazy="joined",
        back_populates="user",
    )

    created = Column(DateTime, default=datetime.datetime.utcnow)
    language = Column(String(32), nullable=True, default=None)

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": type}

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.id!r}"

    def to_dict(self):
        return {
            "id": self.id,
            "oauth_id": self.oauth_id,

            "name": self.name,
            "password": self.password,
            "email": self.email,
            "type": self.type,
            "secret": self.secret,

            "website": self.website,
            "affiliation": self.affiliation,
            "country": self.country,

            "hidden": self.hidden,
            "banned": self.banned,
            "verified": self.verified,

            "team_id": self.team_id,

            "created": self.created,
            "language": self.language

        }


class UserFieldEntries(FieldEntries):
    __mapper_args__ = {"polymorphic_identity": "user"}
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship(
        "Users", foreign_keys="UserFieldEntries.user_id", back_populates="field_entries"
    )


class Brackets(Base):
    __tablename__ = "brackets"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    type = Column(String(80))


class UserLogin:
    def fromDB(self, user_id):
        from src.teams.dao import db_get_team
        self.__user = db_get_user(id=user_id)
        self.__team = db_get_team(team_id=self.get_team_id())
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        if self.__user:
            return str(self.__user.id)
        return None

    def get_username(self):
        if self.__user:
            return str(self.__user.name)
        return None

    def get_email(self):
        if self.__user:
            return str(self.__user.email)
        return None

    def get_team_id(self):
        return str(self.__user.team_id)

    def get_team_name(self):
        if self.__team:
            return str(self.__team.name)
        return None
