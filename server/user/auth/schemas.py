from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    create_admin_password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str
