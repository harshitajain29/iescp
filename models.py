from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Roles(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String, unique=True)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String[32], unique=True)
    passhash = db.Column(db.String[256], nullable=False)
    name = db.Column(db.String[64], nullable=False)
    r_id = db.Column(db.Integer, db.ForeignKey('roles.r_id'), nullable=False)
    role = db.relationship('Roles', backref=db.backref('user', lazy=True))

class Influencer(db.Model):
    influencer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    platform = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('influencer', lazy=True))

class Sponsor(db.Model):
    sponsor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('influencer', lazy=True))

with app.app_context():
    db.create_all()