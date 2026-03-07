from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "your_secret_key_here"
jwt = JWTManager(app)

# Database connection
db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12819216",
    password="43XhGZS8wA",
    database="sql12819216"
)

cursor = db.cursor()

# Helper function
def get_user_role(user_id):
    cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return user[0] if user else None

# ---------------- TEST ROUTES ----------------
@app.route("/login_test")
def login_test():
    return "LOGIN ROUTE EXISTS"

@app.route("/post_job_test")
def post_job_test():
    return "POST JOB ROUTE EXISTS"

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = data["password"].encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    role = data["role"]

    query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
    values = (name, email, hashed, role)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "User registered successfully"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"].encode("utf-8")

    query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password, user[3].encode("utf-8")):
        access_token = create_access_token(identity=str(user[0]))
        return jsonify({
            "message": "Login successful",
            "user_id": user[0],
            "name": user[1],
            "role": user[4],
            "token": access_token
        })
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# ---------------- POST JOB ----------------
@app.route("/post_job", methods=["POST"])
@jwt_required()
def post_job():
    current_user = get_jwt_identity()
    role = get_user_role(int(current_user))

    if role != "recruiter":
        return jsonify({"message": "Only recruiters can post jobs"}), 403

    data = request.get_json()
    title = data["title"]
    description = data["description"]
    company = data["company"]
    recruiter_id = data["recruiter_id"]

    query = """
        INSERT INTO jobs (title, description, company, recruiter_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (title, description, company, recruiter_id))
    db.commit()

    return jsonify({"message": "Job posted successfully"})

# ---------------- GET ALL JOBS ----------------
@app.route("/jobs", methods=["GET"])
def get_jobs():
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    job_list = []
    for job in jobs:
        job_list.append({
            "id": job[0],
            "title": job[1],
            "description": job[2],
            "company": job[3],
            "recruiter_id": job[4]
        })

    return jsonify({"jobs": job_list})

# ---------------- APPLY FOR JOB ----------------
@app.route("/apply", methods=["POST"])
@jwt_required()
def apply_job():
    current_user = get_jwt_identity()
    role = get_user_role(int(current_user))

    if role != "job_seeker":
        return jsonify({"message": "Only job seekers can apply for jobs"}), 403

    data = request.get_json()
    job_id = data["job_id"]
    applicant_id = data["applicant_id"]

    # Check if already applied
    cursor.execute("SELECT * FROM applications WHERE job_id=%s AND applicant_id=%s", (job_id, applicant_id))
    existing = cursor.fetchone()

    if existing:
        return jsonify({"message": "You have already applied for this job"}), 400

    cursor.execute("INSERT INTO applications (job_id, applicant_id) VALUES (%s, %s)", (job_id, applicant_id))
    db.commit()

    return jsonify({"message": "Application submitted successfully"})

# ---------------- GET APPLICATIONS ----------------
@app.route("/applications/<int:job_id>", methods=["GET"])
@jwt_required()
def get_applications(job_id):
    query = """
        SELECT applications.id, users.name, users.email, applications.applied_at
        FROM applications
        JOIN users ON applications.applicant_id = users.id
        WHERE applications.job_id = %s
    """
    cursor.execute(query, (job_id,))
    applications = cursor.fetchall()

    app_list = []
    for app in applications:
        app_list.append({
            "application_id": app[0],
            "applicant_name": app[1],
            "applicant_email": app[2],
            "applied_at": str(app[3])
        })

    return jsonify({"applications": app_list})

# ---------------- SEARCH JOBS ----------------
@app.route("/jobs/search", methods=["GET"])
def search_jobs():
    title = request.args.get("title", "")
    company = request.args.get("company", "")

    query = "SELECT * FROM jobs WHERE title LIKE %s AND company LIKE %s"
    values = (f"%{title}%", f"%{company}%")

    cursor.execute(query, values)
    jobs = cursor.fetchall()

    job_list = []
    for job in jobs:
        job_list.append({
            "id": job[0],
            "title": job[1],
            "description": job[2],
            "company": job[3],
            "recruiter_id": job[4]
        })

    return jsonify({"jobs": job_list})

# ---------------- DELETE JOB ----------------
@app.route("/jobs/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    current_user = get_jwt_identity()
    role = get_user_role(int(current_user))

    if role != "recruiter":
        return jsonify({"message": "Only recruiters can delete jobs"}), 403

    cursor.execute("DELETE FROM jobs WHERE id=%s AND recruiter_id=%s", (job_id, int(current_user)))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Job not found or not authorized"}), 404

    return jsonify({"message": "Job deleted successfully"})

# ---------------- UPDATE JOB ----------------
@app.route("/jobs/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    current_user = get_jwt_identity()
    role = get_user_role(int(current_user))

    if role != "recruiter":
        return jsonify({"message": "Only recruiters can update jobs"}), 403

    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    company = data.get("company")

    query = """
        UPDATE jobs 
        SET title=%s, description=%s, company=%s 
        WHERE id=%s AND recruiter_id=%s
    """
    cursor.execute(query, (title, description, company, job_id, int(current_user)))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Job not found or not authorized"}), 404

    return jsonify({"message": "Job updated successfully"})


# ---- THIS MUST ALWAYS BE AT THE VERY END ----
if __name__ == "__main__":
    app.run(debug=True)