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
