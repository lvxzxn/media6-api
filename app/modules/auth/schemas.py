from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    password: str = Field(..., min_length=3)

class AuthStatusResponse(BaseModel):
    authenticated: bool