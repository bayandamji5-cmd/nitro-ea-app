from flask import Flask, request, jsonify
import uuid
import hashlib

app = Flask(__name__)

# In-memory "database"
users = {}  # username: {password_hash, license_key}
licenses = {}  # license_key: username

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    
    password_hash = hash_password(password)
    license_key = str(uuid.uuid4())  # generate unique license key
    
    users[username] = {
        "password_hash": password_hash,
        "license_key": license_key
    }
    
    licenses[license_key] = username
    
    return jsonify({"message": "User registered", "license_key": license_key})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    user = users.get(username)
    if not user or user["password_hash"] != hash_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Return the license key on successful login
    return jsonify({"license_key": user["license_key"]})

@app.route("/validate_license", methods=["POST"])
def validate_license():
    data = request.json
    license_key = data.get("license_key")
    
    if license_key in licenses:
        return jsonify({"status": "valid", "user": licenses[license_key]})
    else:
        return jsonify({"status": "invalid"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)