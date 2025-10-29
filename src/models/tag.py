from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.app.database import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    todos = relationship("Todo", secondary="todo_tag", back_populates="tags")
