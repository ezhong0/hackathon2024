from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    # New profile fields
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    age: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    field: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    location: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    location_lat: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    location_lng: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    self_description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    experience: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    strength: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    goals: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)

    profile_photo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))  # Store filename or URL

    def __repr__(self):
        return (
            f'<User(id={self.id}, username={self.username}, email={self.email}, '
            f'name={self.name}, age={self.age}, field={self.field}, '
            f'location={self.location}, self_description={self.self_description}, '
            f'experience={self.experience}, strength={self.strength}, goals={self.goals})>'
        )


class Feedback(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'))
    target_user_id: so.Mapped[int] = so.mapped_column(ForeignKey('user.id'))
    like: so.Mapped[bool] = so.mapped_column(sa.Boolean)

    user = relationship('User', foreign_keys=[user_id])
    target_user = relationship('User', foreign_keys=[target_user_id])

    def __repr__(self):
        return (
            f'<Feedback(id={self.id}, user_id={self.user_id}, '
            f'target_user_id={self.target_user_id}, like={self.like})>'
        )