# To-Do Kanban Board (Flask + Turso)

This is a To-Do application in Kanban board style.
Backend is built with **Python (Flask)** and uses **Turso (SQLite cloud)** as the database.

The backend is deployed on **Render (free tier)**, so it may go to sleep when inactive.
The first request may take some time to wake up.

###  Backend Test URL

```
https://todo-backend-m2zc.onrender.com
```

If the server is running, it will return:

```
Turso + Flask is working!
```

---

## Tech Stack

* Python
* Flask
* Turso (libSQL)
* Render (Deployment)

### Libraries

```
Flask==3.1.2
flask_cors==6.0.2
libsql_client==0.3.1
pydantic==2.12.5
python-dotenv==1.2.1
bcrypt
pytz==2025.2
email-validator
gunicorn
```

---

## Installation & Run (Local)

### 1. Clone the project

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
TURSO_DATABASE_URL=your_turso_url
TURSO_AUTH_TOKEN=your_turso_token
```

### 5. Run the server

```bash
python -m flask --app app.py run
```

Server will start at:

```
[http://localhost:5000](http://127.0.0.1:5000)
```

---

##  Notes

* This project uses Turso as cloud SQLite.
* Render free tier may sleep when idle, causing the first request to be slow.
* This backend supports a Kanban-style To-Do board (Todo / Doing / Done).
