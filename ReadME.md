Rover Backend Development
---
# 🚀 Rover Backend Development

## 📌 Overview
Rover Backend Development merupakan salah satu bagian dari **Rover APP** yang berfungsi sebagai penyedia **RESTful API** menggunakan framework **FastAPI**.  
Backend ini dirancang agar mudah dikembangkan, cepat, dan scalable.

---

## ✨ Features
- 🔑 User Authentication & Authorization (JWT Token)
- 📊 Database integration dengan **PostgreSQL**
- 🤖 Object Detection dengan optimisasi aplikasi
- ⚡ FastAPI dengan auto-generated docs (Swagger & ReDoc)

---

## 📦 Project Structure
```sh
src/
├── models/      # ORM model untuk database
│   ├── posts.py
│   ├── result.py
│   ├── users.py
│   └── utils.py
│
├── routers/     # Routing / endpoint API
│   ├── posts.py
│   ├── results.py
│   ├── users.py
│   └── utils.py
│
├── schema/      # Pydantic schema (validasi request/response)
│   ├── posts.py
│   ├── results.py
│   └── users.py
│
├── settings/    # Konfigurasi utama
│   ├── config.py
│   └── db.py
│
└── main.py      # Entry point aplikasi
```

🛠️ Tech Stack

- Python 3.10+

- FastAPI

- SQLAlchemy

- Uvicorn

- PostgreSQL

- Pydantic

- OpenCV

- ONNX Runtime

⚙️ Installation & Setup

1️⃣ Clone Repository
```sh
git clone https://github.com/username/rover-backend.git
cd rover-backend
```

2️⃣ Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
4️⃣ Setup Environment

Buat file .env di root project.
Gunakan format berikut (lihat juga .env.example bila tersedia):

```sh
# Database connection
DATABASE_DEV="postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>"

# JWT Configuration
SECRET_KEY_JWT="<your_secret_key>"
ALGORITHM="<algorithm>"                  # contoh: HS256
ACCESS_TOKEN_EXPIRE_MINUTES="<minutes>"  # contoh: 10
```
⚠️ Note: Isi sesuai kebutuhan, jangan gunakan default value di production.

5️⃣ Run Server
```sh
uvicorn src.main:app --reload
```
