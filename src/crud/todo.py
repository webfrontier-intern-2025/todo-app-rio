from sqlalchemy.orm import Session
from src.models.todo import Todo
from src.schemas.schema import TodoCreate, TodoUpdate   # noqa: F401
from src.models.tag import Tag
from sqlalchemy.orm import joinedload


def get_todos(db: Session):
    return (
        db.query(Todo)
        .options(joinedload(Todo.tags))  
        .order_by(Todo.created_at.desc())
        .all()
    )


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db, content, deadline, tag_ids):
    todo = Todo(content=content, deadline=deadline)

    # 複数タグを設定
    if tag_ids:
        from src.models.tag import Tag
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        todo.tags = tags

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()


def update_todo(db, todo_id: int, content: str, deadline, tag_ids: list[int]):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.content = content
        todo.deadline = deadline

    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        todo.tags = tags  # 既存のタグ関係を上書き

        db.commit()


def toggle_complete(db, todo_id: int, complete: bool):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.complete = complete
        db.commit()


def create_todo_with_tags(db, content: str, tag_ids: list[int]):
    todo = Todo(content=content)
    if tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        todo.tags = tags
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).options(joinedload(Todo.tags)).filter(Todo.id == todo_id).first()