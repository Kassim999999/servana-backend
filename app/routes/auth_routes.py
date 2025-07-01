from flask import Blueprint, request, jsonify
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify(msg="User already exists"), 409
    hashed_pw = generate_password_hash(data["password"])
    user = User(full_name=data["full_name"], email=data["email"], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="Registered successfully"), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify(msg="Invalid credentials"), 401
    token = create_access_token(identity={"id": user.id, "email": user.email})
    return jsonify(token=token, user={"id": user.id, "name": user.full_name}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    identity = get_jwt_identity()
    return jsonify(identity), 200
