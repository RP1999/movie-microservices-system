# Streaming Service 🎬

This is the **Streaming** microservice for the Movie Streaming & Recommendation System assignment.

## 🗣️ What to say to your Lecturer  

Here is the exact pitch you can tell your lecturer when they ask what you did:

> *"Hi Professor! For this assignment, I designed and built the **Streaming Microservice**, utilizing the FastAPI framework and a MongoDB Atlas NoSQL database. My service is responsible for handling the core functionality of delivering movie streams to the user and managing their lifetime watch history.*
> 
> *Instead of relying on basic query parameters, I implemented **Pydantic data models** to ensure robust JSON data validation on all of our endpoints, catching bad requests before they ever hit the database. I also ensured all my MongoDB credentials were secure by extracting them into environment variables.*
> 
> *Finally, I integrated my service with the team's API Gateway on port `8000`. As you can see natively, my service runs safely isolated on port `8003`, but all user traffic is successfully routed through the Gateway, fulfilling the port-hiding requirement."*

## 🧪 How to test all endpoints live

If your lecturer asks you to prove it works live, you can easily do it using your Swagger documentation! Make sure your services are running first (`./run_all.sh`).

**ENDPOINT 1: `GET /stream/{movie_id}` (Testing the stream logic)**
1. Open the API Gateway Swagger: `http://localhost:8000/docs`
2. Scroll to the **blue GET box** at the bottom and click **Try it out**.
3. Set `service_name` to `streaming` and `path` to `stream/M123`.
4. Click **Execute** and show them the `200 OK` JSON response containing the stream URL.

**ENDPOINT 2: `POST /watch` (Testing the database writing)**
_This proves you can successfully "write" data into the MongoDB database._
1. From the same Gateway Swagger, open the **green POST box**.
2. Click **Try it out**.
3. Set `service_name` to `streaming` and `path` to `watch`.
4. Inside the `Request body` box, clear whatever is there and paste this exact JSON:
   ```json
   {
     "user_id": "U999",
     "movie_id": "M123"
   }
   ```
5. Click **Execute** and show them the `201 Created` JSON response confirming it was saved!

**ENDPOINT 3: `GET /watch/{user_id}` (Testing database reading)**
_This proves you can successfully "read" data out of the MongoDB database._
1. From the same Gateway Swagger, open the **blue GET box**.
2. Click **Try it out**.
3. Set `service_name` to `streaming` and `path` to `watch/U999` (using the same user ID we just created).
4. Click **Execute** and show them the `200 OK` JSON response that prints out the watch history array!

**ENDPOINT 4: `PUT /watch/progress` (Testing the database updating)**
_This proves you can successfully "update" existing data in MongoDB._
1. From the Gateway Swagger, open the **orange PUT box**.
2. Click **Try it out**.
3. Set `service_name` to `streaming` and `path` to `watch/progress`.
4. Inside the `Request body` box, clear it and paste this JSON:
   ```json
   {
     "user_id": "U999",
     "movie_id": "M123",
     "progress_minutes": 45
   }
   ```
5. Click **Execute** and show them the `200 OK` JSON response. You can then run Endpoint 3 again to show them the new `progress_minutes` variable is saved in the record!

**ENDPOINT 5: `DELETE /watch/{user_id}` (Testing full history deletion)**
_This proves you can successfully "destroy" all data for a specific user._
1. From the Gateway Swagger, open the **red DELETE box**.
2. Click **Try it out**.
3. Set `path` to `streaming/watch/U999`.
4. Click **Execute** and show them the `200 OK` JSON response confirming the deletion.

**ENDPOINT 6: `DELETE /watch/{user_id}/{movie_id}` (Testing specific movie deletion)**
_This is the "Netflix-style" remove feature. It proves you can perform precise deletions._
1. From the Gateway Swagger, open the **red DELETE box**.
2. Click **Try it out**.
3. Set `path` to `streaming/watch/U999/M123`.
4. Click **Execute** and show them the `200 OK` JSON response. If you run Endpoint 3 again, that specific movie will be gone, but other movies for that user would still be there!
