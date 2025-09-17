import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from backend.extensions import db, bcrypt, jwt
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(os.path.dirname(BASE_DIR), "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)





def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    CORS(app,
     resources={r"/*": {"origins": "http://localhost:5173"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])


    # Config
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "devsecret")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(INSTANCE_DIR, 'vehicle_parking.db')}"
    app.config["CORS_AUTOMATIC_OPTIONS"] = True


    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    from backend.routes.auth_routes import auth_bp
    from backend.routes.admin_routes import admin_bp
    from backend.routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    print("Registered blueprints")
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
