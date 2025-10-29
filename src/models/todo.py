from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.app.database import Base


# 中間テーブル（多対多）
todo_tag = Table(
    "todo_tag",
    Base.metadata,
    Column("todo_id", Integer, ForeignKey("todo.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"))
)


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256), nullable=False)
    complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deadline = Column(DateTime, nullable=True)

    # ✅ 多対多のリレーションをTodoクラス内に
    tags = relationship("Tag", secondary=todo_tag, back_populates="todos")
