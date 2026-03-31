# Movie Catalog Service 🎬 (Shevin)

This is the **Movie Catalog** microservice for the Movie Streaming & Recommendation System assignment.

## 🗣️ What to say to your Lecturer  

Here is the exact pitch for your viva:

> *"Hi Professor! For this assignment, I built the **Movie Catalog Microservice**, which serves as the 'Source of Truth' for the system's movie library. I implemented a robust JSON API using FastAPI and MongoDB Atlas for high-performance metadata storage.*
> 
> *One of the key technical challenges I solved was building a **hybrid storage model**—storing structured metadata in MongoDB while handling binary file uploads for thumbnails and video streams. I also integrated advanced filtering and sorting logic, allowing users to search the catalog by title or category through our unified API Gateway on port `8000`."*

## 🧪 How to test all endpoints live

Make sure your services are running first (`./run_all.sh`).

**ENDPOINT 1: `GET /movies` (Get all movies)**
1. Open the API Gateway Swagger: `http://localhost:8000/docs`
2. Scroll to the **Movie Service** section and click **GET /movies**.
3. Click **Try it out** and then **Execute**.
4. Show the professor the list of movies currently in the database.

**ENDPOINT 2: `POST /movies` (Add a new movie)**
1. In the Gateway Swagger, open the **green POST box** for `/movies`.
2. Click **Try it out**.
3. Fill in the `title` and `category` fields.
4. (Optional) You can actually upload a real `.jpg` or `.mp4` file in the `thumbnail` or `movie_file` boxes to prove the hybrid storage works!
5. Click **Execute** and show them the `201 Created` response.

**ENDPOINT 3: `GET /movies/{movie_id}` (Get specific movie)**
1. Copy an `id` from the list in Endpoint 1.
2. In the Gateway Swagger, open the **blue GET box** for `/movies/{movie_id}`.
3. Paste the ID and click **Execute**.

**ENDPOINT 4: `DELETE /movies/{movie_id}` (Delete movie)**
1. Open the **red DELETE box** for `/movies/{movie_id}`.
2. Paste the ID and click **Execute**. Show them the "Movie deleted successfully" message.

**ENDPOINT 5: `GET /movies/system/health` (Health Check)**
1. Open the health check endpoint.
2. Show them the `status: ok` and confirm that the service and database are both live and healthy.
