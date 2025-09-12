from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.app import db
from backend.models import Reservation, ParkingSpot

reservation_bp = Blueprint("reservation", __name__, url_prefix="/reservation")


# Book a spot
@reservation_bp.route("/book", methods=["POST"])
def book_spot():
    data = request.json
    spot = ParkingSpot.query.filter_by(lot_id=data["lot_id"], status="A").first()

    if not spot:
        return jsonify({"error": "No available spots"}), 400

    reservation = Reservation(
        spot_id=spot.id,
        user_id=data["user_id"],
        start_ts=datetime.utcnow()
    )
    spot.status = "O"
    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Spot booked", "reservation_id": reservation.id})


# Release a spot
@reservation_bp.route("/release/<int:res_id>", methods=["POST"])
def release_spot(res_id):
    reservation = Reservation.query.get(res_id)
    if not reservation or not reservation.active:
        return jsonify({"error": "Reservation not found or inactive"}), 404

    end_time = datetime.utcnow()
    duration = (end_time - reservation.start_ts).total_seconds() / 3600
    cost = duration * reservation.spot.lot.price_per_hour

    reservation.end_reservation(end_time, cost)
    reservation.spot.status = "A"

    db.session.commit()
    return jsonify({"message": "Spot released", "cost": cost})
