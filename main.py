from fastapi import FastAPI
# from routers.auth import router
# from routers.todo import todo_router
from starlette.staticfiles import StaticFiles
from config.config import get_settings
from fastapi.templating import Jinja2Templates
from data.database import engine
from data.model import Base
from routers import auth, todo, web, user

app = FastAPI(
    title="Ezzy todo application",
    description="A FastAPI-based todo app.",
    version="0.1.0",
    openapi_tags= get_settings().tags
)

#HTML Dependencies
templates = Jinja2Templates(directory="templates")

#CSS/JS Dependencies
app.mount("/static", StaticFiles(directory="static"), name="static")

#Bindings database
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(web.router)
app.include_router(todo.router)