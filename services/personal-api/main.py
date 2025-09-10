#!/usr/bin/env python3
# Personal API - Main Application

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from jose import jwt
import os
from passlib.context import CryptContext

# Initialize FastAPI app
app = FastAPI(
    title="Personal API",
    description="Unified interface for personal data and automation",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class DataSummary(BaseModel):
    total_services: int
    last_sync: datetime
    data_points: int
    automations_active: int

class ServiceStatus(BaseModel):
    name: str
    status: str
    last_sync: Optional[datetime]
    data_count: int

# Demo database
fake_users_db = {
    "demo": {
        "username": "demo",
        "full_name": "Demo User",
        "email": "demo@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.get("/")
async def root():
    return {
        "message": "Personal API",
        "version": "0.1.0",
        "status": "operational",
        "timestamp": datetime.now()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "uptime": "2 days, 3:45:22"
    }

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/profile", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/data/summary", response_model=DataSummary)
async def get_data_summary(current_user: User = Depends(get_current_user)):
    return DataSummary(
        total_services=7,
        last_sync=datetime.now() - timedelta(hours=2),
        data_points=15234,
        automations_active=3
    )

@app.get("/services/list", response_model=List[ServiceStatus])
async def list_services(current_user: User = Depends(get_current_user)):
    return [
        ServiceStatus(
            name="GitHub",
            status="connected",
            last_sync=datetime.now() - timedelta(hours=1),
            data_count=523
        ),
        ServiceStatus(
            name="Google Calendar",
            status="connected",
            last_sync=datetime.now() - timedelta(minutes=30),
            data_count=145
        ),
        ServiceStatus(
            name="Notion",
            status="syncing",
            last_sync=datetime.now() - timedelta(hours=3),
            data_count=892
        ),
    ]

@app.post("/automation/trigger/{automation_id}")
async def trigger_automation(
    automation_id: str,
    current_user: User = Depends(get_current_user)
):
    return {
        "automation_id": automation_id,
        "status": "triggered",
        "timestamp": datetime.now(),
        "message": f"Automation {automation_id} has been triggered successfully"
    }

@app.get("/analytics/insights")
async def get_insights(current_user: User = Depends(get_current_user)):
    return {
        "productivity_score": 85,
        "most_active_day": "Tuesday",
        "focus_time_today": "5h 23m",
        "tasks_completed_this_week": 34,
        "trending_topics": ["AI", "System Design", "Health"],
        "recommendations": [
            "Consider taking a break - you've been active for 3 hours",
            "Your most productive time is 9-11 AM",
            "You have 3 pending reviews"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
