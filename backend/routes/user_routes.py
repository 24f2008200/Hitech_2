from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from backend.app import db
from backend.models import Reservation, ParkingSpot, ParkingLot,User
from backend.routes.utils.auth import auth_required, admin_required, current_user

user_bp = Blueprint("user", __name__, url_prefix="/user")


# Book a spot
# Book a spot in a lot (auto-assigns first free spot)
@user_bp.route("/book", methods=["POST"])
@auth_required
def book_spot():
    user = current_user()
    data = request.json
    lot_id = data.get("lot_id")
    vehicle_number = data.get("vehicle_no")
    request_user_id = data.get("user_id")
    driver_name = data.get("driver_name")
    driver_contact = data.get("driver_contact")

    print(request_user_id, user.id)
    print(lot_id, vehicle_number)
    if not request_user_id or user.id != int(request_user_id):
        return jsonify({"error": "User ID is required"}), 400

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
        start_time=datetime.utcnow(),
        driver_name=driver_name,
        driver_contact=driver_contact
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
@user_bp.route("/release/<int:res_id>", methods=["POST"])
@auth_required
def release_spot(res_id):
    user = current_user()
    reservation = db.session.get(Reservation, int(res_id))

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
@user_bp.route("/reservations", methods=["GET"])
@auth_required
def reservations():
    user = current_user()
    reservations = Reservation.query.filter_by(user_id=user.id).all()

    result = []
    for r in reservations:
        result.append({
            "id": r.id,
            "lot_id": r.spot.label,
            "spot_id": r.spot_id,
            "vehicle_number": r.vehicle_number,
            "start_time": r.start_time,
            "end_time": r.end_time,
            "status": "active" if not r.end_time else "completed",
            "cost": r.parking_fee
        })

    return jsonify(result)
@user_bp.route("/lots", methods=["GET"])
@auth_required
def list_lots():
    pin_code = request.args.get("pin_code")
    if pin_code:
        lots = ParkingLot.query.filter_by(pin_code=pin_code).all()

        return jsonify([
            {
                "id": lot.id,
                "name": lot.name,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "price": lot.price,
                "number_of_spots": lot.number_of_spots,
                "available_spots": sum(1 for s in lot.spots if s.status == "A"),
            }
            for lot in lots
        ]), 200
    else:
        return jsonify({"error": "pin_code query parameter is required"}), 400
@user_bp.route("/pincodes", methods=["GET"])
@auth_required
def list_pin_codes():
    pin_codes = db.session.query(ParkingLot.pin_code).distinct().all()
    return jsonify([p[0] for p in pin_codes]), 200  

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        name=data.get("name"),
        email=data["email"],
        mobile=data.get("mobile"),
        address=data.get("address"),
        password=generate_password_hash(data["password"]),
        role=data.get("role", "user")
        
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
