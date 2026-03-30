# Movie Microservices System

Microservices-based Movie Streaming & Recommendation System using FastAPI and MongoDB

---

## User Service

The **User Service** is a microservice responsible for user management operations including authentication, user profiles, email verification, password management, and admin role management.

### Service Details
- **Language**: Python 3.12+
- **Framework**: FastAPI 0.104.1
- **Database**: MongoDB (mongodb+srv://admin:admin123@cluster0.ncxtapi.mongodb.net/movie_system)
- **Port**: 8001
- **API Documentation**: http://localhost:8001/docs (Swagger UI)

---

## Folder Structure

```
user service/
├── main.py                # FastAPI application and startup events
├── routes.py              # API endpoint routes (9 endpoints - CRUD + Auth + Admin)
├── models.py              # Pydantic data models for requests/responses
├── service.py             # Business logic layer
├── data_service.py        # Mock data service (legacy - for testing)
├── db.py                  # MongoDB connection and initialization
└── requirements.txt       # Python dependencies
```

### File Descriptions

#### main.py
- FastAPI application setup
- Route inclusion from routes.py
- MongoDB connection verification on startup
- Health check endpoint (`/health`)
- Root endpoint (`/`)

#### routes.py
- 9 API endpoints organized by feature:
  - **Authentication** (Register, Login, Reset Password)
  - **Email Verification** (Verify Email)
  - **User Profile (CRUD)** (Create, Read, Update, Delete)
  - **Admin Management** (Assign Roles, Get Admin Users)

#### models.py
- `UserRole` enum (USER, ADMIN)
- `UserStatus` enum (ACTIVE, INACTIVE, BLOCKED, PENDING_EMAIL_VERIFICATION)
- `UserPreferences` (language, theme, notifications, privacy)
- Request models (UserLogin, UserRegister, PasswordReset, EmailVerification)
- Response models (User, UserBlocking, RoleAssignment)

#### service.py
- Business logic layer
- Wraps UserMockDataService
- Methods for all CRUD and authentication operations
- Input validation and error handling

#### data_service.py
- Mock data for development/testing
- In-memory user storage
- All CRUD operations
- Password hashing (SHA256 - use bcrypt in production)
- Email/password reset token management

#### db.py
- MongoDB connection setup
- Database and collection initialization
- Connection error handling
- Uses credentials from environment or hardcoded string

#### requirements.txt
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation
- `pymongo==4.6.0` - MongoDB driver
- `httpx==0.25.1` - HTTP client
- `python-multipart==0.0.6` - Multipart form data
- `email-validator` - Email validation

---

## API Endpoints (CRUD)

### Authentication & Verification
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Create new user (CREATE) |
| POST | `/api/auth/login` | Login with email/password |
| POST | `/api/auth/reset-password` | Reset password with token |
| POST | `/api/auth/email-verification/verify` | Verify email with token |

### User Profile (CRUD)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/users/{user_id}` | Read user profile (READ) |
| PUT | `/api/users/{user_id}` | Update user profile (UPDATE) |
| DELETE | `/api/users/{user_id}` | Delete user account (DELETE) |

### Admin Management
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/admin/users/{user_id}/role` | Assign admin/user role |
| GET | `/api/admin/users/role/admin` | Get all admin users |

---

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Service
```bash
cd "user service"
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Access Documentation
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

---

## Database

- **Name**: movie_system
- **Collection**: users
- **Connection**: MongoDB Atlas (Cloud)
- **Credentials**: admin:admin123

### Example User Document
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "password_hash": "sha256_hash",
  "age": 25,
  "role": "user",
  "status": "active",
  "email_verified": true,
  "created_at": "2026-03-30T10:00:00",
  "updated_at": "2026-03-30T10:00:00",
  "last_login": "2026-03-30T12:00:00",
  "preferences": { ... }
}
```

---

## Features Implemented

✓ User Registration  
✓ User Login/Logout  
✓ Email Verification  
✓ Password Reset  
✓ User Profile Management (CRUD)  
✓ Account Activation/Deactivation  
✓ Role-Based Access Control (User/Admin)  
✓ MongoDB Integration  
✓ API Documentation (Swagger UI)  
✓ Health Check Monitoring  

---

## Architecture

```
HTTP Request
    ↓
[routes.py] - API Endpoints
    ↓
[service.py] - Business Logic
    ↓
[data_service.py] - Data Layer (Mock/Database)
    ↓
[db.py] - MongoDB Connection
    ↓
MongoDB Atlas
```

---

## Environment

- **OS**: Windows
- **Python**: 3.12.10
- **Virtual Environment**: .venv (Windows)
- **Port**: 8001 (While other microservices run on port 8000)

---

## Future Improvements

- Replace mock data with actual MongoDB operations
- Implement JWT authentication tokens
- Add bcrypt for password hashing
- Add rate limiting
- Add request logging
- Implement caching
- Add unit tests
- Add API authentication middleware

---

## Author
Millaniya L.A (IT22897312)
Github - LashAchinthka
it22897312@my.sliit.lk | lashanachinthka@gmail.com
User Service - Movie Microservice System

**Last Updated**: March 30, 2026
