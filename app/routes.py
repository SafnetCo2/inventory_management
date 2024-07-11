# app/routes.py
from flask import Blueprint, jsonify, request
from .schemas import UserSchema, InvitationSchema, ProductSchema, InventorySchema, SupplyRequestSchema, PaymentSchema, StoreSchema
from datetime import datetime
from . import db  # Assuming db is your SQLAlchemy object
from .models import User, Invitation, Product, Inventory, SupplyRequest, Payment, Store

# Define a Blueprint
app_bp = Blueprint('app', __name__)

# Route to get all users
@app_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([UserSchema().dump(user) for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(UserSchema().dump(user)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a new user
@app_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password_hash = data['password_hash']
        role = data['role']

        new_user = User(username=username, email=email, password_hash=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User added successfully', 'user': UserSchema().dump(new_user)}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an exception
        return jsonify({'error': str(e)}), 500
@app_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.password_hash = data.get('password_hash', user.password_hash)
        user.role = data.get('role', user.role)
        user.is_active = data.get('is_active', user.is_active)

        db.session.commit()
        return jsonify({'message': 'User updated successfully', 'user': UserSchema().dump(user)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@app_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to get all invitations
@app_bp.route('/invitations', methods=['GET'])
def get_invitations():
    try:
        invitations = Invitation.query.all()
        return jsonify([InvitationSchema().dump(invitation) for invitation in invitations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app_bp.route('/invitations/<int:id>', methods=['GET'])
def get_invitation(id):
    try:
        invitation = Invitation.query.get(id)
        if not invitation:
            return jsonify({'error': 'Invitation not found'}), 404
        return jsonify(InvitationSchema().dump(invitation)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app_bp.route('/invitations/<int:id>', methods=['PUT'])
def update_invitation(id):
    try:
        invitation = Invitation.query.get(id)
        if not invitation:
            return jsonify({'error': 'Invitation not found'}), 404

        data = request.json
        invitation.token = data.get('token', invitation.token)
        invitation.email = data.get('email', invitation.email)
        invitation.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%dT%H:%M:%S') if 'expiry_date' in data else invitation.expiry_date
        invitation.is_used = data.get('is_used', invitation.is_used)

        db.session.commit()
        return jsonify({'message': 'Invitation updated successfully', 'invitation': InvitationSchema().dump(invitation)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to add a new invitation
@app_bp.route('/invitations', methods=['POST'])
def add_invitation():
    try:
        data = request.json
        token = data['token']
        email = data['email']
        expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%dT%H:%M:%S')  # Example format: '2024-07-11T12:00:00'
        is_used = data.get('is_used', False)

        new_invitation = Invitation(token=token, email=email, expiry_date=expiry_date, is_used=is_used)
        db.session.add(new_invitation)
        db.session.commit()

        return jsonify({'message': 'Invitation added successfully', 'invitation': InvitationSchema().dump(new_invitation)}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an exception
        return jsonify({'error': str(e)}), 500
@app_bp.route('/invitations/<int:id>', methods=['DELETE'])
def delete_invitation(id):
    try:
        invitation = Invitation.query.get(id)
        if not invitation:
            return jsonify({'error': 'Invitation not found'}), 404

        db.session.delete(invitation)
        db.session.commit()
        return jsonify({'message': 'Invitation deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to get all products
@app_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([ProductSchema().dump(product) for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a new product
@app_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.json
        product_name = data['product_name']
        buying_price = data['buying_price']
        selling_price = data['selling_price']

        new_product = Product(product_name=product_name, buying_price=buying_price, selling_price=selling_price)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully', 'product': ProductSchema().dump(new_product)}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an exception
        return jsonify({'error': str(e)}), 500
# Route to get a specific product by ID
@app_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify(ProductSchema().dump(product)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a specific product by ID
@app_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to update a specific product by ID
@app_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.json
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Update fields if provided in the request
        if 'product_name' in data:
            product.product_name = data['product_name']
        if 'buying_price' in data:
            product.buying_price = data['buying_price']
        if 'selling_price' in data:
            product.selling_price = data['selling_price']

        db.session.commit()
        return jsonify({'message': 'Product updated successfully', 'product': ProductSchema().dump(product)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500












# Route to get all inventories
@app_bp.route('/inventories', methods=['GET'])
def get_inventories():
    try:
        inventories = Inventory.query.all()
        return jsonify([InventorySchema().dump(inventory) for inventory in inventories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a new inventory
@app_bp.route('/inventories', methods=['POST'])
def add_inventory():
    try:
        data = request.json
        product_id = data['product_id']
        store_id = data['store_id']
        quantity_received = data['quantity_received']
        quantity_in_stock = data['quantity_in_stock']
        quantity_spoilt = data['quantity_spoilt']
        payment_status = data['payment_status']

        new_inventory = Inventory(product_id=product_id, store_id=store_id, quantity_received=quantity_received,
        quantity_in_stock=quantity_in_stock, quantity_spoilt=quantity_spoilt,
        payment_status=payment_status)
        db.session.add(new_inventory)
        db.session.commit()

        return jsonify({'message': 'Inventory added successfully', 'inventory': InventorySchema().dump(new_inventory)}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an exception
        return jsonify({'error': str(e)}), 500

# Route to get all supply requests
@app_bp.route('/supply-requests', methods=['GET'])
def get_supply_requests():
    try:
        supply_requests = SupplyRequest.query.all()
        return jsonify([SupplyRequestSchema().dump(request) for request in supply_requests]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a new supply request
@app_bp.route('/supply-requests', methods=['POST'])
def add_supply_request():
    try:
        data = request.json
        inventory_id = data['inventory_id']
        user_id = data['user_id']
        status = data['status']

        new_request = SupplyRequest(inventory_id=inventory_id, user_id=user_id, status=status)
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Supply request added successfully', 'request': SupplyRequestSchema().dump(new_request)}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an exception
        return jsonify({'error': str(e)}), 500
# Route to get a specific supply request by ID
@app_bp.route('/supply-requests/<int:id>', methods=['GET'])
def get_supply_request(id):
    try:
        supply_request = SupplyRequest.query.get(id)
        if not supply_request:
            return jsonify({'error': 'Supply request not found'}), 404

        return jsonify(SupplyRequestSchema().dump(supply_request)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a specific supply request by ID
@app_bp.route('/supply-requests/<int:id>', methods=['DELETE'])
def delete_supply_request(id):
    try:
        supply_request = SupplyRequest.query.get(id)
        if not supply_request:
            return jsonify({'error': 'Supply request not found'}), 404

        db.session.delete(supply_request)
        db.session.commit()
        return jsonify({'message': 'Supply request deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to update a specific supply request by ID
@app_bp.route('/supply-requests/<int:id>', methods=['PUT'])
def update_supply_request(id):
    try:
        data = request.json
        supply_request = SupplyRequest.query.get(id)
        if not supply_request:
            return jsonify({'error': 'Supply request not found'}), 404

        # Update fields if provided in the request
        if 'inventory_id' in data:
            supply_request.inventory_id = data['inventory_id']
        if 'user_id' in data:
            supply_request.user_id = data['user_id']
        if 'status' in data:
            supply_request.status = data['status']

        db.session.commit()
        return jsonify({'message': 'Supply request updated successfully', 'supply_request': SupplyRequestSchema().dump(supply_request)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# Route to get all payments
@app_bp.route('/payments', methods=['GET'])
def get_payments():
    try:
        payments = Payment.query.all()
        return jsonify([PaymentSchema().dump(payment) for payment in payments]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a new payment
@app_bp.route('/payments', methods=['POST'])
def add_payment():
    try:
        data = request.json
        supplier_name = data['supplier_name']
        invoice_number = data['invoice_number']
        amount = data['amount']
        payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%dT%H:%M:%S')  # Example format: '2024-07-11T12:00:00'
        payment_status = data['payment_status']

        new_payment = Payment(supplier_name=supplier_name, invoice_number=invoice_number, amount=amount,
        payment_date=payment_date, 
        payment_status=payment_status)
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({'message': 'Payment added successfully', 'payment': PaymentSchema().dump(new_payment)}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an exception
        return jsonify({'error': str(e)}), 500
# Route to get a specific payment by ID
@app_bp.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        return jsonify(PaymentSchema().dump(payment)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a specific payment by ID
@app_bp.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        db.session.delete(payment)
        db.session.commit()
        return jsonify({'message': 'Payment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Route to update a specific payment by ID
@app_bp.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    try:
        data = request.json
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Update fields if provided in the request
        if 'supplier_name' in data:
            payment.supplier_name = data['supplier_name']
        if 'invoice_number' in data:
            payment.invoice_number = data['invoice_number']
        if 'amount' in data:
            payment.amount = data['amount']
        if 'payment_date' in data:
            payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%dT%H:%M:%S')
        if 'payment_status' in data:
            payment.payment_status = data['payment_status']

        db.session.commit()
        return jsonify({'message': 'Payment updated successfully', 'payment': PaymentSchema().dump(payment)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
