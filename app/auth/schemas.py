from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    email : EmailStr
    password : str


class TokenResponse(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str = "bearer"

class PasswordReset(BaseModel):
    email : EmailStr

class PasswordResetConfirm(BaseModel):
    token : str
    new_password : str