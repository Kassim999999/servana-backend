from flask import Blueprint, request, jsonify
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify(msg="User already exists"), 409
    hashed = generate_password_hash(data["password"])
    new_user = User(
        full_name=data["full_name"],
        email=data["email"],
        password=hashed,
        is_admin=data.get("is_admin", False),
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg="User created successfully"), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        token = create_access_token(identity={"id": user.id, "is_admin": user.is_admin})
        return jsonify(token=token)
    return jsonify(msg="Invalid credentials"), 401

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(user=current_user)
