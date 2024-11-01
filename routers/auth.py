"""Routes related to Authentication and Authorization."""
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, Depends, Response, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from schema import user
from datetime import timedelta
from data.database import db_session
from utils import service

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

templates = Jinja2Templates(directory="templates")


#USER TOKEN GENERATION
@router.post("/token", response_model= user.Token)
async def login_for_access_token(
    response: Response, 
    form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
    db:db_session
    ):
    
    token = service.authenticate_user(form_data.username, form_data.password, timedelta(minutes=60), db)
    
    if token == False:
        return False
        
    response.set_cookie(key="access_token", value = token, httponly=True)
    
    return True










# from fastapi import APIRouter, Depends, HTTPException, Request, Response, Form
# from pydantic import BaseModel
# from models import User
# from passlib.context import CryptContext
# from database import SessionLocal
# from typing import Annotated
# from sqlalchemy.orm import Session
# from starlette import status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt, JWTError
# from datetime import timedelta
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# # from starlette.responses import RedirectResponse


# router = APIRouter(
#     prefix="/auth",
#     tags=["auth"]
# )

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# templates = Jinja2Templates(directory="templates")

# #USER TOKEN GENERATION
# @router.post("/token", response_model=Token)
# async def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     db: db_dependency):
#     user = authenticate_user(form_data.username, form_data.password, db)
    
#     if not user:
#         return False
    
#     token = create_access_token(user.username, user.id, timedelta(minutes=60))
    
#     response.set_cookie(key="access_token", value=token, httponly=True)
    
#     return True

# #login get page route
# @router.get("/login", response_class=HTMLResponse)
# async def authenticationpage(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# #login post page route
# @router.post("/login", response_class=HTMLResponse)
# async def login(request:Request, db: db_dependency):
#     try:
#         form = LoginForm(request)
#         await form.create_outh_form()
#         response = RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)
        
#         validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)
        
#         if not validate_user_cookie:
#             msg = "Invalid username or password"
#             return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
#         return response
#     except HTTPException:
#         msg = "Unknown error"
#         return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


# @router.get("/logout", response_class=HTMLResponse)
# async def logout(request: Request):
#     msg = "Logout successfully"
#     response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
#     response.delete_cookie(key="access_token")
#     return response
