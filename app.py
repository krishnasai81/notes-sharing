from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from models import create_tables
import os

app = Flask(__name__, static_folder="build", static_url_path="")
CORS(app)

# Initialize DB
create_tables()

def get_db():
    return sqlite3.connect("database.db")

# ---------------- SERVE REACT ----------------
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password,role) VALUES (?,?,?)",
        (data['username'], data['password'], data['role'])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered"})

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data['username'], data['password'])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload_note():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes(title,content,author) VALUES (?,?,?)",
        (data['title'], data['content'], data['author'])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note uploaded"})

# ---------------- GET NOTES ----------------
@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    result = []
    for n in notes:
        result.append({
            "id": n[0],
            "title": n[1],
            "content": n[2],
            "author": n[3]
        })

    return jsonify(result)

# ---------------- SEARCH ----------------
@app.route("/search", methods=["GET"])
def search_notes():
    keyword = request.args.get("q")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    )

    notes = cursor.fetchall()
    conn.close()

    result = []
    for n in notes:
        result.append({
            "title": n[1],
            "content": n[2]
        })

    return jsonify(result)

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)