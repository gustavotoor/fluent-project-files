
import asyncio
import asyncpg
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresDB:
    """PostgreSQL database operations using asyncpg"""
    
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        """Create connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database pool created successfully")
            await self.create_tables()
        except Exception as e:
            logger.error(f"Failed to create database pool: {e}")
            raise
    
    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database pool closed")
    
    async def create_tables(self):
        """Create tables if they don't exist"""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_projects_table = """
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
        
        create_messages_table = """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            sender TEXT NOT NULL,
            project_id TEXT,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        );
        """
        
        create_files_table = """
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            size INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
        
        async with self.pool.acquire() as conn:
            await conn.execute(create_users_table)
            await conn.execute(create_projects_table)
            await conn.execute(create_messages_table)
            await conn.execute(create_files_table)
            logger.info("Tables created successfully")
    
    async def create_user(self, email: str, password_hash: str) -> dict:
        """Create a new user"""
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        created_at = datetime.utcnow()
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (id, email, password, created_at) VALUES ($1, $2, $3, $4)",
                user_id, email, password_hash, created_at
            )
        
        logger.info(f"User created: {user_id} - {email}")
        return {
            "id": user_id,
            "email": email,
            "password": password_hash,
            "created_at": created_at.isoformat()
        }
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, email, password, created_at FROM users WHERE email = $1",
                email
            )
            if row:
                return dict(row)
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, email, password, created_at FROM users WHERE id = $1",
                user_id
            )
            if row:
                return dict(row)
        return None
    
    async def create_project(self, name: str, description: str, user_id: str) -> dict:
        """Create a new project"""
        project_id = f"project_{uuid.uuid4().hex[:8]}"
        created_at = datetime.utcnow()
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO projects (id, name, description, user_id, created_at) VALUES ($1, $2, $3, $4, $5)",
                project_id, name, description, user_id, created_at
            )
        
        logger.info(f"Project created: {project_id} - {name}")
        return {
            "id": project_id,
            "name": name,
            "description": description,
            "user_id": user_id,
            "created_at": created_at.isoformat()
        }
    
    async def get_projects_by_user(self, user_id: str) -> List[dict]:
        """Get all projects for a user"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, name, description, user_id, created_at FROM projects WHERE user_id = $1 ORDER BY created_at DESC",
                user_id
            )
            return [dict(row) for row in rows]
    
    async def create_message(self, content: str, sender: str, project_id: Optional[str] = None) -> dict:
        """Create a new message"""
        message_id = f"msg_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.utcnow()
        
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO messages (id, content, sender, project_id, timestamp) VALUES ($1, $2, $3, $4, $5)",
                message_id, content, sender, project_id, timestamp
            )
        
        return {
            "id": message_id,
            "content": content,
            "sender": sender,
            "project_id": project_id,
            "timestamp": timestamp.isoformat()
        }
    
    async def get_messages(self, project_id: Optional[str] = None) -> List[dict]:
        """Get messages, optionally filtered by project"""
        async with self.pool.acquire() as conn:
            if project_id:
                rows = await conn.fetch(
                    "SELECT id, content, sender, project_id, timestamp FROM messages WHERE project_id = $1 ORDER BY timestamp ASC",
                    project_id
                )
            else:
                rows = await conn.fetch(
                    "SELECT id, content, sender, project_id, timestamp FROM messages ORDER BY timestamp ASC"
                )
            return [dict(row) for row in rows]

# Global database instance
db = PostgresDB()

async def connect_db():
    """Connect to database"""
    await db.connect()

async def disconnect_db():
    """Disconnect from database"""
    await db.disconnect()
