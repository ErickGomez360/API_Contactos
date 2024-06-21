from flask import Flask, request, jsonify
from config import Config
from modelos import db
from modelos.contactos import Contacto
from schemas.contactos import ma, contacto_schema, contactos_schema

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all() 
    
@app.route('/contacto', methods=['GET'])
def obtener_contactos():
    pagina = request.args.get('page', 1, type=int)
    tamano_pagina = request.args.get('page_size', 10, type=int)
    contactos_pag = Contacto.query.paginate(page=pagina, per_page=tamano_pagina, error_out=False)
    contactos = contactos_pag.items
    
    return jsonify(contactos_schema.dump(contactos))

@app.route('/contacto/<int:id>', methods=['GET'])
def obtener_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    return contacto_schema.jsonify(contacto)

@app.route('/contacto', methods=['POST'])
def agregar_contacto():
    nuevo_contacto = Contacto(
        nombre=request.json['nombre'],
        telefono=request.json['telefono'],
        correo=request.json.get('correo')
    )
    db.session.add(nuevo_contacto)
    db.session.commit()
    return contacto_schema.jsonify(nuevo_contacto), 201

@app.route('/contacto/<int:id>', methods=['PUT'])
def actualizar_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    contacto.nombre = request.json.get('nombre', contacto.nombre)
    contacto.telefono = request.json.get('telefono', contacto.telefono)
    contacto.correo = request.json.get('correo', contacto.correo)
    db.session.commit()
    return contacto_schema.jsonify(contacto)

@app.route('/contacto/<int:id>', methods=['DELETE'])
def eliminar_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    db.session.delete(contacto)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)