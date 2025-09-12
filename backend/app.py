import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.extensions import db, bcrypt, jwt

basedir = os.path.abspath(os.path.dirname(__file__))




def create_app():
    app = Flask(__name__)
    app = Flask(__name__, instance_relative_config=True)
    db_path = os.path.join(app.instance_path, 'vehicle_parking.db')
    os.makedirs(app.instance_path, exist_ok=True)
    

    # Config
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "devsecret")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # replace with env variable later

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    from backend.routes.auth_routes import auth_bp
    from backend.routes.parking_routes import parking_bp
    from backend.routes.reservation_routes import reservation_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(reservation_bp)
    print("Registered blueprints")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
