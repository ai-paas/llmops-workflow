from db.models.base import (
    BaseModel,
    TimestampCreateMixin,
    TimestampMixin,
    TimestampUpdateMixin,
)
from sqlalchemy import BigInteger, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Solution(BaseModel, TimestampMixin):
    __tablename__ = "solution"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    knowledge_id: Mapped[int] = mapped_column(ForeignKey("knowledge.id", ondelete="CASCADE"))
    knowledge: Mapped["Knowledge"] = relationship("Knowledge")
    solution_config: Mapped["SolutionConfig"] = relationship("SolutionConfig", back_populates="solution")


class SolutionConfig(BaseModel):
    __tablename__ = "solution_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    solution_id: Mapped[int] = mapped_column(ForeignKey("solution.id", ondelete="CASCADE"))

    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    presence_penalty: Mapped[float] = mapped_column(Float, nullable=False)
    frequency_penalty: Mapped[float] = mapped_column(Float, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    top_p: Mapped[float] = mapped_column(Integer, nullable=False)

    solution: Mapped["Solution"] = relationship("Solution", back_populates="solution_config", passive_deletes=True)
