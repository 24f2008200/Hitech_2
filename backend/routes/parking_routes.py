from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import ParkingLot, ParkingSpot

parking_bp = Blueprint("parking", __name__, url_prefix="/parking")


# Create parking lot
@parking_bp.route("/lots", methods=["POST"])
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


# List parking lots
@parking_bp.route("/lots", methods=["GET"])
def list_lots():
    lots = ParkingLot.query.all()
    return jsonify([{
        "id": lot.id,
        "name": lot.prime_location_name,
        "price": lot.price_per_hour,
        "spots": [{"id": s.id, "status": s.status} for s in lot.spots]
    } for lot in lots])


# Delete parking lot
@parking_bp.route("/lots/<int:lot_id>", methods=["DELETE"])
def delete_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"error": "Lot not found"}), 404
    db.session.delete(lot)
    db.session.commit()
    return jsonify({"message": "Lot deleted"})
