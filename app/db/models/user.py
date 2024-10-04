from db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
