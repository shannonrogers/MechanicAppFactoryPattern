from .schemas import service_schema, services_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Services, Mechanics, PartDescriptions, db
from . import services_bp
from app.extensions import cache
from app.util.auth import token_required
from app.blueprints.inventory.schemas import parts_schema
from app.extensions import limiter

#create ticket
@services_bp.route('', methods=['POST'])
@token_required
def create_service():
    try:
        data = service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service = Services(**data)
    db.session.add(new_service)
    db.session.commit()
    return service_schema.jsonify(new_service), 201

#assign mechanic
@services_bp.route('/<int:service_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
@token_required
def assign_mechanic(service_id, mechanic_id): 
    service = db.session.get(Services, service_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not service or not mechanic: 
        return jsonify({"error": "Service or Mechanic not found"}), 400
    
    if mechanic in service.mechanics: 
        return jsonify({"message": 'Mechanic already assigned'}), 409
    
    if mechanic not in service.mechanics:
        service.mechanics.append(mechanic)
        db.session.commit()
        return jsonify({"message": f"{mechanic.first_name} {mechanic.last_name} added to service ID {service_id}"}), 200

#remove mechanic
@services_bp.route('/<int:service_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
@token_required
def remove_mechanic(service_id, mechanic_id):
    service = db.session.get(Services, service_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not service or not mechanic:
        return jsonify({"error": "Service or Mechanic not found"}), 404

    if mechanic in service.mechanics:
        service.mechanics.remove(mechanic)
        db.session.commit()

    return jsonify({"message": f"{mechanic.first_name} {mechanic.last_name} removed from service ID {service_id}"}), 200

#read all tickets
@services_bp.route('', methods=['GET'])
@cache.cached(timeout=60)
def read_services():
    services = db.session.query(Services).all()
 
    return services_schema.jsonify(services), 200

#get tickets related to mechnaic
@services_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_tickets(): 
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    services = mechanic.services

    #fixed it, I was trying to go from services to mechanics instead of the other way and we didn't get service ID in request
    # services = db.session.query(Services).join(Services.mechanics).filter(Mechanics.id == mechanic_id).all()
    #searching services table, joining ticket-mechanics table, where mechanic_id = token mechanic ID returning all results
    #I feel like there should be simpler way since there is a relationship list and ticket_mechanic table, but I ended up having to look it up and this is what I got

    return services_schema.jsonify(services), 200

#add part to service
@services_bp.route('/<int:service_id>/assign-part/<int:part_id>', methods=['PUT'])
def assign_part(service_id, part_id): 
    service = db.session.get(Services, service_id)
    part = db.session.get(PartDescriptions, part_id)

    if not service or not part: 
        return jsonify({"error": "Service or Part not found"}), 400
    
    if part in service.parts: 
        return jsonify({"message": 'Part already added'}), 409
    
    service.parts.append(part)
    db.session.commit()
    return jsonify({"message": f"{part.name} added to service ID {service_id}"}), 200

#find parts on service
@services_bp.route('/get-parts/<int:service_id>', methods=['GET'])
def get_parts(service_id): 
    service = db.session.get(Services, service_id)
    return parts_schema.jsonify(service.parts)
