# Analytics & Reporting Service 📊 (Dilina)

This is the **Analytics** microservice for the Movie Streaming & Recommendation System assignment.

## 🗣️ What to say to your Lecturer  

Here is the exact pitch for your viva:

> *"Hi Professor! I was responsible for the **Analytics and Reporting Microservice**. While other services focus on raw data, my service is the 'brain' that turns usage data into actionable business intelligence.*
> 
> *I implemented high-speed tracking endpoints to record movie watch activity and utilized **MongoDB Aggregation Pipelines** to generate real-time reports on popular genres and total watch time. My service provides a 'Dashboard' view that would normally be used by business admins and is fully accessible through our API Gateway on port `8000`."*

## 🧪 How to test all endpoints live

Make sure your services are running first (`./run_all.sh`).

**ENDPOINT 1: `GET /analytics/dashboard` (Live Dashboard Report)**
1. Open the API Gateway Swagger: `http://localhost:8000/docs`
2. Scroll to the **Analytics Service** section and click **GET /analytics/dashboard**.
3. Click **Try it out** and then **Execute**.
4. Show the professor the **"Live System Dashboard"** report, which aggregates data from across the system (Revenue, Health, Genre Popularity).

**ENDPOINT 2: `POST /analytics/movies` (Track a Watch Event)**
1. In the Gateway Swagger, open the **green POST box** for `/analytics/movies`.
2. Click **Try it out**.
3. Paste this JSON:
   ```json
   {
     "movie_id": "M123",
     "title": "Interstellar",
     "genre": "Sci-Fi",
     "watch_count": 1,
     "total_watch_time_minutes": 160
   }
   ```
4. Click **Execute**. This proves the service can actively "listen" to and record system activities.

**ENDPOINT 3: `GET /analytics/movies` (Most Watched Movies)**
1. Open the **blue GET box** for `/analytics/movies`.
2. Click **Execute**. This shows the sorted list of movies based on their watch popularity—effectively proving the analytics logic works!

**ENDPOINT 4: `DELETE /analytics/movies/{id}` (Data Maintenance)**
1. Open the **red DELETE box** for `/analytics/movies/{id}`.
2. Provide an ID to show how bad or invalid analytics data can be cleaned from the system.
