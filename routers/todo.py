"""Routes related to todo CRUD actions"""

from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data import database, model
from sqlalchemy.orm import Session
from utils import service

router = APIRouter(prefix="/todo", tags=["todo"])

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def read_all_by_user(
    request:Request, 
    db:Session=Depends(database.get_db)
    ):
    
    user = service.get_user_from_token(request, db)
    if not user:
        return RedirectResponse("/user/login", status_code=status.HTTP_404_NOT_FOUND)
    
    """View URL."""
    todos = db.query(model.Todos).filter(model.Todos.owner_id == user.id).all()
    
    return templates.TemplateResponse(
        "home.html", {
            "request": request, 
            "todos": todos, 
            "user": user
        }
    )

#create_todo GET route
@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(
    request:Request,
    db:Session=Depends(database.get_db)
    ):
    
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        msg = []
        
        msg.append("Session Expired, Login")
        
        return templates.TemplateResponse(
            "add-todo.html", 
            {"request": request, "user": user}
        )
        
    return templates.TemplateResponse(
        "add-todo.html", 
        {"request": request, "user": user}
    )

#create_todo POST route.
@router.post("/add-todo", response_class=HTMLResponse)
async def add_new_todo_post(
    request:Request, 
    db:Session=Depends(database.get_db),
    title: str = Form(...), 
    description: str = Form(...),
    priority: int = Form(...)
    ):

    """Create a todo entry."""
    
    msg = []

    # authentication
    user = service.get_user_from_token(request, db)
    
    if user is None:
        msg.append("Session Expired, Login")
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    
    
    #database dump
    todo_model = model.Todos(
    title = title,
    description = description,
    priority = priority,
    completed = False,
    owner_id = user.id
    )
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return RedirectResponse("/todo/dashboard", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(
    request:Request, 
    todo_id: int, 
    db:Session=Depends(database.get_db)
    ):
    
    msg = []

    # authentication
    user = service.get_user_from_token(request, db)   
    
    if user is None:
        msg.append("session expired, kindly Login")
        return templates.TemplateResponse("login.html", {'request':Request, 'msg':msg})
    
    todo = db.query(model.Todos).filter(model.Todos.id == todo_id).first()
    
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user, "msg": msg})

#edit PUT ROUTE
@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(
    request:Request, 
    todo_id: int, 
    db:Session=Depends(database.get_db), 
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...)
    ):
    
    msg = []
    
    # authentication
    user = service.get_user_from_token(request, db)
    if not user:
        msg.append("session expired, kindly Login")
        return templates.TemplateResponse("login.html", {'request':Request, 'msg':msg})
    
    todo = db.query(model.Todos).filter(model.Todos.id == todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = priority
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)

#delete entry routes
@router.get("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(
    request:Request, 
    todo_id: int, 
    db:Session=Depends(database.get_db)
    ):
    
    msg = []
    
    user = service.get_user_from_token(request, db)
    if user is None:
        msg.append("session expired, kindly Login again")
        return templates.TemplateResponse(
            "login.html", 
            {'request':Request, 'msg':msg}, 
            status_code=status.HTTP_403_FORBIDDEN
        )

    todo_model = db.query(model.Todos).filter(model.Todos.id == todo_id).filter(model.Todos.owner_id == user.id).first()
    
    if todo_model is None:
        return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)
    
    db.delete(todo_model)
    db.commit()
    
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(
    request:Request, 
    todo_id: int, 
    db:Session=Depends(database.get_db)
    ):
    
    msg = []
    
    user = service.get_user_from_token(request, db)
    if user is None:
        return RedirectResponse("/todo/login", status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(model.Todos).filter(model.Todos.id == todo_id).filter(model.Todos.ower_id == user.get.id).first()
    
    if todo_model is None:
        return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)
    
    todo_model.completed = not todo_model.completed
    
    db.add(todo_model)
    db.commit()
    
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)
