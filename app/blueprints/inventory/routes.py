from .schemas import part_schema, parts_schema
from flask import request, jsonify
from app.extensions import limiter
from marshmallow import ValidationError
from app.models import PartDescriptions, db
from . import parts_bp
from app.util.auth import token_required
from app.extensions import cache

#create part description
@parts_bp.route('', methods=['POST'])
@token_required
@limiter.limit('100 per day')
def create_part_description(): 
    try: 
        data = part_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    
    new_part = PartDescriptions(**data)
    db.session.add(new_part)
    db.session.commit()
    return part_schema.jsonify(new_part), 201

#Read all part descriptions
@parts_bp.route("", methods=['GET'])
@cache.cached(timeout=60)
def read_part_descrptions(): 
    parts = db.session.query(PartDescriptions).all()

    print(parts)
    return parts_schema.jsonify(parts), 200

#read specific
@parts_bp.route('/<int:part_id>', methods=['GET'])
def read_part_description(part_id):
    part = db.session.get(PartDescriptions, part_id)
    if not part: 
        return jsonify({"error": "part not found"}), 404
    return part_schema.jsonify(part), 200

#update part
@parts_bp.route('/<int:part_id>', methods=['PUT'])
@limiter.limit('100 per day')
@token_required
def update_part(part_id): 
    part = db.session.get(PartDescriptions, part_id)

    if not part: 
        return jsonify({"error": "Part not found"}), 404
    
    try: 
        part_data = part_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    
    for key, value in part_data.items(): 
        setattr(part, key, value)
    
    db.session.commit()
    return part_schema.jsonify(part), 200

#delete part
@parts_bp.route('/<int:part_id>', methods=['DELETE'])
@limiter.limit('100 per day')
@token_required
def delete_part(part_id): 
 
    part = db.session.get(PartDescriptions, part_id)
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted part {part.id}"}), 200
