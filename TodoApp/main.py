from typing import Optional

from fastapi import FastAPI,Depends,HTTPException
import models
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield  db
    finally:
        db.close()


class Todos(BaseModel):
    title: str
    description: Optional[str]
    priority:int=Field(gt=0,lt=6,description="Value must be between 0 and 6")
    complete:bool


@app.post('/')
async def create_todo(todo : Todos,db : Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()
    return {
        'status' : 201,
        'transaction' : 'Successful'
    }


@app.put("/{model_id}")
async  def update_todo(model_id : int ,todo : Todos,db : Session = Depends(get_db)):
    model_todo = db.query(models.Todos).filter(models.Todos.id == model_id).first()

    if model_todo is None:
        raise HTTPException(status_code=404,detail="This record do not exixts")

    model_todo.title = todo.title
    model_todo.description = todo.description
    model_todo.priority = todo.priority
    model_todo.complete = todo.complete
    db.add(model_todo)
    db.commit()

    return {
        "status" : 200,
        "description" : "Item has been Update"
    }


@app.get('/')
async def read_all(db:Session = Depends(get_db)):
    return db.query(models.Todos).all()

@app.get('/todo/{todo_id}')
async def get_todo_by_id(todo_id :int,db : Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code = 404,
                        detail = " Todo not Found ")

@app.delete('/{id}')
async def delete_todo(id: int,db : Session = Depends(get_db)):
    model_todo = db.query(models.Todos).filter(models.Todos.id == id).first()

    if model_todo is None:
        raise HTTPException(detail="Record Not Found", status_code="404")

    db.query(models.Todos).filter(models.Todos.id == id).delete()
    db.commit()

    return {
        "status" : 200,
        "Description" : "Deleted"
    }
