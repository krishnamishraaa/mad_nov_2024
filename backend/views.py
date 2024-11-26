from flask import Blueprint, jsonify, request
from flask_login import login_user
from .data import datastore
from werkzeug.security import generate_password_hash, check_password_hash

view = Blueprint('views', __name__)


@view.post('/user-login')
def user_login():
	data = request.get_json()
	email = data.get('email')
	if not email:
		return jsonify({"message": "Email not provided"}), 400

	user = datastore.find_user(email=email)

	if not user:    
		return jsonify({"message": "User not found"}), 404
	if not user.active :
		return jsonify({"message": "Account is disabled"}), 401

	if check_password_hash(user.password, data.get('password')):
		login_user(user)
		
		return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name, 'active': user.active, 'id': user.id, 'name': user.name }), 200
	else:
		return jsonify({"message": "Wrong Password"}), 400

@view.post('/user-register')
def user_register():
	data = request.get_json()
	email = data.get('email')
	
	if not email:
		return jsonify({"message": "Email not provided"}), 400
	if datastore.find_user(email=email):
		return jsonify({"message": "User already exists"}), 400
