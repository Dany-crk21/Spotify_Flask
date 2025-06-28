from Models.db import canciones,db

from flask import request
from Models.db import db
from Models.cancion import Cancion
class cancionesResource(canciones):
    def get(self):
        canciones = canciones.query.filter_by(activo=True).all()
        return [{
            "id":c.id,
            "cancion": c.cancion,
            "artista":c.artista,
            "duracion": c.duracion
            
            
             } for c in canciones], 200
        
    def post(self):
        data = request.get_json()
        nueva = Cancion(
            cancion = data.get("cancion"),
            artista = data.get("artista"),
            album = data.get("album"),
            anio = data.get("anio"),
            duracion = data.get("duracion"),
            fecha_lanzamiento =data.get("fecha_lanzamiento"),
            hora_estreno = data.get("hora_estreno"),
            descripcion = data.get("descripcion"),
            email_contacto = data.get("email_contacto"),
            activo = True
        )
        
        db.session.add(nueva)
        db.session.commit()
        return{"mensaje": "canción agregada", "id":nueva.id},201
    
    
    class CancionBajaLogica(canciones):
        def delete(self,id):
            cancion = Cancion.query.get(id)
            if not cancion:
                return{"mensaje": "No se encontrò la canción"}, 404
            cancion.activo = False
            db.session.commit()
            return{"mensaje": f"Canciòn con ID {id} fue desactivada"},200
        
        #Get /api/spotify/cancniones/clasificadas
        
    class CancionesClasificadasResource(canciones):
        def get(self):
            canciones = Cancion.query.filter_by(activo=True).all()
            clasificacion = {
                "Corta": [],
                "Media": [],
                "Larga": []
            }
    
for c in canciones:
    if c.duracion < 180:
        clasificacion["Corta"].append(c.cancion)
        
    elif 180 <= c.duracion <= 240:
        clasificacion ["Media"].append(c.cancion)
        
    else: clasificacion ["Larga"].append(c.cancion)
    
    return clasificacion,200


