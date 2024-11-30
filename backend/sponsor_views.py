from flask import Blueprint, jsonify, request
from flask_security import auth_required, roles_required, current_user
from .data import datastore
from .model import db, Influencer, User, Sponsor, Flag, Campaign

sponsor_view = Blueprint("sponsor_views", __name__)


@sponsor_view.post("/flag/post")
@auth_required("token")
@roles_required("sponsor")
def flag_post():

    data = request.get_json()
    flag = Flag(
        reason=data["reason"],
        influencer_id=data["influencer_id"],
        sponsor_id=current_user.id,
    )
    db.session.add(flag)
    db.session.commit()
    return jsonify({"message": "Flagged"}), 200


@sponsor_view.post("/campaign")
@auth_required("token")
@roles_required("sponsor")
def post_campaigns():
    args = request.get_json()
    sponsor_id = current_user.id

    new_campaign = Campaign(sponsor_id=sponsor_id, **args)

    try:
        db.session.add(new_campaign)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error creating campaign: {str(e)}"}, 500

    return {"message": "Campaign created successfully"}, 201

@sponsor_view.get("/campaign")
@auth_required("token")
@roles_required("sponsor")
def get_campaigns():
    sponsor_id = current_user.id
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
    campaigns_dict = [
        campaign.to_dict() for campaign in campaigns
    ]  
    return jsonify(campaigns_dict), 200


@sponsor_view.get("/campaign/<int:id>")
@auth_required("token")
@roles_required("sponsor")
def get_sponsor_campaigns(id):
    campaign = Campaign.query.get(id)
    return jsonify(campaign.to_dict()), 200


@sponsor_view.put("/campaign/<int:campaign_id>")
@auth_required("token")
@roles_required("sponsor")
def update_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return {"message": "Campaign not found"}, 404
    if campaign.sponsor_id != current_user.id:
        return {"message": "Unauthorized to update this campaign"}, 403

    data = request.get_json()
    for key, value in data.items():
        setattr(campaign, key, value)

    db.session.commit()
    return {"message": "Campaign updated successfully"}, 200


@sponsor_view.post("/campaign/<int:campaign_id>")
@auth_required("token")
@roles_required("sponsor")
def post_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return {"message": "Campaign not found"}, 404
    if campaign.sponsor_id != current_user.id:
        return {"message": "Unauthorized to update this campaign"}, 403

    data = request.get_json()
    for key, value in data.items():
        setattr(campaign, key, value)

    db.session.commit()
    return {"message": "Campaign updated successfully"}, 200


@sponsor_view.delete("/deletecampaign/<int:campaign_id>")
@auth_required("token")
@roles_required("sponsor")
def delete_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return {"message": "Campaign not found"}, 404
    if campaign.sponsor_id != current_user.id:
        return {"message": "Unauthorized to delete this campaign"}, 403

    db.session.delete(campaign)
    db.session.commit()
    return {"message": "Campaign deleted successfully"}, 200
