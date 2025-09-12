from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class ParkingLot(db.Model):
    __tablename__ = "parking_lot"

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(255), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    address = db.Column(db.String(512))
    pin_code = db.Column(db.String(20))
    number_of_spots = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    spots = db.relationship("ParkingSpot", backref="lot", cascade="all, delete-orphan")


class ParkingSpot(db.Model):
    __tablename__ = "parking_spot"

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lot.id"), nullable=False)
    status = db.Column(db.String(1), nullable=False, default="A")  # A=available, O=occupied
    label = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    start_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_ts = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, default=True)

    spot = db.relationship("ParkingSpot")
    user = db.relationship("User")

    def end_reservation(self, end_time, cost: float):
        self.end_ts = end_time
        self.parking_cost = cost
        self.active = False
