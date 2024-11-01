""" schema validation for user route"""
from pydantic import EmailStr, BaseModel
from fastapi import Request
from typing import Optional

# class CreateUserRequest(BaseModel):
#     username: str
#     email: EmailStr
#     first_name: str
#     last_name: str
#     password: str
#     role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        
    async def create_outh_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")
        
        