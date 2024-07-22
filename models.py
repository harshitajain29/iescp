from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Roles(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String, unique=True)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String[32], unique=True)
    password = db.Column(db.String[256], nullable=False)
    email = db.Column(db.String[256], nullable = False)
    user_status = db.Column(db.Integer, nullable = False)
    profile_created = db.Column(db.Integer, nullable = False)
    r_id = db.Column(db.Integer, db.ForeignKey('roles.r_id'), nullable=False)
    role = db.relationship('Roles', backref=db.backref('user', lazy=True))

class Influencer(db.Model):
    influencer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    platform = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    FName = db.Column(db.String[256])
    LName = db.Column(db.String[256])
    Birthday = db.Column(db.DateTime)
    Bio = db.Column(db.String)
    Photo = db.Column(db.String[255])
    link = db.Column(db.String[255])
    user = db.relationship('User', backref=db.backref('influencer', lazy=True))

class Sponsor(db.Model):
    sponsor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('sponsor', lazy=True))

with app.app_context():
    db.create_all()

