# user-service/models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    PENDING_EMAIL_VERIFICATION = "pending_email_verification"

class UserPreferences(BaseModel):
    preferred_language: Optional[str] = "en"
    theme: Optional[str] = "dark"
    notifications_email: Optional[bool] = True
    notifications_push: Optional[bool] = True
    email_on_new_release: Optional[bool] = True
    email_on_recommendations: Optional[bool] = True
    privacy_level: Optional[str] = "public"

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = None
    preferences: Optional[UserPreferences] = None

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    reset_token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = None
    preferences: Optional[UserPreferences] = None

class User(BaseModel):
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
    reason: Optional[str] = None
    duration: Optional[int] = None

class EmailVerification(BaseModel):
    email: EmailStr
    verification_token: str

class RoleAssignment(BaseModel):
    user_id: int
    role: UserRole
    assigned_by: int
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
