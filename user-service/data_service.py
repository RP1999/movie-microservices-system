# user-service/data_service.py
from models import User, UserRole, UserStatus, UserPreferences
from datetime import datetime
from typing import Optional, List
import hashlib

class UserMockDataService:
    """Mock data service for user operations - for development/testing"""

    def __init__(self):
        self.users = [
            {
                "id": 1,
                "name": "Admin User",
                "email": "admin@moviestream.com",
                "password_hash": self._hash_password("Admin@123"),
                "age": 30,
                "role": UserRole.ADMIN,
                "status": UserStatus.ACTIVE,
                "email_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": datetime.utcnow(),
                "preferences": UserPreferences(),
            },
            {
                "id": 2,
                "name": "John Doe",
                "email": "john@example.com",
                "password_hash": self._hash_password("John@123"),
                "age": 25,
                "role": UserRole.USER,
                "status": UserStatus.ACTIVE,
                "email_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": None,
                "preferences": UserPreferences(),
            },
        ]
        self.next_id = 3
        self.email_verification_tokens = {}
        self.password_reset_tokens = {}
        self.blocked_users_log = []

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        return self._hash_password(password) == password_hash

    def register_user(self, user_data) -> dict:
        if self.get_user_by_email(user_data.email):
            return {"success": False, "error": "Email already registered"}
        new_user = {
            "id": self.next_id,
            "name": user_data.name,
            "email": user_data.email,
            "password_hash": self._hash_password(user_data.password),
            "age": user_data.age,
            "role": UserRole.USER,
            "status": UserStatus.PENDING_EMAIL_VERIFICATION,
            "email_verified": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None,
            "preferences": user_data.preferences or UserPreferences(),
        }
        self.users.append(new_user)
        self.next_id += 1
        return {"success": True, "user_id": new_user["id"], "message": "User registered. Please verify email."}

    def login_user(self, email: str, password: str) -> dict:
        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "error": "User not found"}
        if user["status"] == UserStatus.BLOCKED:
            return {"success": False, "error": "User account is blocked"}
        if not user["email_verified"]:
            return {"success": False, "error": "Please verify your email first"}
        if not self._verify_password(password, user["password_hash"]):
            return {"success": False, "error": "Invalid password"}
        user["last_login"] = datetime.utcnow()
        return {"success": True, "user_id": user["id"], "role": user["role"]}

    def generate_email_verification_token(self, email: str) -> str:
        token = hashlib.sha256(f"{email}{datetime.utcnow()}".encode()).hexdigest()
        self.email_verification_tokens[email] = token
        return token

    def verify_email(self, email: str, token: str) -> dict:
        if self.email_verification_tokens.get(email) != token:
            return {"success": False, "error": "Invalid verification token"}
        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "error": "User not found"}
        user["email_verified"] = True
        user["status"] = UserStatus.ACTIVE
        user["updated_at"] = datetime.utcnow()
        del self.email_verification_tokens[email]
        return {"success": True, "message": "Email verified successfully"}

    def generate_password_reset_token(self, email: str) -> dict:
        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "error": "User not found"}
        token = hashlib.sha256(f"{email}{datetime.utcnow()}".encode()).hexdigest()
        self.password_reset_tokens[email] = token
        return {"success": True, "token": token, "message": "Reset token generated"}

    def reset_password(self, email: str, token: str, new_password: str) -> dict:
        if self.password_reset_tokens.get(email) != token:
            return {"success": False, "error": "Invalid or expired reset token"}
        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "error": "User not found"}
        user["password_hash"] = self._hash_password(new_password)
        user["updated_at"] = datetime.utcnow()
        del self.password_reset_tokens[email]
        return {"success": True, "message": "Password reset successfully"}

    def get_all_users(self) -> List[dict]:
        return self.users

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        return next((u for u in self.users if u["id"] == user_id), None)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return next((u for u in self.users if u["email"] == email), None)

    def update_user_profile(self, user_id: int, update_data) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            if value is not None:
                user[key] = value
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "user_id": user["id"]}

    def update_user_preferences(self, user_id: int, preferences) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        user["preferences"] = preferences
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "message": "Preferences updated"}

    def get_user_preferences(self, user_id: int) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        return {"success": True, "preferences": user["preferences"]}

    def activate_account(self, user_id: int) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        user["status"] = UserStatus.ACTIVE
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "message": "Account activated"}

    def deactivate_account(self, user_id: int) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        user["status"] = UserStatus.INACTIVE
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "message": "Account deactivated"}

    def block_user(self, user_id: int, reason: str = None) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        user["status"] = UserStatus.BLOCKED
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "message": "User blocked"}

    def unblock_user(self, user_id: int) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        user["status"] = UserStatus.ACTIVE
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "message": "User unblocked"}

    def assign_role(self, user_id: int, new_role: UserRole) -> dict:
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        user["role"] = new_role
        user["updated_at"] = datetime.utcnow()
        return {"success": True, "message": f"Role updated to {new_role}"}

    def get_users_by_role(self, role: UserRole) -> List[dict]:
        return [u for u in self.users if u["role"] == role]
