from flask import Blueprint, request, jsonify
from models import db, User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not (data and data.get("username") and data.get("email") and data.get("password")):
        return jsonify({"message": "Missing data"}), 400

    new_user = User(username=data["username"], email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username"), password=data.get("password")).first()
    if user:
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    return jsonify({"message": "Invalid credentials"}), 401
