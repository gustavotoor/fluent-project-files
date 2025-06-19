
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import jwt
import hashlib
import json
import shutil
from datetime import datetime, timedelta
from database import db, connect_db, disconnect_db, create_tables
from config import settings

app = FastAPI(title="ProjectManager API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Ensure upload folder exists
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

# Database startup/shutdown events
@app.on_event("startup")
async def startup():
    await connect_db()
    await create_tables()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# Models
class User(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str

class LoginResponse(BaseModel):
    token: str
    user: UserResponse

class Project(BaseModel):
    id: str
    name: str
    description: str
    created_at: str
    user_id: str

class ChatMessage(BaseModel):
    id: str
    content: str
    sender: str  # 'user' or 'assistant'
    timestamp: str
    project_id: Optional[str] = None

# Utility functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Auth endpoints
@app.post("/auth/register", response_model=LoginResponse)
async def register(user: User):
    existing_user = await db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await db.create_user(user.email, hash_password(user.password))
    token = generate_token(new_user["id"])
    
    return LoginResponse(
        token=token,
        user=UserResponse(id=new_user["id"], email=new_user["email"])
    )

@app.post("/auth/login", response_model=LoginResponse)
async def login(user: User):
    db_user = await db.get_user_by_email(user.email)
    if not db_user or db_user["password"] != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = generate_token(db_user["id"])
    return LoginResponse(
        token=token,
        user=UserResponse(id=db_user["id"], email=db_user["email"])
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(verify_token)):
    user = await db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user["id"], email=user["email"])

# Projects endpoints
@app.get("/projects", response_model=List[Project])
async def get_projects(user_id: str = Depends(verify_token)):
    projects = await db.get_projects_by_user(user_id)
    return projects

@app.post("/projects", response_model=Project)
async def create_project(project_data: dict, user_id: str = Depends(verify_token)):
    project = await db.create_project(
        project_data["name"],
        project_data.get("description", ""),
        user_id
    )
    return project

# Chat endpoints
@app.get("/chat/messages")
async def get_chat_messages(project_id: Optional[str] = None, user_id: str = Depends(verify_token)):
    messages = await db.get_messages(project_id)
    return sorted(messages, key=lambda x: x["timestamp"])

@app.post("/chat/send")
async def send_message(message_data: dict, user_id: str = Depends(verify_token)):
    message = await db.create_message(
        message_data["content"],
        "user",
        message_data.get("project_id")
    )
    
    # Simulate AI response
    response = await db.create_message(
        f"Entendi sua mensagem: '{message_data['content']}'. Como posso ajudar com seu projeto?",
        "assistant",
        message_data.get("project_id")
    )
    
    return {"message": message, "response": response}

# Upload endpoints
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(verify_token)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "size": os.path.getsize(file_path),
        "message": "File uploaded successfully"
    }

@app.get("/uploads")
async def list_uploads(user_id: str = Depends(verify_token)):
    files = []
    if os.path.exists(settings.UPLOAD_FOLDER):
        for filename in os.listdir(settings.UPLOAD_FOLDER):
            filepath = os.path.join(settings.UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                files.append({
                    "filename": filename,
                    "size": os.path.getsize(filepath),
                    "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                })
    return files

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
