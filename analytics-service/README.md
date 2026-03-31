# 📊 9. Analytics Service (Member 6 - @dilina)

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</div>

<br/>

## 📖 Simple Description

The **Analytics Service** is a highly-optimized, dedicated microservice responsible for tracking in-depth system usage and generating comprehensive insights. It captures critical data like the most-watched movies, active system status, popular genres, and overall watch-time trends. 

This service strictly empowers the administrative dashboard with real-time, aggregated analytical metrics perfectly suited for monitoring system health and business growth.

---

## ⚙️ Service Configuration

| System Property | Definition |
| --- | --- |
| **🔌 Service Port** | `8006` |
| **🗄️ Database Tier** | MongoDB Atlas Cloud (`movie_system` cluster) |
| **🏗️ API Framework** | FastAPI (Python Async) |

---

## ✨ Main Features & API Endpoints

This microservice perfectly utilizes a RESTful **5-Endpoint CRUD Architecture**:

### 1. 📈 Track Most Watched Movies & Views (CREATE)
Records when a user fully watches a movie, automatically updating system totals.
* **`POST /analytics/movies`** - Add new movie watch activity data.

### 2. 🎬 Get Most Watched Analytics (READ)
Retrieves the most watched movies sorted by popularity and paginated optimally.
* **`GET /analytics/movies`** - Get an array list of the most watched movies.

### 3. 📅 Comprehensive Dashboard & Reports (READ)
*A consolidated mega-endpoint!* Automatically generates daily/weekly reports, watch time statistics, tracks active user activity numbers, and analyzes popular genres dynamically into one single JSON response for the admin dashboard components.
* **`GET /analytics/dashboard`** - Fetches all calculated dashboard summary metrics.

### 4. ✏️ Correct Analytics Data (UPDATE)
Administrators can securely update historical system records for specific data if a bug occurs.
* **`PUT /analytics/movies/{id}`** - Manually correct historical movie watch metrics.

### 5. 🗑️ Remove Invalid Data (DELETE)
Delete completely corrupt, duplicate, or testing-level records securely from the system's watch data.
* **`DELETE /analytics/movies/{id}`** - Permanently erase an analytics tracking record.

---

## 🚀 Getting Started Locally

Getting the server running natively on your local machine is extremely simple:

1. **Activate the Virtual Environment (if applicable) & Navigate to the service folder:**
   ```bash
   cd analytics_service
   ```
2. **Start the FastAPI Uvicorn Server:**
   ```bash
   uvicorn main:app --port 8006
   ```
3. **Open the Auto-Generated Swagger Documentation:**
   Open your browser directly to [http://localhost:8006/docs](http://localhost:8006/docs) to access the interactive Swagger UI and test exactly all 5 of these endpoints live!
