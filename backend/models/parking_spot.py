from app import db

class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(20), nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)

    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id"), nullable=False)
    reservations = db.relationship("Reservation", backref="spot", lazy=True)
