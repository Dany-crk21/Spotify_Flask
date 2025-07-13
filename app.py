from flask import Flask
from Config.Config import DATABASE_CONNECTION_URI
from Models.db import db

app = Flask (__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from Routes.canciones import Cancion_bp

app.register_blueprint(Cancion_bp)

if __name__ == '__main__':
    app.run(debug=True)
    

 
