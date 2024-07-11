from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Invitation(db.Model):
    __tablename__ = 'invitations'

    user_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Invitation {self.email}>'

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String, nullable=False)
    buying_price = db.Column(db.Numeric)
    selling_price = db.Column(db.Numeric)

    inventories = db.relationship('Inventory', back_populates='product', overlaps="products,inventories")

    def __repr__(self):
        return f'<Product {self.product_id}>'

class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    quantity_received = db.Column(db.Integer, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    quantity_spoilt = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(10), nullable=False)

    product = db.relationship('Product', back_populates='inventories', overlaps="inventories,product")
    store = db.relationship('Store', backref=db.backref('inventories', lazy=True), overlaps="inventories,store")

    def __repr__(self):
        return f'<Inventory {self.inventory_id}>'

class SupplyRequest(db.Model):
    __tablename__ = 'supply_requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    inventory = db.relationship('Inventory', backref=db.backref('supply_requests', lazy=True))
    user = db.relationship('User', backref=db.backref('supply_requests', lazy=True))

    def __repr__(self):
        return f'<SupplyRequest {self.request_id}>'

class Payment(db.Model):
    __tablename__ = 'payments'

    user_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(25), nullable=False)
    invoice_number = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Payment {self.id}>'

class Store(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Store {self.store_id}>'

