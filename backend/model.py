from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer,db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer,db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    verified = db.Column(db.Boolean, nullable=False, default=False)

###############################################


class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    
    sponsor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Company Name / Individual Name
    industry = db.Column(db.String(100))
    budget = db.Column(db.Float)

    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)  # Sponsor can have many campaigns

class Influencer(db.Model):
    __tablename__ = 'influencer'
    
    influencer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the influencer
    category = db.Column(db.String(100))  # Influencer's category (e.g., technology, fashion)
    niche = db.Column(db.String(100))  # Specific niche within the category
    reach = db.Column(db.Integer)  # Number of followers, activity, etc.

    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)  # Influencer can have many Ad Requests

class Campaign(db.Model):
    __tablename__ = 'campaign'
    
    campaign_id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the campaign
    description = db.Column(db.String(200))  # Campaign details
    start_date = db.Column(db.String(100))  # Start date of the campaign
    end_date = db.Column(db.String(100))  # End date of the campaign
    budget = db.Column(db.Float)  # Budget for the campaign
    visibility = db.Column(db.String(10), nullable=False)  # public or private
    goals = db.Column(db.String(200))  # Campaign goals

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)  # Campaign can have many Ad Requests

class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    
    ad_request_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    messages = db.Column(db.String(200))  # Conversation or negotiation between sponsor and influencer
    requirements = db.Column(db.String(200))  # Requirements for the ad (e.g., "show Samsung s23 in 3 videos")
    payment_amount = db.Column(db.Float)  # Agreed payment amount
    status = db.Column(db.String(10), nullable=False)  # Status: Pending, Accepted, Rejected
