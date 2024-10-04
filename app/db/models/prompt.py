from db.models.base import (
    BaseModel,
    TimestampCreateMixin,
    TimestampMixin,
    TimestampUpdateMixin,
)
from sqlalchemy import BigInteger, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Prompt(BaseModel, TimestampCreateMixin, TimestampUpdateMixin):
    __tablename__ = "prompt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), nullable=False)
    prompt_variable: Mapped[list["PromptVariable"] | None] = relationship("PromptVariable", back_populates="prompt")


class PromptVariable(BaseModel):
    __tablename__ = "prompt_variable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompt.id", ondelete="CASCADE"))

    prompt: Mapped["Prompt"] = relationship("Prompt", back_populates="prompt_variable", passive_deletes=True)
