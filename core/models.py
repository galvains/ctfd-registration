import os
import datetime

from sqlalchemy import create_engine, Integer, String, Boolean, Column, UniqueConstraint, ForeignKey, DateTime, Text, \
    JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
session_factory = sessionmaker(bind=engine)


class Pages(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True)
    data = Column(String(128))


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("id", "oauth_id"), {})
    # Core attributes
    id = Column(Integer, primary_key=True)
    oauth_id = Column(Integer, unique=True)
    # User names are not constrained to be unique to allow for official/unofficial teams.
    name = Column(String(128))
    password = Column(String(128))
    email = Column(String(128), unique=True)
    type = Column(String(80))
    secret = Column(String(128))

    # Supplementary attributes
    website = Column(String(128))
    affiliation = Column(String(128))
    country = Column(String(32))
    bracket_id = Column(
        Integer, ForeignKey("brackets.id", ondelete="SET NULL")
    )
    hidden = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)

    # Relationship for Teams
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


class Teams(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("id", "oauth_id"), {})
    # Core attributes
    id = Column(Integer, primary_key=True)
    oauth_id = Column(Integer, unique=True)
    # Team names are not constrained to be unique to allow for official/unofficial teams.
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    secret = Column(String(128))

    members = relationship(
        "Users", backref="team", foreign_keys="Users.team_id", lazy="joined"
    )

    # Supplementary attributes
    website = Column(String(128))
    affiliation = Column(String(128))
    country = Column(String(32))
    bracket_id = Column(
        Integer, ForeignKey("brackets.id", ondelete="SET NULL")
    )
    hidden = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)

    # Relationship for Users

    field_entries = relationship(
        "TeamFieldEntries",
        foreign_keys="TeamFieldEntries.team_id",
        lazy="joined",
        back_populates="team",
    )

    created = Column(DateTime, default=datetime.datetime.utcnow)
    captain_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    captain = relationship("Users", foreign_keys=[captain_id])

    def __init__(self, **kwargs):
        super(Teams, self).__init__(**kwargs)


class FieldEntries(Base):
    __tablename__ = "field_entries"
    id = Column(Integer, primary_key=True)
    type = Column(String(80), default="standard")
    value = Column(JSON)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))

    field = relationship(
        "Fields", foreign_keys="FieldEntries.field_id", lazy="joined"
    )

    __mapper_args__ = {"polymorphic_identity": "standard", "polymorphic_on": type}


class Fields(Base):
    __tablename__ = "fields"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    type = Column(String(80), default="standard")
    field_type = Column(String(80))
    description = Column(Text)
    required = Column(Boolean, default=False)
    public = Column(Boolean, default=False)
    editable = Column(Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "standard", "polymorphic_on": type}


class Brackets(Base):
    __tablename__ = "brackets"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    type = Column(String(80))


class TeamFieldEntries(FieldEntries):
    __mapper_args__ = {"polymorphic_identity": "team"}
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    team = relationship(
        "Teams", foreign_keys="TeamFieldEntries.team_id", back_populates="field_entries"
    )


class UserFieldEntries(FieldEntries):
    __mapper_args__ = {"polymorphic_identity": "user"}
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship(
        "Users", foreign_keys="UserFieldEntries.user_id", back_populates="field_entries"
    )
