from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db, init_db
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI and SQLite",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to Todo API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, tags=["Todos"])
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo item
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoResponse], tags=["Todos"])
def get_all_todos(
    skip: int = 0,
    limit: int = 100,
    completed: bool = None,
    db: Session = Depends(get_db)
):
    """
    Get all todos with optional filtering
    """
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    todos = query.offset(skip).limit(limit).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Get a specific todo by ID
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse, tags=["Todos"])
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """
    Update a todo item
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    update_data = todo_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(todo, field, value)

    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a todo item
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    db.delete(todo)
    db.commit()
    return None

@app.patch("/todos/{todo_id}/complete", response_model=TodoResponse, tags=["Todos"])
def mark_todo_complete(todo_id: int, db: Session = Depends(get_db)):
    """
    Mark a todo as completed
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    todo.completed = True
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

@app.patch("/todos/{todo_id}/incomplete", response_model=TodoResponse, tags=["Todos"])
def mark_todo_incomplete(todo_id: int, db: Session = Depends(get_db)):
    """
    Mark a todo as incomplete
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    todo.completed = False
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo
