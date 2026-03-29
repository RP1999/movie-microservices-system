# 🎬 Watchlist Service

**Developed by IT22363848-Tennakoon I.M.S.R**

---

## 🎯 Purpose
The purpose of this service is to manage user personal lists through the following sub-functions:
- Add movie to watchlist
- Remove movie from watchlist
- Get user watchlist
- Mark/unmark favorite
- Clear watchlist
- Sort watchlist

---

## 🛠️ Technologies
-  **Backend Framework**: Python (FastAPI)
- **Database**: MongoDB (Atlas / Compass)
- **Database Driver**: Motor (Asyncio)

---

## 💡 Usefulness for Movie Streaming & Recommendation
1. Personalizes user content experience completely.
2. Tracks favorite movies effortlessly always.
3. Enhances personalized movie recommendations directly.
4. Helps users organize viewing history.
5. Provides data for personalized suggestions.

---


## 🌐 Base URLs

| Access Method | URL |
|---------------|-----|
| **Direct Access** | `http://localhost:8004` |
| **Via API Gateway** | `http://localhost:8000/watchlist` (after gateway integration) |



## 🚀 API Endpoints (CRUD)

### 🟢 CREATE
- `POST /api/watchlist/add` - Add To Watchlist
- `POST /api/watchlist/sort` - Sort Watchlist

### 🔵 READ
- `GET /api/watchlist/{user_id}` - Get Watchlist
- `GET /api/watchlist/check/{user_id}/{movie_id}` - Check In Watchlist
- `GET /api/watchlist/stats/{user_id}` - Get Stats
- `GET /` - Health Check
- `GET /db-status` - Db Status

### 🟡 UPDATE
- `PATCH /api/watchlist/favorite` - Mark Favorite
- `PATCH /api/watchlist/status` - Update Status

### 🔴 DELETE
- `DELETE /api/watchlist/remove` - Remove From Watchlist
- `DELETE /api/watchlist/clear/{user_id}` - Clear Watchlist

---

## 💻 How to Run (Step-by-Step)
1. Open your terminal in the `watchlist-service` directory.
   ```bash
   cd watchlist-service
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server specifically on port 8004 to connect with the API Gateway:
   ```bash
   python -m uvicorn app.main:app --port 8004 --reload
   ```
4. Access the interactive API documentation (Swagger UI) at:
   👉 **http://127.0.0.1:8004/docs**

---
