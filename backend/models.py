
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Project(BaseModel):
    id: str
    name: str
    description: str
    created_at: str
    user_id: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class ChatMessage(BaseModel):
    id: str
    content: str
    sender: str  # 'user' or 'assistant'
    timestamp: str
    project_id: Optional[str] = None

class ChatMessageCreate(BaseModel):
    content: str
    project_id: Optional[str] = None

class FileUpload(BaseModel):
    filename: str
    size: int
    message: str
