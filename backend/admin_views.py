from flask import Blueprint, jsonify, request
from flask_security import auth_required, roles_required, current_user
from .data import datastore
from .model import db, Influencer, User, Sponsor, Flag, Campaign

admin_view= Blueprint('admin_views', __name__)

@admin_view.get('/influencers')
@auth_required('token')
@roles_required('admin')
def get_influencers():
    influencers = Influencer.query.all()
    return jsonify([influencer.to_dict() for influencer in influencers])

@admin_view.get('/flag')
@auth_required('token')
@roles_required('admin')
def flag():
    flag=Flag.query.all()

    return jsonify([fl.to_dict() for fl in flag])


@admin_view.delete('/resetflag/<int:id>')
@auth_required('token')
@roles_required('admin')
def resetflag(id):
    print(id)
    flag = Flag.query.get(id)
    print(flag)
    db.session.delete(flag)
    db.session.commit()
    return jsonify({"message": "Flag reset successfully"}), 200


@admin_view.put('/deactivateuser/<int:id>')
@auth_required("token")
@roles_required("admin")
def deactivate_user(id):
   
    influencer = Influencer.query.get(id)
    user = datastore.find_user(id=influencer.user_id)
   
    user.active = True
    db.session.commit()
    return jsonify({"message": "User deactivated successfully"}), 200


@admin_view.get("/fetch_edit_profile/<int:id>")
@auth_required("token")
@roles_required('influencer')
def fetch_edit_profile(id):
   
    influencer = Influencer.query.filter_by(user_id=id).first()

    return jsonify(influencer.to_dict())


@admin_view.put('/editprofile/<int:id>')
@auth_required("token")
@roles_required("influencer")
def edit_profile(id):
    args=request.get_json()
    print(args)
    influencer = Influencer.query.filter_by(user_id=id).first()

    for key, value in args.items():
        if value:
            setattr(influencer, key, value)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
