
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class InMemoryDB:
    """Simple in-memory database for development"""
    
    def __init__(self):
        self.users: Dict[str, dict] = {}
        self.projects: Dict[str, dict] = {}
        self.messages: Dict[str, dict] = {}
        self.files: Dict[str, dict] = {}
        
    def create_user(self, email: str, password_hash: str) -> dict:
        user_id = f"user_{len(self.users) + 1}"
        user = {
            "id": user_id,
            "email": email,
            "password": password_hash,
            "created_at": datetime.utcnow().isoformat()
        }
        self.users[email] = user
        return user
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.users.get(email)
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        for user in self.users.values():
            if user["id"] == user_id:
                return user
        return None
    
    def create_project(self, name: str, description: str, user_id: str) -> dict:
        project_id = f"project_{len(self.projects) + 1}"
        project = {
            "id": project_id,
            "name": name,
            "description": description,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat()
        }
        self.projects[project_id] = project
        return project
    
    def get_projects_by_user(self, user_id: str) -> List[dict]:
        return [p for p in self.projects.values() if p["user_id"] == user_id]
    
    def create_message(self, content: str, sender: str, project_id: Optional[str] = None) -> dict:
        message_id = f"msg_{len(self.messages) + 1}"
        message = {
            "id": message_id,
            "content": content,
            "sender": sender,
            "project_id": project_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.messages[message_id] = message
        return message
    
    def get_messages(self, project_id: Optional[str] = None) -> List[dict]:
        if project_id:
            return [m for m in self.messages.values() if m.get("project_id") == project_id]
        return list(self.messages.values())

# Global database instance
db = InMemoryDB()
