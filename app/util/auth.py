from jose import jwt
import jose
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify



SECRET_KEY = 'super secret secrets'

def encode_token(mechanic_id, role='mechanic'):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        #expiration date of one hour from now
        'iat': datetime.now(timezone.utc),
        'sub': str(mechanic_id), #always set to a string or you will get an error when decoding
        'role': role
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decoration(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token: 
            return jsonify({"error": "token missing from authorization header"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.mechanic_id = int(data['sub'])

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'message': 'invalid expired'}), 403
        
        return f(*args, **kwargs)
    
    return decoration

