from flask import Blueprint, jsonify, request, send_file
from flask_security import current_user
from .data import datastore
from werkzeug.security import generate_password_hash, check_password_hash
from .tasks import generate_campaign_csv
from celery.result import AsyncResult
from .model import Campaign
import os
import flask_excel as excel


view = Blueprint('views', __name__)

@view.get('/download_csv')
def download_csv():
   task = generate_campaign_csv.delay()
   return jsonify({"task_id": task.id})

@view.get('getcsv/<task_id>')
def getcsv(task_id):
	task = AsyncResult(task_id)
	if task.ready():
		filename = task.result
		return send_file("../"+filename, as_attachment=True)
	else:
		return jsonify({"message": "Task in progress"}), 404
		
	



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
