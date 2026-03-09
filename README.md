# 🏢 JobBoard — Full Stack Job Portal

A full stack job portal REST API built with **Flask** and **MySQL**, featuring secure authentication, role-based access control, and a modern frontend. Live and deployed on Render + Vercel.

🌐 **Live Demo:** [your-vercel-url.vercel.app](https://job-portal-frontend-puce-five.vercel.app/)  
⚙️ **API:** [job-portal-backend-a22d.onrender.com](https://job-portal-backend-a22d.onrender.com/jobs)

---

## 🚀 Features

- **User Authentication** — Register and login with JWT tokens
- **Password Security** — Passwords hashed using bcrypt (never stored as plain text)
- **Role-Based Access Control** — Separate permissions for Recruiters and Job Seekers
- **Job Management** — Recruiters can post, update, and delete job listings
- **Job Applications** — Job seekers can apply for jobs with duplicate prevention
- **Search & Filter** — Search jobs by title or company name
- **RESTful API** — Clean, well-structured API endpoints
- **Responsive Frontend** — Modern UI built with HTML, CSS, and JavaScript

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | MySQL |
| Authentication | JWT (Flask-JWT-Extended) |
| Password Hashing | bcrypt |
| Frontend | HTML, CSS, JavaScript |
| Backend Hosting | Render |
| Frontend Hosting | Vercel |
| Cloud Database | FreeSQLDatabase |

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register a new user | No |
| POST | `/login` | Login and get JWT token | No |

### Jobs
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/jobs` | Get all job listings | No |
| GET | `/jobs/search` | Search jobs by title/company | No |
| POST | `/post_job` | Post a new job | Yes (Recruiter) |
| PUT | `/jobs/<id>` | Update a job listing | Yes (Recruiter) |
| DELETE | `/jobs/<id>` | Delete a job listing | Yes (Recruiter) |

### Applications
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/apply` | Apply for a job | Yes (Job Seeker) |
| GET | `/applications/<job_id>` | Get all applicants for a job | Yes |

---

## ⚙️ Running Locally

### Prerequisites
- Python 3.x
- MySQL

### 1. Clone the repository
```bash
git clone https://github.com/vishall-n/job-portal-backend.git
cd job-portal-backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MySQL database
```sql
CREATE DATABASE job_portal;

USE job_portal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(50)
);

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    company VARCHAR(100),
    recruiter_id INT
);

CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    applicant_id INT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Update database credentials in `app.py`
```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="job_portal"
)
```

### 5. Run the server
```bash
python app.py
```

API will be running at `http://127.0.0.1:5000`

---

## 🔒 Security Features

- Passwords are **never stored as plain text** — bcrypt hashing with salt
- All sensitive routes are **protected with JWT tokens**
- **Role-based authorization** prevents job seekers from posting jobs and recruiters from applying
- Duplicate application prevention built in

---

## 📁 Project Structure

```
job-portal-backend/
├── app.py           # Main Flask application
├── requirements.txt # Python dependencies
├── index.html       # Frontend UI
└── README.md        # Project documentation
```

---

## 👨‍💻 Author

**Vishal**  
GitHub: [@vishall-n](https://github.com/vishall-n)
