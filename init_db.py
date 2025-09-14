from backend.models import db, User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from backend.app import create_app, db
from backend.models import User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # --- Add Admin ---
    admin = User(
        name="Admin",
        email="admin@example.com",
        password=generate_password_hash("admin123"),
        is_admin=True
    )
    db.session.add(admin)

    # --- Add Some Users ---
    user1 = User(
        name="Alice",
        email="alice@example.com",
        password=generate_password_hash("alice123"),
        is_admin=False
    )
    user2 = User(
        name="Bob",
        email="bob@example.com",
        password=generate_password_hash("bob123"),
        is_admin=False
    )
    db.session.add_all([user1, user2])

    # --- Add Parking Lots with Spots ---
    lot1 = ParkingLot(
        name="Lot A",
        address="123 Main Street",
        pin_code="600001",
        price=50,
        number_of_spots=5
    )
    db.session.add(lot1)
    db.session.flush()  # ensures lot1.id is available

    # Create spots automatically
    for i in range(1, lot1.number_of_spots + 1):
        spot = ParkingSpot(
            lot_id=lot1.id,
            label=f"A-{i}",
            status="A"
        )
        db.session.add(spot)

    lot2 = ParkingLot(
        name="Lot B",
        address="456 Side Street",
        pin_code="600002",
        price=40,
        number_of_spots=3
    )
    db.session.add(lot2)
    db.session.flush()

    for i in range(1, lot2.number_of_spots + 1):
        spot = ParkingSpot(
            lot_id=lot2.id,
            label=f"B-{i}",
            status="A"
        )
        db.session.add(spot)
# Create reservations
    res1 = Reservation(
        user_id=user1.id,
        spot_id=lot1.spots[0].id,
        vehicle_number="TN01AB1234",
        start_time=datetime.utcnow() - timedelta(hours=1),
        end_time=None  # still parked
    )

    res2 = Reservation(
        user_id=user2.id,
        spot_id=lot1.spots[1].id,
        vehicle_number="TN01XY9999",
        start_time=datetime.utcnow() - timedelta(hours=3),
        end_time=datetime.utcnow() - timedelta(hours=1)  # released
    )

    # Mark spot 0 occupied
    lot1.spots[0].status = "O"

    db.session.add_all([res1, res2])
    db.session.commit()
    print("✅ Database initialized with dummy data!")
