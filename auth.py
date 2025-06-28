from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from datetime import datetime
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if db.users.find_one({"username": username}):
        return {"error": "Username già esistente"}, 400

    hashed = generate_password_hash(password)
    user_id = db.users.insert_one({
        "username": username,
        "password": hashed,
        "data_registrazione": datetime.utcnow()
    }).inserted_id

    return {"message": "Utente registrato", "user_id": str(user_id)}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = db.users.find_one({"username": data.get("username")})
    if not user or not check_password_hash(user["password"], data.get("password")):
        return {"error": "Credenziali non valide"}, 401

    session["user_id"] = str(user["_id"])
    return {"message": "Login effettuato", "user_id": session["user_id"]}

@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return {"message": "Logout eseguito"}
