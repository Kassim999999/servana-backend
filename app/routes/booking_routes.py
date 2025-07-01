from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from app.models import db, Booking, Service

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    service = Service.query.get(data["service_id"])
    if not service:
        return jsonify({"error": "Service not found"}), 404

    booking = Booking(
        service_id=service.id,
        name=data["name"],
        phone=data["phone"],
        date=data["date"],
        notes=data.get("notes", "")
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify(booking.serialize()), 201


@booking_bp.route("/bookings", methods=["GET"])
@jwt_required()
def all_bookings():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    if not user or not user.is_admin:
        return jsonify({"error": "Admins only"}), 403

    bookings = Booking.query.all()
    return jsonify([b.serialize() for b in bookings])



@booking_bp.route("/my-bookings", methods=["GET"])
@jwt_required()
def get_my_bookings():
    identity = get_jwt_identity()
    user_id = identity["id"]
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([b.serialize() for b in bookings])
