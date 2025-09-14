from .schemas import login_schema, mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, db
from . import mechanics_bp
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required


#LOGIN FOR MECHANICS
@mechanics_bp.route('/login', methods=['POST'])
@limiter.limit('5 per 10 min')
def login(): 
    try:
        data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    mechanic = db.session.query(Mechanics).where(Mechanics.email==data['email']).first()

    if mechanic and check_password_hash(mechanic.password, data['password']): 
        token = encode_token(mechanic.id)
        return jsonify({
            "message": f"Welcome {mechanic.first_name}",
            "token": token
        }), 200
    
    return jsonify("Invalid email or password"), 403





#create mechanic
@mechanics_bp.route('', methods=['POST'])
# @limiter.limit('10 per day')

def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password'] = generate_password_hash(data['password'])

    new_mechanic = Mechanics(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


#read all
@mechanics_bp.route('', methods=['GET'])
def read_mechanics():
    mechanics = db.session.query(Mechanics).all()
    
    print(mechanics)
    return mechanics_schema.jsonify(mechanics), 200


#read specific
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def read_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    return mechanic_schema.jsonify(mechanic), 200


#delete mechanic
@mechanics_bp.route('', methods=['DELETE'])
@limiter.limit('10 per day')
@token_required
def delete_mechanic(): 
    token_id = request.mechanic_id
    mechanic = db.session.get(Mechanics, token_id)
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted mechanic {mechanic.id}"}), 200



#update mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
@limiter.limit('50 per day')
@token_required
def update_mechanic(mechanic_id):
 # pulled from token
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)  # allow partial updates
    except ValidationError as e:
        return jsonify(e.messages), 400

    if "password" in mechanic_data:
        mechanic_data["password"] = generate_password_hash(mechanic_data["password"])

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


