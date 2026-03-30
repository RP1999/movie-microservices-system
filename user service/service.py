# user-service/service.py
from data_service import UserMockDataService
from models import UserLogin, UserRegister, UserUpdate, UserPreferences, UserRole, EmailVerification, PasswordReset, PasswordResetRequest
from typing import Optional, List, Dict, Any

class UserService:
    """Business logic service for user operations"""
    
    def __init__(self):
        self.data_service = UserMockDataService()
    
    # ================== USER REGISTRATION & LOGIN ==================
    
    def register_user(self, user_data: UserRegister) -> Dict[str, Any]:
        """
        Register a new user
        Returns: dict with success status and message
        """
        result = self.data_service.register_user(user_data)
        if result["success"]:
            # Generate and return email verification token
            email = user_data.email
            token = self.data_service.generate_email_verification_token(email)
            result["verification_token"] = token
            result["message"] = "Registration successful. Please verify your email."
        return result
    
    def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """
        Login user with email and password
        Returns: dict with success status, user_id, and role
        """
        return self.data_service.login_user(login_data.email, login_data.password)
    
    def logout_user(self, user_id: int) -> Dict[str, Any]:
        """
        Logout user (invalidate session)
        """
        return self.data_service.logout_user(user_id)
    
    # ================== EMAIL VERIFICATION ==================
    
    def send_email_verification(self, email: str) -> Dict[str, Any]:
        """
        Generate and send email verification token
        """
        user = self.data_service.get_user_by_email(email)
        if not user:
            return {"success": False, "error": "User not found"}
        
        token = self.data_service.generate_email_verification_token(email)
        return {
            "success": True,
            "email": email,
            "token": token,
            "message": "Verification email sent. Check your inbox."
        }
    
    def verify_email(self, email_verification: EmailVerification) -> Dict[str, Any]:
        """
        Verify user email with token
        """
        return self.data_service.verify_email(email_verification.email, email_verification.verification_token)
    
    # ================== PASSWORD MANAGEMENT ==================
    
    def request_password_reset(self, password_reset_request: PasswordResetRequest) -> Dict[str, Any]:
        """
        Request password reset - generates reset token
        """
        result = self.data_service.generate_password_reset_token(password_reset_request.email)
        if result["success"]:
            result["message"] = f"Password reset link sent to {password_reset_request.email}"
        return result
    
    def reset_password(self, password_reset: PasswordReset) -> Dict[str, Any]:
        """
        Reset user password with token
        Validates new password and confirm password match
        """
        if password_reset.new_password != password_reset.confirm_password:
            return {"success": False, "error": "Passwords do not match"}
        
        # Extract email from token (in production, token should be validated)
        # For now, we'll search for the token in password_reset_tokens
        email = None
        for e, token in self.data_service.password_reset_tokens.items():
            if token == password_reset.reset_token:
                email = e
                break
        
        if not email:
            return {"success": False, "error": "Invalid or expired reset token"}
        
        return self.data_service.reset_password(email, password_reset.reset_token, password_reset.new_password)
    
    # ================== USER PROFILE ==================
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        return self.data_service.get_all_users()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.data_service.get_user_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        return self.data_service.get_user_by_email(email)
    
    def update_user_profile(self, user_id: int, update_data: UserUpdate) -> Dict[str, Any]:
        """Update user profile (name, age, preferences)"""
        return self.data_service.update_user_profile(user_id, update_data)
    
    # ================== USER PREFERENCES ==================
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user's preferences"""
        return self.data_service.get_user_preferences(user_id)
    
    def update_user_preferences(self, user_id: int, preferences: UserPreferences) -> Dict[str, Any]:
        """Update user's preferences (language, theme, notifications, etc.)"""
        return self.data_service.update_user_preferences(user_id, preferences)
    
    # ================== ACCOUNT STATUS ==================
    
    def activate_account(self, user_id: int) -> Dict[str, Any]:
        """Activate user account"""
        return self.data_service.activate_account(user_id)
    
    def deactivate_account(self, user_id: int) -> Dict[str, Any]:
        """Deactivate user account"""
        return self.data_service.deactivate_account(user_id)
    
    # ================== USER BLOCKING ==================
    
    def block_user(self, user_id: int, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Block a user account (admin only)
        """
        return self.data_service.block_user(user_id, reason)
    
    def unblock_user(self, user_id: int) -> Dict[str, Any]:
        """
        Unblock a user account (admin only)
        """
        return self.data_service.unblock_user(user_id)
    
    # ================== ROLE MANAGEMENT ==================
    
    def assign_role(self, user_id: int, role: UserRole) -> Dict[str, Any]:
        """
        Assign role to user (admin only)
        """
        return self.data_service.assign_role(user_id, role)
    
    def get_admins(self) -> List[Dict[str, Any]]:
        """Get all admin users"""
        return self.data_service.get_users_by_role(UserRole.ADMIN)
    
    def get_regular_users(self) -> List[Dict[str, Any]]:
        """Get all regular users"""
        return self.data_service.get_users_by_role(UserRole.USER)
    
    # ================== UTILITY METHODS ==================
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        user = self.get_user_by_id(user_id)
        return user and user.get("role") == UserRole.ADMIN
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists by email"""
        return self.data_service.get_user_by_email(email) is not None
    
    def validate_login_credentials(self, email: str, password: str) -> bool:
        """Validate login credentials"""
        result = self.login_user(UserLogin(email=email, password=password))
        return result.get("success", False)