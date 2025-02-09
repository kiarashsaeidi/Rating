### 📌 **Smart Rating System with Redis & Celery**  

🚀 **A Scalable Rating System for Django Applications**  

This project optimizes the way user ratings are handled in a Django application. Instead of writing ratings directly to the database, it **caches ratings in Redis** and updates them periodically using **Celery** to prevent sudden fluctuations and ensure a fair rating system.  

---

## 🛠 **Features**  

✅ **Optimized Rating System** – Prevents excessive database writes by caching ratings first.  
✅ **Batch Processing with Celery** – Ratings are saved in bulk at scheduled intervals.  
✅ **Decay Factor Implementation** – Prevents spam ratings from drastically changing a post’s score.  
✅ **Redis Caching** – Stores ratings temporarily before committing to the database.  
✅ **Scalable & Efficient** – Reduces load on the database and improves performance.  

---

## ⚙️ **Tech Stack**  

| Component    | Technology  |
|-------------|------------|
| Backend | Django & Django REST Framework |
| Database | PostgreSQL / SQLite |
| Cache    | Redis |
| Task Queue | Celery + Celery Beat |
| Containerization | Docker (Optional) |

---

## 🚀 **How It Works**  

### ✅ **Step 1: User Submits a Rating**  
A user submits a rating between **0 to 5** for a post.  

### ✅ **Step 2: Rating is Stored in Redis**  
Instead of immediately updating the database, the rating is **cached in Redis** for a short period.  

### ✅ **Step 3: Celery Processes Ratings in Batches**  
A **Celery task** runs periodically (e.g., every 5 minutes) to:  
- Retrieve cached ratings from Redis  
- Calculate the **weighted average** using a **decay factor**  
- Update the database in a single batch operation  

### ✅ **Step 4: Fair Rating Calculation**  
The decay factor ensures that **new ratings have a smaller immediate impact**, reducing spammy behavior.  

---
## 🎯 **API Endpoints**  

| Method | Endpoint | Description |
|--------|----------|------------|
| `POST` | `/api/posts/{id}/rate/` | Submit a new rating (0-5) |
| `GET`  | `/api/posts/` | Retrieve list of posts with average ratings |
