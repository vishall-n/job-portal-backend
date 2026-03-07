import mysql.connector

db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12819216",
    password="43XhGZS8wA",
    database="sql12819216"
)

cursor = db.cursor()

print("Database connected successfully")
