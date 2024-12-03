from flask import Blueprint, jsonify, request
from flask_security import auth_required, roles_required, current_user
from .model import db, Influencer, User, Sponsor, Flag, Campaign

influencer_view = Blueprint("influencer_views", __name__)

@influencer_view.get("/fetch_edit_profile/<int:id>")
@auth_required("token")
@roles_required("influencer")
def fetch_edit_profile(id):

    influencer = Influencer.query.filter_by(user_id=id).first()

    return jsonify(influencer.to_dict())


@influencer_view.put("/editprofile/<int:id>")
@auth_required("token")
@roles_required("influencer")
def edit_profile(id):
    args = request.get_json()
    influencer = Influencer.query.filter_by(user_id=id).first()

    for key, value in args.items():
        if value:
            setattr(influencer, key, value)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
