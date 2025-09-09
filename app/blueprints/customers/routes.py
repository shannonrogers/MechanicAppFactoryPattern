from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from app.extensions import limiter
from marshmallow import ValidationError
from app.models import Customers, db
from . import customers_bp
from app.util.auth import token_required



#create customer
@customers_bp.route('', methods=['POST'])
@limiter.limit("20 per hour")
@token_required
def create_customer():
    try:
        data = customer_schema.load(request.json) 
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_customer = Customers(**data)
    db.session.add(new_customer)
    db.session.commit()
    # print('someone is creating a customer')
    return customer_schema.jsonify(new_customer), 201

#read all customers
@customers_bp.route('', methods=['GET'])
def read_customers():
    customers = db.session.query(Customers).all()
    print(customers)
    return customers_schema.jsonify(customers), 200
    
#read single customer - dynamic endpoint
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def read_customer(customer_id): 
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    return customer_schema.jsonify(customer), 200

#delete a customer
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@limiter.limit("10 per day")
@token_required
def delete_customer(customer_id): 
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer {customer.id}"}), 200

#update a customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit('50 per day')
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

#search for customer by email
@customers_bp.route('/searchcustomers/<customer_email>', methods=['GET'])
def search_customer(customer_email):
   

    if not customer_email:
        return jsonify({"error": "Email required"}), 400

    customer = db.session.query(Customers).filter(Customers.email == customer_email).first()
    
    if not customer: 
        return jsonify({"error": "Customer not found."}), 404
    
    return customer_schema.jsonify(customer), 200
