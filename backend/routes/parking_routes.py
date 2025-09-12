from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import ParkingLot, ParkingSpot, Reservation, User
from backend.utils.auth import auth_required , admin_required

parking_bp = Blueprint("parking", __name__, url_prefix="/parking")


# Create parking lot
@parking_bp.route("/lots", methods=["POST"])
@auth_required
@admin_required
def create_lot():
    data = request.json
    lot = ParkingLot(
        prime_location_name=data["prime_location_name"],
        price_per_hour=data["price_per_hour"],
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



@parking_bp.route("/dashboard", methods=["GET"])
@auth_required
@admin_required
def view_dashboard():
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        spots = lot.spots
        spots_data = [
            {
                "id": spot.id,
                "label": spot.label,
                "status": spot.status  # 'A' or 'O'
            }
            for spot in spots
        ]
        result.append({
            "lot_id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price_per_hour": lot.price_per_hour,
            "total_spots": len(spots),
            "available_spots": sum(1 for s in spots if s.status == "A"),
            "occupied_spots": sum(1 for s in spots if s.status == "O"),
            "spots": spots_data
        })
    return jsonify(result), 200

# View all users
@parking_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "name": u.name} for u in users])


# Summary data
@parking_bp.route("/summary", methods=["GET"])
@admin_required
def summary():
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



# Update parking lot
@parking_bp.route("/lots/<int:lot_id>", methods=["PUT"])
@auth_required
@admin_required
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
    lot.price_per_hour = data.get("price_per_hour", lot.price_per_hour)
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
@parking_bp.route("/lots/<int:lot_id>", methods=["DELETE"])
@auth_required
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

# List parking lots
@parking_bp.route("/lots", methods=["GET"])
@auth_required
def list_lots():
    lots = ParkingLot.query.all()
    return jsonify([{
        "id": lot.id,
        "name": lot.prime_location_name,
        "price": lot.price_per_hour,
        "spots": [{"id": s.id, "status": s.status} for s in lot.spots]
    } for lot in lots])




