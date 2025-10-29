from fastapi import APIRouter, Form, Body, HTTPException
from fastapi.responses import RedirectResponse
from src.app.database import SessionLocal
from src.crud import todo as crud_todo
from src.models.todo import Todo
from src.schemas.schema import TodoCreate
from datetime import datetime
from urllib.parse import urlencode
from src.crud import tag as crud_tag
from src.models.tag import Tag
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/tags")
def tag_list(request: Request):
    db = SessionLocal()
    tags = db.query(Tag).all()
    db.close()
    return templates.TemplateResponse("tags.html", {"request": request, "tags": tags})


@router.post("/tags/add")
def add_tag(name: str = Form(...)):
    db = SessionLocal()
    crud_tag.create_tag(db, name)
    db.close()
    return RedirectResponse("/tags", status_code=303)


@router.post("/tags/delete/{tag_id}")
def delete_tag(tag_id: int):
    db = SessionLocal()
    crud_tag.delete_tag(db, tag_id)
    db.close()
    return RedirectResponse("/tags", status_code=303)


@router.post("/api/add")
def add_todo_api(data: dict = Body(...)):
    db = SessionLocal()
    content = data.get("content")
    deadline = data.get("deadline")

    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None

    # ✅ 過去日チェック
    if deadline_dt and deadline_dt.date() < datetime.now().date():
        db.close()
        raise HTTPException(status_code=400, detail="期限は今日以降の日付を指定してください。")

    new_todo = TodoCreate(content=content, deadline=deadline_dt)
    crud_todo.create_todo(db, new_todo)
    db.close()
    return {"message": "Todo created successfully"}


# =============================
# 🗑 ToDo削除
# =============================
@router.post("/delete/{todo_id}", response_class=RedirectResponse)
def delete_todo(todo_id: int):
    db = SessionLocal()
    crud_todo.delete_todo(db, todo_id)
    db.close()
    return RedirectResponse("/", status_code=303)


# =============================
# ✏️ ToDo編集（完了済みは不可）
# =============================
@router.post("/edit/{todo_id}", response_class=RedirectResponse)
def edit_todo(
    todo_id: int,
    content: str = Form(...),
    deadline: str = Form(None),
    tag_ids: list[int] = Form([]),
):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        db.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    # ✅ 完了済みは編集禁止
    if todo.complete:
        db.close()
        raise HTTPException(status_code=400, detail="完了済みのタスクは編集できません。")

    # ✅ 過去日チェック
    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
    if deadline_dt and deadline_dt.date() < datetime.now().date():
        db.close()
        raise HTTPException(status_code=400, detail="期限は今日以降の日付を指定してください。")

    crud_todo.update_todo(db, todo_id, content, deadline_dt, tag_ids)
    db.close()
    return RedirectResponse("/", status_code=303)


# =============================
# ✅ 完了トグル
# =============================
@router.post("/toggle/{todo_id}", response_class=RedirectResponse)
def toggle_complete(todo_id: int, complete: bool = Form(...)):
    db = SessionLocal()
    crud_todo.toggle_complete(db, todo_id, complete)
    db.close()
    return RedirectResponse("/", status_code=303)
