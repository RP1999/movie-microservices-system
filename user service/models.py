# user-service/models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """User role enumeration"""
    USER = "user"
    ADMIN = "admin"

class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    PENDING_EMAIL_VERIFICATION = "pending_email_verification"

class UserPreferences(BaseModel):
    """User preferences model"""
    preferred_language: Optional[str] = "en"
    theme: Optional[str] = "dark"
    notifications_email: Optional[bool] = True
    notifications_push: Optional[bool] = True
    email_on_new_release: Optional[bool] = True
    email_on_recommendations: Optional[bool] = True
    privacy_level: Optional[str] = "public"  # public, friends, private

class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserRegister(BaseModel):
    """User registration model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = None
    preferences: Optional[UserPreferences] = None

class PasswordResetRequest(BaseModel):
    """Password reset request model"""
    email: EmailStr

class PasswordReset(BaseModel):
    """Password reset model"""
    reset_token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """User profile update model"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = None
    preferences: Optional[UserPreferences] = None

class User(BaseModel):
    """User response model"""
    id: int
    name: str
    email: str
    age: Optional[int] = None
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    email_verified: bool = False
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    preferences: Optional[UserPreferences] = None
    
    class Config:
        from_attributes = True

class UserBlocking(BaseModel):
    """User blocking/unblocking model"""
    reason: Optional[str] = None
    duration: Optional[int] = None  # in days

class EmailVerification(BaseModel):
    """Email verification model"""
    email: EmailStr
    verification_token: str

class RoleAssignment(BaseModel):
    """Role assignment model"""
    user_id: int
    role: UserRole
    assigned_by: int  # Admin who assigned the role
    assigned_at: datetime = Field(default_factory=datetime.utcnow) 
