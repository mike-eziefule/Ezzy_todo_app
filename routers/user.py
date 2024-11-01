"""Routes related to User Account creation."""

from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from data import database, model
from utils.service import bcrpyt_context
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.rate_limit import rate_limiter
from schema import user
from starlette.responses import RedirectResponse
from routers import auth

router = APIRouter(prefix="/user", tags=["user"])

templates = Jinja2Templates(directory="templates")


#register page route
@router.get("/sign-up", response_class=HTMLResponse)
@rate_limiter(max_calls=3, time_frame=60)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#NEW USER REGISTRATION
@router.post('/sign-up', response_class=HTMLResponse)
async def register(
    request: Request, 
    email: str = Form(...), 
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...), 
    password: str = Form(...), 
    password2: str = Form(...),
    role: str = Form(...),
    db:Session=Depends(database.get_db)    
    ):
    
    msg = []
    
    if password != password2:
        msg.append("Passwords do not match")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "msg": msg,
            'email': email,
            "first_name": first_name,  
            "last_name": last_name,
            "username" : username,
            "role": role
        })
    
    if len(password) < 6:
        msg.append("Password should be > 6 character")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "msg": msg,
            'email': email,
            "first_name": first_name,  
            "last_name": last_name,
            "username" : username,
            "role": role
        })

    new_user = model.User(
        email = email,
        username = username,
        first_name = first_name,
        last_name = last_name,
        hashed_password = bcrpyt_context.hash(password),
        is_active = True,
        role = role
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        msg.append("Registration successful")
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, 
                "msg": msg,
            })
        
    except IntegrityError:
        msg.append("Email or Username already taken")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "msg": msg,
            "first_name": first_name,  
            "last_name": last_name,
            "username" : username,
            "role": role
        })

#login get page route
@router.get("/login", response_class=HTMLResponse)
@rate_limiter(max_calls=3, time_frame=60)
async def authenticationpage(request: Request):
    
    return templates.TemplateResponse("login.html", {"request": request})

#login post page route
@router.post("/login", response_class=HTMLResponse)
@rate_limiter(max_calls=3, time_frame=60)
async def login(
    request:Request, 
    db:Session=Depends(database.get_db)
    ):
    
    msg = []
    
    try:
        form = user.LoginForm(request)
        await form.create_auth_form()
        response = RedirectResponse("/todo/dashboard", status_code = status.HTTP_302_FOUND)
        
        validate_user_cookie = await auth.login_for_access_token(response=response, form_data=form, db=db)
        
        if not validate_user_cookie:
            msg.append("Invalid Email or Password")
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "msg": msg, 
                "email": form.username
            })
        
        return response
    except HTTPException:
        msg.append("Unknown error")
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "msg": msg,
            "email": form.username
            })
    

#logout page route
@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    
    msg = []
    
    msg.append("Logout successful")
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


# #EDITING USER INFORMATION BY User ONLY
# @router.put("/edit_user")
# async def edit_username(username, db:Session=Depends(database.get_db), token:str=Depends(oauth2_scheme)):
    
#     # authentication
#     user = get_user_from_token(db, token)
    
#     #Authorazation
#     scan_db = db.query(model.USER).filter(model.USER.email == user.email)
#     if not scan_db.first():
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="UNAUTHORIZED USER"
#         )
    
#     scan_db.update({model.USER.username:username})
#     db.commit()
#     raise HTTPException(
#             status_code=status.HTTP_202_ACCEPTED, 
#             detail='Information updated successfully'
#         )