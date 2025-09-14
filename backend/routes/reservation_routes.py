from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.app import db
from backend.models import Reservation, ParkingSpot, ParkingLot
from backend.routes.utils.auth import auth_required, admin_required, current_user

reservation_bp = Blueprint("reservation", __name__, url_prefix="/reservation")


# Book a spot
# Book a spot in a lot (auto-assigns first free spot)
@reservation_bp.route("/book", methods=["POST"])
@auth_required
def book_spot():
    user = current_user()
    data = request.json
    lot_id = data.get("lot_id")
    vehicle_number = data.get("vehicle_number")

    if not lot_id or not vehicle_number:
        return jsonify({"error": "lot_id and vehicle_number are required"}), 400

    lot = db.session.get(ParkingLot, lot_id)
    if not lot:
        return jsonify({"error": "Invalid parking lot"}), 404

    # Find first available spot in lot
    spot = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").first()
    if not spot:
        return jsonify({"error": "No available spots in this lot"}), 400

    # Reserve spot
    reservation = Reservation(
        user_id=user.id,
        spot_id=spot.id,
        vehicle_number=vehicle_number,
        start_time=datetime.utcnow()
    )
    spot.status = "O"

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": "Spot booked successfully",
        "reservation_id": reservation.id,
        "lot_id": lot.id,
        "spot_id": spot.id
    })


# Release a spot
@reservation_bp.route("/release/<int:res_id>", methods=["POST"])
@auth_required
def release_spot(res_id):
    user = current_user()
    reservation = db.session.get(Reservation, res_id)

    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404
    if reservation.user_id != user.id and not user.is_admin:
        return jsonify({"error": "Unauthorized release attempt"}), 403
    if reservation.end_time:
        return jsonify({"error": "Spot already released"}), 400

    reservation.end_time = datetime.utcnow()
    reservation.spot.status = "A"

    # Calculate cost (duration * lot price)
    lot_price = reservation.spot.lot.price
    duration_hours = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    reservation.parking_fee = round(duration_hours * lot_price, 2)

    db.session.commit()

    return jsonify({
        "message": "Spot released successfully",
        "reservation_id": res_id,
        "spot_id": reservation.spot_id,
        "lot_id": reservation.spot.lot_id,
        "cost": reservation.parking_fee
    })


# View user’s reservations
@reservation_bp.route("/my", methods=["GET"])
@auth_required
def my_reservations():
    user = current_user()
    reservations = Reservation.query.filter_by(user_id=user.id).all()

    result = []
    for r in reservations:
        result.append({
            "id": r.id,
            "lot_id": r.spot.lot_id,
            "spot_id": r.spot_id,
            "vehicle_number": r.vehicle_number,
            "start_time": r.start_time,
            "end_time": r.end_time,
            "status": "active" if not r.end_time else "completed",
            "cost": r.parking_fee
        })

    return jsonify(result)
