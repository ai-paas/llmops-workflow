from db.models.base import (
    BaseModel,
    TimestampCreateMixin,
    TimestampMixin,
    TimestampUpdateMixin,
)
from sqlalchemy import BigInteger, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Knowledge(BaseModel, TimestampMixin):
    __tablename__ = "knowledge"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    permission_id: Mapped[int] = mapped_column(ForeignKey("permission.id"))
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"))
    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    chunk_type_id: Mapped[int] = mapped_column(ForeignKey("chunk_type.id"))
    search_type_id: Mapped[int] = mapped_column(ForeignKey("search_type.id"))
    top_k: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Float)
    chunk_length: Mapped[int] = mapped_column(Integer)
    overlap: Mapped[int] = mapped_column(Integer)

    permission: Mapped["Permission"] = relationship("Permission")
    language: Mapped["Language"] = relationship("Language")
    model: Mapped["Model"] = relationship("Model")
    search_type: Mapped["SearchType"] = relationship("SearchType")
    chunk_type: Mapped["ChunkType"] = relationship("ChunkType")
    dataset: Mapped[list["KnowledgeFile"] | None] = relationship("KnowledgeFile", back_populates="knowledge")


class KnowledgeFile(BaseModel, TimestampCreateMixin, TimestampUpdateMixin):
    __tablename__ = "knowledge_file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    path: Mapped[str] = mapped_column(String(256), nullable=False)
    knowledge_id: Mapped[int] = mapped_column(ForeignKey("knowledge.id", ondelete="CASCADE"))
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)
    chunk_number: Mapped[int] = mapped_column(Integer)

    knowledge: Mapped["Model"] = relationship("Knowledge", back_populates="dataset", passive_deletes=True)


class FileType(BaseModel):
    __tablename__ = "file_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)


class Language(BaseModel):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)


class SearchType(BaseModel):
    __tablename__ = "search_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)


class ChunkType(BaseModel):
    __tablename__ = "chunk_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)


class Permission(BaseModel):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
