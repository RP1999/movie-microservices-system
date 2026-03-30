# user-service/routes.py
from fastapi import APIRouter, HTTPException, status
from models import (
    UserLogin, UserRegister, UserUpdate, PasswordReset,
    EmailVerification, UserRole
)
from service import UserService
from typing import Dict, Any

# Create router
router = APIRouter(prefix="/api", tags=["user-service"])

# Initialize service
user_service = UserService()

# ================== AUTHENTICATION ==================

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister) -> Dict[str, Any]:
    """CREATE: Register a new user"""
    result = user_service.register_user(user_data)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/auth/login")
def login_user(login_data: UserLogin) -> Dict[str, Any]:
    """LOGIN: Authenticate user with email and password"""
    result = user_service.login_user(login_data)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@router.post("/auth/reset-password")
def reset_password(password_reset: PasswordReset) -> Dict[str, Any]:
    """Reset password with token"""
    result = user_service.reset_password(password_reset)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ================== EMAIL VERIFICATION ==================

@router.post("/auth/email-verification/verify")
def verify_email(verification_data: EmailVerification) -> Dict[str, Any]:
    """Verify user email with token"""
    result = user_service.verify_email(verification_data)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ================== USER PROFILE (CRUD) ==================

@router.get("/users/{user_id}")
def get_user(user_id: int) -> Dict[str, Any]:
    """READ: Get user by ID"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}")
def update_user_profile(user_id: int, update_data: UserUpdate) -> Dict[str, Any]:
    """UPDATE: Update user profile"""
    result = user_service.update_user_profile(user_id, update_data)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_account(user_id: int) -> Dict[str, Any]:
    """DELETE: Delete user account"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Mark user as deleted or remove from database
    # For now, we can deactivate the account instead
    result = user_service.deactivate_account(user_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Account deleted successfully", "user_id": user_id}

# ================== ROLE MANAGEMENT ==================

@router.post("/admin/users/{user_id}/role")
def assign_role(user_id: int, role: UserRole) -> Dict[str, Any]:
    """ADMIN: Assign role to user"""
    result = user_service.assign_role(user_id, role)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/admin/users/role/admin")
def get_admin_users() -> Dict[str, Any]:
    """ADMIN: Get all admin users"""
    return {"admins": user_service.get_admins()}
