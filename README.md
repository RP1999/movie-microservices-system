# movie-microservices-system
Microservices-based Movie Streaming &amp; Recommendation System


## 🚀 Review Service – How to Run

Follow these steps to set up and run the Review & Rating Service locally.

### 1. Navigate to Project Folder

```bash
cd movie-microservices-system
```

---

### 2. Create Virtual Environment (First Time Only)

```bash
python -m venv venv
```

---

### 3. Activate Virtual Environment

* **Windows:**

```bash
venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 4. Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

---

### 5. Configure Environment Variables

Create a `.env` file in the root folder and add:

```env
MONGO_URI=your_mongodb_atlas_uri_here
```


---

### 6. Run the Service

```bash
uvicorn app.main:app --reload --port 8005
```

---

### 7. Access API Documentation (Swagger UI)

Open in your browser:

```
http://localhost:8005/docs
```

---

## 🔁 Daily Run (After Initial Setup)

```bash
venv\Scripts\activate
uvicorn app.main:app --reload --port 8005
```

---

## ⚠️ Notes

* Default port: **8005**


* Ensure MongoDB Atlas IP whitelist allows your connection


---

## 📁 Project Structure

app/
 ├── main.py
 ├── database.py
 ├── models/
 │    └── review_model.py
 ├── schemas/
 │    └── review_schema.py
 ├── routes/
 │    └── review_routes.py
 ├── services/
 │    └── review_service.py
requirements.txt
.env.example
.gitignore

```
