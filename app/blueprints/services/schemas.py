from app.extensions import ma
from app.models import Services, Mechanics


# class MechanicSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Mechanics
#         fields = ("id",)
#          #used google for this to figure out how to show mechanics on the service tickets

# mechanic_schema = MechanicSchema()
# mechanics_schema = MechanicSchema(many=True)

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    # mechanics = ma.Nested(MechanicSchema, many=True)
    #used google for this to figure out how to show mechanics on the service tickets
    class Meta:
        model = Services
        include_fk = True 
        

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)



