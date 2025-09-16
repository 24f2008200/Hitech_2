from flask import Blueprint, request, jsonify
from sqlalchemy import func
from backend.app import db
from backend.models import ParkingLot, ParkingSpot, Reservation, User
from backend.routes.utils.auth import auth_required , admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Create parking lot
@admin_bp.route("/lots", methods=["POST"])
@admin_required
def create_lot():
    data = request.json
    lot = ParkingLot(
        name=data["name"],
        price=data["price"],
        address=data.get("address"),
        pin_code=data.get("pin_code"),
        number_of_spots=data.get("number_of_spots", 0),
    )
    db.session.add(lot)
    db.session.commit()

    # Create spots
    for i in range(lot.number_of_spots):
        spot = ParkingSpot(lot_id=lot.id, label=f"Spot-{i+1}")
        db.session.add(spot)
    db.session.commit()

    return jsonify({"message": "Parking lot created", "id": lot.id}), 201

# Get all parking lots with their spots
@admin_bp.route("/lots", methods=["GET"])
@admin_required
def list_lots():
    lots = ParkingLot.query.all()
    return jsonify([
        {
            "id": lot.id,
            "name": lot.name,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "price": lot.price,
            "number_of_spots": lot.number_of_spots,
            "available_spots": sum(1 for s in lot.spots if s.status == "A"),
            "occupied_spots": sum(1 for s in lot.spots if s.status == "O"),
            "spots": [
                spot.get_details
                for spot in lot.spots
            ]
        }
        for lot in lots
    ]), 200

# View all users
@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "name": u.name} for u in users])


    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    occupied = ParkingSpot.query.filter_by(is_occupied=True).count()
    free = total_spots - occupied
    revenue = db.session.query(db.func.sum(Reservation.cost)).scalar() or 0

    return jsonify({
        "total_lots": total_lots,
        "total_spots": total_spots,
        "occupied_spots": occupied,
        "free_spots": free,
        "revenue": revenue
    })

@admin_bp.route("/search", methods=["GET"])
@admin_required
def search_users():
    current_user = admin_required()
    if isinstance(current_user, tuple):
        return current_user

    query = request.args.get("query", "").strip()
    if not query:
        return jsonify([])

    results = User.query.filter(
        (User.email.ilike(f"%{query}%")) |
        (User.phone.ilike(f"%{query}%")) |
        (User.name.ilike(f"%{query}%"))
    ).all()

    return jsonify([
        {"id": u.id, "email": u.email, "phone": u.phone, "name": u.name}
        for u in results
    ])


# Update parking lot
@admin_bp.route("/lots/<int:lot_id>", methods=["PUT"])
@admin_required
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    lot.name = data.get("name", lot.name)
    lot.price = data.get("price", lot.price)
    lot.address = data.get("address", lot.address)
    lot.pin_code = data.get("pin_code", lot.pin_code)

    # Adjust number of spots if changed
    new_spot_count = data.get("number_of_spots", lot.number_of_spots)
    if new_spot_count > lot.number_of_spots:
        # Add new spots
        for i in range(lot.number_of_spots, new_spot_count):
            spot = ParkingSpot(lot_id=lot.id, status="A", label=f"Spot-{i+1}")
            db.session.add(spot)
    elif new_spot_count < lot.number_of_spots:
        # Remove extra spots (only if available)
        removable = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").all()
        to_remove = lot.number_of_spots - new_spot_count
        if len(removable) < to_remove:
            return jsonify({"error": "Not enough available spots to remove"}), 400
        for spot in removable[:to_remove]:
            db.session.delete(spot)

    lot.number_of_spots = new_spot_count
    db.session.commit()

    return jsonify({"message": "Parking lot updated"}), 200

# Delete parking lot
@admin_bp.route("/lots/<int:lot_id>", methods=["DELETE"])
@admin_required
def delete_parking_lot(lot_id):
    lot = db.session.get(ParkingLot, lot_id)
    if not lot:
        return jsonify({"error": "Lot not found"}), 404

    if ParkingSpot.query.filter_by(lot_id=lot.id, status="O").count() > 0:
        return jsonify({"error": "Cannot delete lot with active spots"}), 400

    db.session.delete(lot)
    db.session.commit()
    return jsonify({"message": "Lot deleted"}), 200



@admin_bp.route("/summary", methods=["GET"])
@admin_required
def summary():
    total_users = User.query.count()
    # blocked_users = User.query.filter_by(is_blocked=True).count()

    # Example: total active reservations
    from backend.models import Reservation, ParkingLot

    active_reservations = Reservation.query.filter(
        Reservation.end_time == None
    ).count()

    lots = ParkingLot.query.count()

    # Revenue by month
    revenue = db.session.query(
        func.strftime("%Y-%m", Reservation.start_time).label("month"),
        func.sum(Reservation.parking_fee).label("total")
    ).group_by("month").all()

    revenue_data = [{"month": r[0], "amount": float(r[1] or 0)} for r in revenue]

    return jsonify({
        "total_users": total_users,
        # "blocked_users": blocked_users,
        "active_reservations": active_reservations,
        "lots": lots,
        "revenue": revenue_data
    })

@admin_bp.route("/reservations", methods=["GET"])
@admin_required
def list_reservations():
    reservations = Reservation.query.all()
    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "spot_id": r.spot_id,
            "lot_id": r.lot_id,
            "vehicle_number": r.vehicle_number,
            "start_time": r.start_time,
            "end_time": r.end_time,
            "cost": r.cost,
        }
        for r in reservations
    ])

