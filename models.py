from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Calificacion(db.Model):
    __tablename__ = 'calificacion'  
    id = db.Column(db.Integer, primary_key=True)
    clase = db.Column(db.String(100), nullable=False)
    calificacion = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha_scraping = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Calificacion {self.id}>'    