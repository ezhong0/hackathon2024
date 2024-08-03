from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

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
    self_description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    experience: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    strength: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    goals: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)

    def __repr__(self):
        return (
            f'<User(id={self.id}, username={self.username}, email={self.email}, '
            f'name={self.name}, age={self.age}, field={self.field}, '
            f'location={self.location}, self_description={self.self_description}, '
            f'experience={self.experience}, strength={self.strength}, goals={self.goals})>'
        )
