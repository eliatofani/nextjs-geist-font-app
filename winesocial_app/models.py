from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')  # 'admin' or 'user'
    wines = db.relationship('Wine', backref='owner', lazy=True)
    tastings = db.relationship('Tasting', backref='user', lazy=True)
    uploads = db.relationship('Upload', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Wine(db.Model):
    __tablename__ = 'wines'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer)
    type = db.Column(db.String(100))
    region = db.Column(db.String(100))
    alcohol = db.Column(db.Float)
    price = db.Column(db.Float)
    producer = db.Column(db.String(150))
    uploads = db.relationship('Upload', backref='wine', lazy=True)
    tastings = db.relationship('Tasting', backref='wine', lazy=True)

class Tasting(db.Model):
    __tablename__ = 'tastings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), nullable=False)
    tasting_date = db.Column(db.Date, default=datetime.utcnow)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    visual_analysis = db.relationship('VisualAnalysis', uselist=False, backref='tasting')
    olfactory_analysis = db.relationship('OlfactoryAnalysis', uselist=False, backref='tasting')
    gustatory_analysis = db.relationship('GustatoryAnalysis', uselist=False, backref='tasting')

class VisualAnalysis(db.Model):
    __tablename__ = 'visual_analyses'
    id = db.Column(db.Integer, primary_key=True)
    tasting_id = db.Column(db.Integer, db.ForeignKey('tastings.id'), nullable=False)
    color = db.Column(db.String(50))
    color_density = db.Column(db.String(50))
    clarity = db.Column(db.String(50))
    consistency = db.Column(db.String(50))
    bubble_size = db.Column(db.String(50))
    bubble_number = db.Column(db.String(50))
    bubble_persistence = db.Column(db.String(50))

class OlfactoryAnalysis(db.Model):
    __tablename__ = 'olfactory_analyses'
    id = db.Column(db.Integer, primary_key=True)
    tasting_id = db.Column(db.Integer, db.ForeignKey('tastings.id'), nullable=False)
    intensity = db.Column(db.String(50))
    complexity = db.Column(db.String(50))
    quality = db.Column(db.String(50))
    dominant_aromas = db.Column(db.String(255))

class GustatoryAnalysis(db.Model):
    __tablename__ = 'gustatory_analyses'
    id = db.Column(db.Integer, primary_key=True)
    tasting_id = db.Column(db.Integer, db.ForeignKey('tastings.id'), nullable=False)
    sugar_qty = db.Column(db.String(50))
    alcohol_qty = db.Column(db.String(50))
    acidity_qty = db.Column(db.String(50))
    tannin_qty = db.Column(db.String(50))
    tannin_quality = db.Column(db.String(50))
    balance = db.Column(db.String(50))
    body = db.Column(db.String(50))
    persistence = db.Column(db.String(50))
    quality = db.Column(db.String(50))

class Upload(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
