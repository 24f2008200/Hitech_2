from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import User
from ..app import db

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    u = User(email=email, name=name)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity={"id": user.id, "is_admin": user.is_admin})
    return jsonify({"access_token": token})
