from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask import Blueprint, jsonify, request
from Models.db import db
from Models.cancion import Cancion

Cancion_bp = Blueprint('cancion', __name__,url_prefix ="/api")

#-------------------- GET --------------------------------------#

@Cancion_bp.route("/spotify/", methods=["GET"])
def get_Cancion():
    canciones = Cancion.query.all()
    return jsonify([c.serialize()for c in canciones]),200

#-------------------- GET(por id) -------------------------

@Cancion_bp.route("/Spotify/<int:id>",methods =["GET"])
def get_cancion(id):
    cancion = Cancion.query.get_or_404(id)
    return jsonify(cancion.serialize()), 200

# --------------------- POST ------------------------------------#

@Cancion_bp.route('/api/add_cancion', methods = ["POST"])
def add_cancion():
    data = request.get_json() or {}
    
    # Campos obligatorios
    
    required = ("cancion", "artista", "duracion")
    faltantes = [k for k in required if not data.get(k)]
    
    if faltantes:
        return(
            jsonify({"error": f"Faltan campos requeridos: {','.join(faltantes)}"}),
            400,
        )
    
    try:
        nueva_cancion = Cancion(
            cancion = data.get["cancion"],
            album = data.get["album"],
            anio = data.get["anio"],
            duracion = data.get["duracion"],
            fecha_lanzamiento = datetime.strptime(data.get('fecha_lanzamiento'),'%Y-%m-%d') if data.get('fecha_lanzamiento') else None,
            hora_estreno = datetime.strptime(data.get('hora_estreno'),'%H:%M:%S').time() if data.get('hora_estreno') else None,
            descripcion = data.get('descripcion'),
            email_contacto = data.get('email_contacto'),
            activo = data.get('activo',True)
        )
        
        db.session.add(nueva_cancion)
        db.session.commit()
        
        return jsonify({
            'mensaje':'Cancion agregada exitosamente',
            'cancion': nueva_cancion.serialize()
        }),201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error de integridad (¿campo duplicado?)'}),400
    
    except ValueError as ve:
        return jsonify ({'error': f'Error en formato de fecaha u hora:{str(ve)}'}),400
    
    except Exception as e:
        db.session.rollback
        return jsonify ({'error': str(e)}),500
    
#-------------------- PUT ---------------------------------# 

@Cancion_bp.route('/api/update_cancion/<int:id>', methods=['PUT'])
def update_cancion(id):
    data = request.get_json() or {}
    cancion = Cancion.query.get_or_404(id)
    
    if not cancion:
        return jsonify({'error': 'cancion no encontrada'}),404
    
    try:
        cancion.cancion = data.get('cancion', cancion.cancion)
        cancion.artista = data.get('artista', cancion.artista)
        cancion.album = data.get('album', cancion.album)
        cancion.anio = data.get('anio', cancion.anio)
        cancion.duracion = data.get('duracion', cancion.duracion)
        
        if 'fecha_lanzamiento' in data:
            cancion.fecha_lanzamiento = datetime.strptime(data['fecha_lanzamiento'],'%Y-%m-%d')
            
        if 'hora_estreno' in data:
            cancion.hora_estreno = datetime.strptime(data['hora estreno'], '%H:%M:%S').time()
            
        cancion.descripcion = data.get ('descripcion', cancion.descripcion)
        cancion.email_contacto = data.get ('email_contacto', cancion.email_contacto)
        cancion.activo = data.get('activo', cancion.activo)
        
        db.session.commit()
        return jsonify ({'mensaje': 'cancion actualizada corectamente', 'cancion': cancion.serialize()}),200
    
    except ValueError as ve:
        return jsonify ({'error': f'Error en formato de fecha u hora: {str(ve)}'}),400
    
    except Exception as e:
        db.session.rollback()
        return jsonify ({'error': str(e)}),500
    
# ----------------- DELETE -------------------------------#

@Cancion_bp.route('/api/delete_cancion/<int:id>', methods=['DELETE'])
def delete_cancion(id):
    cancion = Cancion.query.get(id)
    
    if not cancion:
        return jsonify ({'error': 'Cancion no encontrada'}),404
    
    try:
        db.session.delete(cancion)
        db.session.commit()
        return jsonify ({'mensaje': 'Canción eliminada correctamente'}),200
    
    except Exception as e:
        db.session.rollback()
        return jsonify ({'error': str(e)}),500
    
    
    
    
    