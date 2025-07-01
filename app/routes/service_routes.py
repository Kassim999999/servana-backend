from flask import Blueprint, jsonify
from app.models import Service

service_bp = Blueprint("services", __name__)

@service_bp.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([s.serialize() for s in services])
