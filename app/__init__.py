import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://josephine:root@localhost/inventory_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'lNxaXitGvQEeNHy0/ha+W9xaPmjrygsncnyyRUMsXek=')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrate.init_app(app, db)

    from .models import User, Invitation, Product, Inventory, SupplyRequest, Payment, Store
    from .schemas import UserSchema, InvitationSchema, ProductSchema, InventorySchema, SupplyRequestSchema, PaymentSchema, StoreSchema
    from .routes import app_bp

    app.register_blueprint(app_bp)

    if not app.config['JWT_SECRET_KEY']:
        raise ValueError("JWT_SECRET_KEY not set. Set it in the environment or configuration.")
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("SQLALCHEMY_DATABASE_URI not set. Set it in the environment or configuration.")

    return app, db
