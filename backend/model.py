from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, current_user
from datetime import datetime

db = SQLAlchemy()

def get_formatted_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "'%Y-%m-%d %H:%M:%S'").strftime(
                "%Y-%m-%d"
            )
        except ValueError:
            return None  # Return None if the date is not valid
        return None  # Return None if no date is provided


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

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'active': self.active,
            'photo': self.photo,
            'create_datetime': self.create_datetime,
            'roles': [role.name for role in self.roles]
        }


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,) 
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)

    def to_dict(self):
        return {
            'influencer_id': self.influencer_id,
            'name': self.name,
            'category': self.category,
            'niche': self.niche,
            'reach': self.reach,
            'social_links': self.social_links,
            'website': self.website
        }


class Campaign(db.Model):
    __tablename__ = 'campaign'

    campaign_id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)  
    description = db.Column(db.String(200)) 
    requirements = db.Column(db.String(200))  
    start_date = db.Column((db.String), nullable=False, default=db.func.current_timestamp())
    end_date = db.Column(db.String)
    budget = db.Column(db.Float) 
    visibility = db.Column(db.Boolean(), default= True, nullable=False)  
    goals = db.Column(db.String(200))  
    category= db.Column(db.String(100)) 
    niche = db.Column(db.String(100)) 
    status = db.Column(db.String(10), nullable=False)  # Status: Active, Completed, Cancelled
    interested_influencers = db.Column(db.Text(200))  # List of influencer ids

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)  

    def change_status(self):
        if self.status not in ['Active', 'Completed', 'Cancelled']:
            raise ValueError('Invalid status')

        if self. end_date < db.func.current_timestamp():
            self.status = 'Completed'
            self.visibility = False
        if self.end_date and self.end_date < datetime.now():
            self.status = 'Completed'
            self.visibility = 0

    def to_dict(self):
        return {
            "campaign_id": self.campaign_id,
            "name": self.name,
            "description": self.description,
            "requirements": self.requirements,
            "start_date": get_formatted_date(self.start_date),
            "end_date": get_formatted_date(self.end_date),
            "budget": self.budget,
            "visibility": self.visibility,
            "goals": self.goals,
            "category": self.category,
            "niche": self.niche,
            "status": self.status,
        }

class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    
    ad_request_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    messages = db.Column(db.String(200)) 
    payment_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(10), nullable=False, default='Pending')

    def to_dict(self):
        return {
            'ad_request_id': self.ad_request_id,
            'campaign_id': self.campaign_id,
            'influencer_id': self.influencer_id,
            'messages': self.messages,
            'payment_amount': self.payment_amount,
            'created_at': self.created_at,
            'status': self.status
        }

class Flag(db.Model):
    __tablename__ = 'flag'

    flag_id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'), nullable=False)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(10), nullable=False, default='Pending')
    
    def to_dict(self):
        return {
            'flag_id': self.flag_id,
            'influencer_id': self.influencer_id,
            'sponsor_id': self.sponsor_id,
            'reason': self.reason,
            'created_at': self.created_at,
            'status': self.status
        }
