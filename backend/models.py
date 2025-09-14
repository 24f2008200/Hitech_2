from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class ParkingLot(db.Model):
    __tablename__ = "parking_lot"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
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
    reservations = db.relationship("Reservation", back_populates="spot", lazy=True)
    @property
    def occupied(self):
        return self.status == 'O'
    @property
    def current_reservation(self):
        # returns the first active one
        for r in self.reservations:
            if r.end_time is None:
                return r
        return None

    @property
    def current_vehicle_number(self):
        res = self.current_reservation
        return res.vehicle_number if res else None

    @property
    def get_details(self):
        r = self.current_reservation
        return {
            "id": self.id,
            "label": self.label,
            "status": self.status,
            "vehicle_number": r.vehicle_number if r else None,
            "occupied_since": r.start_time if r else None,
            "user_id": r.user_id if r else None
        }   
    
class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.id"), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)   # NEW
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    parking_fee = db.Column(db.Float, nullable=True)
    active = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship("User", backref="reservations")
    spot = db.relationship("ParkingSpot", back_populates="reservations")

    # def end_reservation(self, end_time, cost: float):
    #     self.end_time = end_time
    #     self.parking_fee = cost
    #     self.active = False
