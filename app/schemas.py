from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import User, Invitation, Product, Inventory, SupplyRequest, Payment, Store
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class InvitationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        load_instance = True

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

class SupplyRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SupplyRequest
        load_instance = True

class PaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = True

class StoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Store
        load_instance = True




def init_ma(app):
    ma.init_app(app)
