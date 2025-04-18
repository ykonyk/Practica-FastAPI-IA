from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PromptRequest(BaseModel):
    prompt: str
    content_type: str = "general"

class CreationBase(BaseModel):
    prompt: str
    content_type: str
    generated_text: Optional[str] = None

class Creation(CreationBase):
    id: int
    timestamp: datetime