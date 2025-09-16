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
    user3 = User(
        name="Charlie",
        email="charlie@example.com",
        password=generate_password_hash("charlie123"),
        is_admin=False
    )
    user4 = User(
        name="David",
        email="david@example.com",
        password=generate_password_hash("david123"),
        is_admin=False
    )
    user5 = User(
        name="Eve",
        email="eve@example.com",
        password=generate_password_hash("eve123"),
        is_admin=False
    )
    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()

    # --- Add Parking Lots with Spots ---
    lot1 = ParkingLot(
        name="Lot A",
        address="123 Main Street",
        pin_code="600001",
        price=50,
        number_of_spots=10
    )
    lot2 = ParkingLot(
        name="Lot B",
        address="456 Side Street",
        pin_code="600002",
        price=40,
        number_of_spots=30
    )   
    lot3 = ParkingLot(
        name="Lot C",  
        address="789 Market Road",
        pin_code="600003",
        price=30,
        number_of_spots=20
    )   
    db.session.add_all([lot1, lot2, lot3])
    db.session.flush()  # ensures lot1.id is available

    lot4 = ParkingLot(
        name="Lot D",
        address="456 Side Street",
        pin_code="600002",
        price=40,
        number_of_spots=15
    )
    db.session.add(lot4)
    db.session.flush()
    db.session.commit()

    lots = [lot1, lot2, lot3, lot4]

    for lot in lots:
        for i in range(1, lot.number_of_spots + 1):
            spot = ParkingSpot(
                lot_id=lot.id,
                label=f"{lot.name[-1]}-{i}",
            status="A")
            db.session.add(spot)
        
        db.session.commit()
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
    res3= Reservation(
        user_id=user3.id,
        spot_id=lot2.spots[0].id,
        vehicle_number="TN01ZZ8888",
        start_time=datetime.utcnow() - timedelta(hours=2),
        end_time=None  # still parked
    )
    res4 = Reservation(
        user_id=user4.id,
        spot_id=lot3.spots[0].id,
        vehicle_number="TN01CC7777",
        start_time=datetime.utcnow() - timedelta(hours=4),
        end_time=datetime.utcnow() - timedelta(hours=2)  # released
    )
    res5 = Reservation(
        user_id=user5.id,
        spot_id=lot4.spots[0].id,
        vehicle_number="TN01DD6666",
        start_time=datetime.utcnow() - timedelta(hours=1, minutes=30),
        end_time=None  # still parked
    )
    res6 = Reservation(
        user_id=user1.id,
        spot_id=lot4.spots[1].id,
        vehicle_number="TN01EE5555",
        start_time=datetime.utcnow() - timedelta(hours=5),
        end_time=datetime.utcnow() - timedelta(hours=3)  # released
    )
    # Mark spot 0 occupied
    lot1.spots[0].status = "O"

    db.session.add_all([res1, res2, res3, res4, res5, res6])
    db.session.commit()
    print("✅ Database initialized with dummy data!")
