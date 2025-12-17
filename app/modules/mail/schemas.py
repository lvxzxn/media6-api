from pydantic import BaseModel, Field

class SendMailSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    contact: str = Field(..., min_length=3, max_length=100)
    message: str = Field(..., min_length=5, max_length=2000)
    hcaptcha_token: str