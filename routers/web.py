"""Routes related to browsing webpages"""

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data import database, model
from sqlalchemy.orm import Session
from utils import service
from starlette.datastructures import URL
from config.config import get_settings


router = APIRouter(tags=["web"])

templates = Jinja2Templates(directory="templates")

#home page route
@router.get("/", response_class = HTMLResponse)
async def home(
    request:Request,
):
    return templates.TemplateResponse("home.html", {"request": request})





