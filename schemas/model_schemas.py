from pydantic import BaseModel


class PhiInput(BaseModel):
    system_prompt: str
    user_prompt: str
