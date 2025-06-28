from Models.db import db


class Cancion(db.Model):
    __tablename__= 'cancion'
    id = db.Column(db.Integer,primary_key = True)
    cancion = db.Column(db.String (100))
    artista = db.Column(db.String(100))
    album = db.Column (db.String(100))
    anio = db.Column(db.Integer)
    duracion = db.Column(db.Integer)
    fecha_lanzamiento = db.Column(db.Date)
    hora_estreno = db.Column(db.Time)
    descripcion = db.Column(db.Text)
    email_contacto = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    