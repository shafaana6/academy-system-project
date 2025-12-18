from flask import Flask
import os
import mysql.connector

app = Flask(__name__)

# Connect to the database using environment variables
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),       # e.g., localhost or your cloud DB host
    user=os.getenv("DB_USER"),       # your DB username
    password=os.getenv("DB_PASSWORD"),  # hidden password
    database=os.getenv("DB_NAME")    # your database name
)

# Define the home page route
@app.route("/")
def home():
    return "Academy System is Live!"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
