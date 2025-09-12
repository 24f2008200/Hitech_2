from app import create_app, db
from models.user import User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create admin
    admin = User(username="admin", is_admin=True)
    admin.set_password("admin123")  # 🔒 change later
    db.session.add(admin)
    db.session.commit()

    print("Database initialized with admin user (username=admin, password=admin123)")
