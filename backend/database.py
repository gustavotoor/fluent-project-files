
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, DateTime, Integer
from sqlalchemy.sql import func
from typing import Dict, List, Optional
import os
from datetime import datetime
from config import settings

# Database URL from environment
DATABASE_URL = settings.DATABASE_URL

# Database instance
database = Database(DATABASE_URL)

# SQLAlchemy metadata
metadata = MetaData()

# Define tables
users_table = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("password", String),
    Column("created_at", DateTime, server_default=func.now())
)

projects_table = Table(
    "projects",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("description", Text),
    Column("user_id", String),
    Column("created_at", DateTime, server_default=func.now())
)

messages_table = Table(
    "messages",
    metadata,
    Column("id", String, primary_key=True),
    Column("content", Text),
    Column("sender", String),
    Column("project_id", String),
    Column("timestamp", DateTime, server_default=func.now())
)

files_table = Table(
    "files",
    metadata,
    Column("id", String, primary_key=True),
    Column("filename", String),
    Column("filepath", String),
    Column("size", Integer),
    Column("user_id", String),
    Column("created_at", DateTime, server_default=func.now())
)

# Create engine for table creation
engine = create_engine(DATABASE_URL)

async def create_tables():
    """Create tables if they don't exist"""
    metadata.create_all(engine)

async def connect_db():
    """Connect to database"""
    await database.connect()

async def disconnect_db():
    """Disconnect from database"""
    await database.disconnect()

class PostgresDB:
    """PostgreSQL database operations"""
    
    async def create_user(self, email: str, password_hash: str) -> dict:
        user_id = f"user_{datetime.utcnow().timestamp()}"
        query = users_table.insert().values(
            id=user_id,
            email=email,
            password=password_hash
        )
        await database.execute(query)
        
        return {
            "id": user_id,
            "email": email,
            "password": password_hash,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        query = users_table.select().where(users_table.c.email == email)
        result = await database.fetch_one(query)
        if result:
            return dict(result)
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        query = users_table.select().where(users_table.c.id == user_id)
        result = await database.fetch_one(query)
        if result:
            return dict(result)
        return None
    
    async def create_project(self, name: str, description: str, user_id: str) -> dict:
        project_id = f"project_{datetime.utcnow().timestamp()}"
        query = projects_table.insert().values(
            id=project_id,
            name=name,
            description=description,
            user_id=user_id
        )
        await database.execute(query)
        
        return {
            "id": project_id,
            "name": name,
            "description": description,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def get_projects_by_user(self, user_id: str) -> List[dict]:
        query = projects_table.select().where(projects_table.c.user_id == user_id)
        results = await database.fetch_all(query)
        return [dict(result) for result in results]
    
    async def create_message(self, content: str, sender: str, project_id: Optional[str] = None) -> dict:
        message_id = f"msg_{datetime.utcnow().timestamp()}"
        query = messages_table.insert().values(
            id=message_id,
            content=content,
            sender=sender,
            project_id=project_id
        )
        await database.execute(query)
        
        return {
            "id": message_id,
            "content": content,
            "sender": sender,
            "project_id": project_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_messages(self, project_id: Optional[str] = None) -> List[dict]:
        if project_id:
            query = messages_table.select().where(messages_table.c.project_id == project_id)
        else:
            query = messages_table.select()
        
        results = await database.fetch_all(query)
        return [dict(result) for result in results]

# Global database instance
db = PostgresDB()
