# 💸 Expense Tracker

A full-stack web application to manage personal expenses with secure authentication and persistent storage.

## 🚀 Tech Stack

* **Frontend:** React (Vite)
* **Backend:** FastAPI (Python)
* **Database:** MongoDB
* **Auth:** JWT
* **Containerization:** Docker & Docker Compose

## ✨ Features

* User authentication (register & login)
* JWT-based protected routes
* Full CRUD for expenses
* Each user can only access their own data
* Clean and modular backend architecture
* Fully containerized environment

## 📸 Screenshots

(Add screenshots here)

## ▶️ Run with Docker

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

* Frontend: http://localhost:3000
* Backend: http://localhost:8000/health

## 🧪 Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🧠 Challenges & Learnings

* Resolved bcrypt compatibility issues with Python 3.12
* Fixed dependency conflicts between Motor and PyMongo
* Handled MongoDB datetime serialization correctly
* Built a clean backend architecture (routers, services, repositories)

## 📌 Future Improvements

* Add charts and analytics dashboard
* Export expenses (CSV/PDF)
* Deploy to cloud (Render / Vercel / MongoDB Atlas)
