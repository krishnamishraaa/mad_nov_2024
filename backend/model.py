from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, current_user

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    photo = db.Column(db.LargeBinary, nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    create_datetime= db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    sponsor = db.relationship('Sponsor', backref='user', uselist=False)  # One-to-one relationship with Sponsor
    influencer = db.relationship('Influencer', backref='user', uselist=False)  # One-to-one relationship with Influencer


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    verified = db.Column(db.Boolean, nullable=False, default=False)

###############################################

class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    
    sponsor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    budget = db.Column(db.Float)
    company_website = db.Column(db.String(255))
    notes = db.Column(db.String(200))
    approved = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,)  # Reference to the User table
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)

    def to_dict(self):
        return {
            'sponsor_id': self.sponsor_id,
            'name': self.name,
            'industry': self.industry,
            'budget': self.budget,
            'company_website': self.company_website,
            'notes': self.notes,
            'approved': self.approved
        }


class Influencer(db.Model):
    __tablename__ = 'influencer'
    
    influencer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    reach = db.Column(db.Integer)
    social_links = db.Column(db.JSON)
    website = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to the User table

    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)


class Campaign(db.Model):
    __tablename__ = 'campaign'

    campaign_id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the campaign
    description = db.Column(db.String(200))  # Campaign details
    requirements = db.Column(db.String(200))  # Influencer requirements
    start_date = db.Column(db.String(100))  # Start date of the campaign
    end_date = db.Column(db.String(100))  # End date of the campaign
    budget = db.Column(db.Float)  # Budget for the campaign
    visibility = db.Column(db.Boolean(10), default= True, nullable=False)  # public or private
    goals = db.Column(db.String(200))  # Campaign goals
    category= db.Column(db.String(100))  # Category of the campaign
    niche = db.Column(db.String(100))  # Niche of the campaign
    status = db.Column(db.String(10), nullable=False)  # Status: Active, Completed, Cancelled

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)  # Campaign can have many Ad Requests

class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    
    ad_request_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    messages = db.Column(db.String(200)) 
    payment_amount = db.Column(db.Float) 
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(10), nullable=False, default='Pending')
