import datetime

from sqlalchemy import Integer, String, Boolean, Column, UniqueConstraint, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship

from src.database import Base


class Additional(Base):
    __tablename__ = "additional"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(256))
    username = Column(String(128))
    email = Column(String(128), unique=True)
    age = Column(Integer)

    def __repr__(self):
        return f"{self.email!r}"


class Teams(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("id", "oauth_id"), {})

    id = Column(Integer, primary_key=True)
    oauth_id = Column(Integer, unique=True)

    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    secret = Column(String(128))

    members = relationship(
        "Users", backref="team", foreign_keys="Users.team_id", lazy="joined"
    )

    website = Column(String(128))
    affiliation = Column(String(128))
    country = Column(String(32))
    bracket_id = Column(
        Integer, ForeignKey("brackets.id", ondelete="SET NULL")
    )
    hidden = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)

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


class TeamFieldEntries(FieldEntries):
    __mapper_args__ = {"polymorphic_identity": "team"}
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    team = relationship(
        "Teams", foreign_keys="TeamFieldEntries.team_id", back_populates="field_entries"
    )
