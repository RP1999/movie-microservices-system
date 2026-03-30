# user-service/service.py
from data_service import UserMockDataService
from models import UserLogin, UserRegister, UserUpdate, UserPreferences, UserRole, EmailVerification, PasswordReset, PasswordResetRequest
from typing import Optional, List, Dict, Any

class UserService:
    """Business logic service for user operations"""

    def __init__(self):
        self.data_service = UserMockDataService()

    def register_user(self, user_data: UserRegister) -> Dict[str, Any]:
        result = self.data_service.register_user(user_data)
        if result["success"]:
            token = self.data_service.generate_email_verification_token(user_data.email)
            result["verification_token"] = token
            result["message"] = "Registration successful. Please verify your email."
        return result

    def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        return self.data_service.login_user(login_data.email, login_data.password)

    def verify_email(self, email_verification: EmailVerification) -> Dict[str, Any]:
        return self.data_service.verify_email(email_verification.email, email_verification.verification_token)

    def reset_password(self, password_reset: PasswordReset) -> Dict[str, Any]:
        if password_reset.new_password != password_reset.confirm_password:
            return {"success": False, "error": "Passwords do not match"}
        email = None
        for e, token in self.data_service.password_reset_tokens.items():
            if token == password_reset.reset_token:
                email = e
                break
        if not email:
            return {"success": False, "error": "Invalid or expired reset token"}
        return self.data_service.reset_password(email, password_reset.reset_token, password_reset.new_password)

    def get_all_users(self) -> List[Dict[str, Any]]:
        return self.data_service.get_all_users()

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.data_service.get_user_by_id(user_id)

    def update_user_profile(self, user_id: int, update_data: UserUpdate) -> Dict[str, Any]:
        return self.data_service.update_user_profile(user_id, update_data)

    def deactivate_account(self, user_id: int) -> Dict[str, Any]:
        return self.data_service.deactivate_account(user_id)

    def assign_role(self, user_id: int, role: UserRole) -> Dict[str, Any]:
        return self.data_service.assign_role(user_id, role)

    def get_admins(self) -> List[Dict[str, Any]]:
        return self.data_service.get_users_by_role(UserRole.ADMIN)
