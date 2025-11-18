from flask import Flask
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.services import services_bp
from .blueprints.inventory import parts_bp
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

#swagger bluepring
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Mechanic Shop API'})



def create_app(config_name): 
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    CORS(app)

    #intialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #Registering Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(parts_bp, url_prefix='/parts')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


    return app