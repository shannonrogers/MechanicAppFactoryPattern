from app.extensions import ma
from app.models import PartDescriptions

class PartDescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = PartDescriptions
   

part_schema = PartDescriptionSchema()
parts_schema = PartDescriptionSchema(many=True)
