
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

app = FastAPI(title="ProjectManager API", version="1.0.0")

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-here-min-256-bits")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/app/uploads")

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple in-memory storage (replace with database in production)
users_db = {}
projects_db = {}
chats_db = {}

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
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
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
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user_{len(users_db) + 1}"
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "password": hash_password(user.password)
    }
    
    token = generate_token(user_id)
    return LoginResponse(
        token=token,
        user=UserResponse(id=user_id, email=user.email)
    )

@app.post("/auth/login", response_model=LoginResponse)
async def login(user: User):
    db_user = users_db.get(user.email)
    if not db_user or db_user["password"] != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = generate_token(db_user["id"])
    return LoginResponse(
        token=token,
        user=UserResponse(id=db_user["id"], email=db_user["email"])
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(verify_token)):
    for email, user_data in users_db.items():
        if user_data["id"] == user_id:
            return UserResponse(id=user_data["id"], email=user_data["email"])
    raise HTTPException(status_code=404, detail="User not found")

# Projects endpoints
@app.get("/projects", response_model=List[Project])
async def get_projects(user_id: str = Depends(verify_token)):
    user_projects = [p for p in projects_db.values() if p["user_id"] == user_id]
    return user_projects

@app.post("/projects", response_model=Project)
async def create_project(project_data: dict, user_id: str = Depends(verify_token)):
    project_id = f"project_{len(projects_db) + 1}"
    project = {
        "id": project_id,
        "name": project_data["name"],
        "description": project_data.get("description", ""),
        "created_at": datetime.utcnow().isoformat(),
        "user_id": user_id
    }
    projects_db[project_id] = project
    return project

# Chat endpoints
@app.get("/chat/messages")
async def get_chat_messages(project_id: Optional[str] = None, user_id: str = Depends(verify_token)):
    messages = []
    for msg in chats_db.values():
        if project_id is None or msg.get("project_id") == project_id:
            messages.append(msg)
    return sorted(messages, key=lambda x: x["timestamp"])

@app.post("/chat/send")
async def send_message(message_data: dict, user_id: str = Depends(verify_token)):
    message_id = f"msg_{len(chats_db) + 1}"
    message = {
        "id": message_id,
        "content": message_data["content"],
        "sender": "user",
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": message_data.get("project_id")
    }
    chats_db[message_id] = message
    
    # Simulate AI response
    response_id = f"msg_{len(chats_db) + 1}"
    response = {
        "id": response_id,
        "content": f"Entendi sua mensagem: '{message_data['content']}'. Como posso ajudar com seu projeto?",
        "sender": "assistant",
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": message_data.get("project_id")
    }
    chats_db[response_id] = response
    
    return {"message": message, "response": response}

# Upload endpoints
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(verify_token)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
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
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
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
