from backend.app import create_app, db
from backend.models import User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create the admin user with required fields
    admin = User(
        email="admin@example.com",
        name="Admin",
        is_admin=True
    )
    admin.set_password("admin123")  # default password

    db.session.add(admin)
    db.session.commit()
    print("Database initialized with admin user.")
