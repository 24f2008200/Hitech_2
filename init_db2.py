from backend.models import db, User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from backend.app import create_app, db
from backend.models import User
from reservations_data import reservations_data

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # --- Add Admin ---
    admin = User(
        name="Admin",
        email="admin@example.com",
        password=generate_password_hash("admin123"),
        role="admin",
        is_admin=True,
        mobile="9999999999",
        address="Admin Address"
    )
    db.session.add(admin)

    # --- Add Some Users ---
    user1 = User(
        name="Ram",
        email="ram@example.com",
        password=generate_password_hash("ram123"),
        is_admin=False,
        mobile="8888888888",
        role="user",
        address="Ram's Address"
    )
    user2 = User(
        name="Murugan",
        email="murugan@example.com",
        password=generate_password_hash("murugan123"),
        is_admin=False,
        mobile="7777777777",
        role="user", address="Murugan's Address"
    )
    user3 = User(
        name="Chandran",
        email="chandran@example.com",
        password=generate_password_hash("chandran123"),
        is_admin=False,
        mobile="6666666666",
        role="user", address="Chandran's Address"
    )
    user4 = User(
        name="Devika",
        email="devika@example.com",
        password=generate_password_hash("devika123"),
        is_admin=False,
        mobile="5555555555",
        role="user", address="Devika's Address"
    )
    user5 = User(
        name="Lakshmi",
        email="lakshmi@example.com",
        password=generate_password_hash("lakshmi123"),
        is_admin=False,
        mobile="4444444444",
        role="user", address="Lakshmi's Address"
    )
    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()

    # --- Add Parking Lots with Spots ---
    lot1 = ParkingLot(
        name="Railway Station",
        prefix="RS",
        address="123 Main Street",
        pin_code="600001",
        price=50,
        max_slots=10
    )
    lot2 = ParkingLot(
        name="Mall Parking Lot",
        prefix="MPL",
        address="456 Side Street",
        pin_code="600002",
        price=40,
        max_slots=30
    )   
    lot3 = ParkingLot(
        name="City Center",
        prefix="CC",
        address="789 Market Road",
        pin_code="600003",
        price=30,
        max_slots=20
    )   
    db.session.add_all([lot1, lot2, lot3])
    db.session.flush()  # ensures lot1.id is available

    lot4 = ParkingLot(
        name="Community Hall",
        prefix="CH",    
        address="456 Side Street",
        pin_code="600002",
        price=40,
        max_slots=15
    )
    db.session.add(lot4)
    db.session.flush()
    db.session.commit()

    # lots = [lot1, lot2, lot3, lot4]

    # for lot in lots:
    #     for i in range(1, lot.max_slots + 1):
    #         spot = ParkingSpot(
    #             lot_id=lot.id,
    #             label=f"{lot.name[-1]}-{i}",
    #         status="A")
    #         db.session.add(spot)
        
    #     db.session.commit()
# Create reservations
#   {
#     "user_no": 2,
#     "spot_no": 69,
#     "car_reg_no": "UP58GL6636",
#     "telephone": "9738265833",
#     "name": "Anil Reddy",
#     "start_time": "2025-09-15 09:00:00",
#     "end_time": "2025-09-16 09:00:00"
#   },

    for r in reservations_data:
        spot = ParkingSpot.query.offset(r["spot_no"] - 1).first()
        reservation = Reservation(
            user_id=r["user_no"],
            spot_id=r["spot_no"] if spot else None,
            vehicle_number=r["car_reg_no"],
            start_time=datetime.strptime(r["start_time"], "%Y-%m-%d %H:%M:%S"),
            end_time= datetime.strptime(r["end_time"], "%Y-%m-%d %H:%M:%S") if r["end_time"] else None,
            driver_contact=f"{r['telephone']}",
            driver_name= r["name"],
        )
        if reservation.end_time is None:
            spot.status = "O"
        db.session.add(reservation)

    db.session.commit()
    print("✅ Database initialized with dummy data!")
