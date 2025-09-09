from app.extensions import ma
from app.models import Customers

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Customers

customer_schema = CustomerSchema() #works on one object at a time
customers_schema = CustomerSchema(many=True) #works on a list of objects at a time
