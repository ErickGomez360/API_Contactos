from flask import Flask
from config import Config
from modelos import db
from schemas import ma

app = Flask(__name__)
app.config.from_object(Config)

db.__init__(app)
ma.__init__(app)

@app.before_first_request
def crear_tablas():
    db.create_all()

@app.route('/contacto', methods=['GET'])
def obtener_contactos():
    pagina = request.args.get('page', 1, type=int)
    tamano_pagina = request.args.get('page_size', 10, type=int)
    contactos = Contacto.query.paginate(pagina, tamano_pagina, False).items
    return jsonify(contactos_esquema.dump(contactos))

@app.route('/contacto/<int:id>', methods=['GET'])
def obtener_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    return contacto_esquema.jsonify(contacto)

@app.route('/contacto', methods=['POST'])
def agregar_contacto():
    nuevo_contacto = Contacto(
        nombre=request.json['nombre'],
        numero_telefono=request.json['numero_telefono'],
        correo_electronico=request.json.get('correo_electronico')
    )
    db.session.add(nuevo_contacto)
    db.session.commit()
    return contacto_esquema.jsonify(nuevo_contacto), 201

@app.route('/contacto/<int:id>', methods=['PUT'])
def actualizar_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    contacto.nombre = request.json.get('nombre', contacto.nombre)
    contacto.numero_telefono = request.json.get('numero_telefono', contacto.numero_telefono)
    contacto.correo_electronico = request.json.get('correo_electronico', contacto.correo_electronico)
    db.session.commit()
    return contacto_esquema.jsonify(contacto)

@app.route('/contacto/<int:id>', methods=['DELETE'])
def eliminar_contacto(id):
    contacto = Contacto.query.get_or_404(id)
    db.session.delete(contacto)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)