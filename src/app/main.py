from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # noqa: F401
from datetime import datetime
from src.app.router import router
from fastapi.staticfiles import StaticFiles
from urllib.parse import urlencode


from src.app.database import SessionLocal
from src.crud import todo as crud_todo, tag as crud_tag
from src.schemas.schema import TodoCreate

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index(request: Request):
    error = request.query_params.get("error")
    db = SessionLocal()
    todos = crud_todo.get_todos(db)
    tags = crud_tag.get_all_tags(db)
    db.close()
    return templates.TemplateResponse(
        "index.html", {"request": request, "todos": todos, "error": error, "tags": tags}
    )


@app.post("/add")
def add_todo(
    request: Request,
    content: str = Form(...),
    deadline: str = Form(None),
    tag_ids: list[int] = Form([]),  # ← 複数タグ対応
    db: Session = Depends(get_db),
):
    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
    if deadline_dt.date() < datetime.now().date():
        params = urlencode({"error": "過去の日付は登録できません。"})
        return RedirectResponse(f"/?{params}", status_code=303)
    else:
        deadline_dt = None
    crud_todo.create_todo(db, content, deadline_dt, tag_ids)
    return RedirectResponse("/", status_code=303)


# 編集フォームの表示


@app.get("/edit/{todo_id}")
def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = crud_todo.get_todo_by_id(db, todo_id)
    tags = crud_tag.get_all_tags(db)  # タグ一覧を取得
    return templates.TemplateResponse(
        "edit.html", {"request": request, "todo": todo, "tags": tags}
    )


# 編集実行


@app.post("/edit/{todo_id}")
def update_todo(
    request: Request,
    todo_id: int,
    content: str = Form(...),
    deadline: str = Form(None),
    tag_ids: list[int] = Form([]),  # ← 複数タグに対応
    db: Session = Depends(get_db),
):
    crud_todo.update_todo(db, todo_id, content, deadline, tag_ids)
    return RedirectResponse("/", status_code=303)
