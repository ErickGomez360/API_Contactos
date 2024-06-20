from . import ma
from modelos.contactos import Contacto

class ContactosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contacto
        load_instance = True

contacto_schema = ContactosSchema()
contactos_schema = ContactosSchema(many=True)