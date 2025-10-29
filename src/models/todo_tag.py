from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class TodoTag(Base):
    __tablename__ = "todo_tags"

    todo_id = Column(Integer, ForeignKey("todo.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
