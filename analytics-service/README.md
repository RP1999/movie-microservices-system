# 📊 9. Analytics Service (Member 6 - @dila)

## Simple Description
The **Analytics Service** is a dedicated microservice responsible for tracking in-depth system usage and generating comprehensive insights. It captures critical data like the most-watched movies, active system status, popular genres, and overall watch-time trends. This service empowers the administrative dashboard with real-time, aggregated analytical metrics (daily and weekly) essential for monitoring system health and business growth.

## Service Configuration
- **Port:** `8006`
- **Database:** MongoDB (Connected to `movie_system` on cluster0.ncxtapi.mongodb.net)
- **Framework:** FastAPI

---

## Main Features & API Endpoints (Exactly 5 CRUD Endpoints)

### 1. 📈 Track Most Watched Movies & Views (CREATE)
Records when a user fully watches a movie, updating system totals.
- **POST** `/analytics/movies` - Add new movie watch activity data.

### 2. 🎬 Get Most Watched Analytics (READ)
Retrieves the most watched movies sorted and paginated.
- **GET** `/analytics/movies` - Get a list of the most watched movies.

### 3. 📅 Comprehensive Dashboard & Reports (READ)
A unified endpoint that automatically generates daily/weekly reports, watch time statistics, tracks active user activity numbers, and analyzes popular genres for the dashboard.
- **GET** `/analytics/dashboard` - Fetches all calculated dashboard summary metrics.

### 4. ✏️ Correct Analytics Data (UPDATE)
Administrators can update invalid records for specific data if a bug occurs.
- **PUT** `/analytics/movies/{id}` - Manually update historical movie watch metrics.

### 5. 🗑️ Remove Invalid Data (DELETE)
Delete completely corrupt or testing records from the system's watch data.
- **DELETE** `/analytics/movies/{id}` - Permanently delete an analytics tracking record.

---

## 🚀 How to take your requested screenshots:

Your server is currently running locally! To grab the correct screenshots for your slides:

### 1. Native API Swagger UI Screenshot:
1. Open your browser and go directly to: **`http://localhost:8006/docs`**
2. You will instantly see the beautiful, interactive Swagger interface demonstrating perfectly 5 endpoints!
3. Take a screenshot of this page showing your 8006 service.

### 2. Function Run Port (Server Startup) Screenshot:
1. Open up a terminal windows in `d:\Analytics Service`.
2. Run `.\venv\Scripts\Activate.ps1`
3. Run `cd analytics_service` and run `uvicorn main:app --port 8006` 
4. Take a screenshot of the successful server start log showing `"Uvicorn running on http://127.0.0.1:8006"`!
