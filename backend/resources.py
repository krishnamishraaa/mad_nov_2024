from flask_restful import Resource, fields, marshal_with, reqparse, Api, request
from .model import *
from flask import g, request, jsonify, json, current_app as app
from sqlalchemy import desc
from datetime import datetime
from .data import datastore
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

api = Api(prefix="/api")


def check_token_and_user():
	token = request.headers.get("Authorization")
	if not token:
		return jsonify({"message": "Token is missing!"}), 403
	user_details_json = request.headers.get("userDetails")
	user_details = json.loads(user_details_json)
	if not user_details:
		return jsonify({"message": "User details are missing!"}), 403
	else:
		user_id = int(user_details["id"])
		user_role = user_details["role"]
	return token, user_id, user_role

################## CAMPAIGN ###################################
output_fields_campaign = {
	"campaign_id": fields.Integer,
	"sponsor_id": fields.Integer,
	"name": fields.String,
	"description": fields.String,
	"budget": fields.String,
	"start_date": fields.String,
	"end_date": fields.String,
	"visibility": fields.String,
	"goals": fields.String,
}


class CampaignApi(Resource):

	@marshal_with(output_fields_campaign)
	def get(self):
		token, user_id, user_role = check_token_and_user()
		# Retrieve the campaign by its ID
		if user_role == "admin":
			campaign = Campaign.query.all()
		elif user_role == "sponsor":
			campaign = Campaign.query.filter_by(sponsor_id=user_id).all()
		else:
			campaign = Campaign.query.filter_by(visibility=True).all()

		if campaign:
			return campaign, 200
		return {"message": "No Relevant Campaign Found"}, 404

	def post(self):

		token, user_id, user_role = check_token_and_user()

		if not token or user_role != "sponsor":
			return {"message": "Unauthorized access"}, 403

		# Define request parser for campaign input
		parser = reqparse.RequestParser()
		parser.add_argument(
			"name", type=str, required=True, help="Campaign name is required"
		)
		parser.add_argument(
			"description",
			type=str,
			required=True,
			help="Campaign description is required",
		)
		parser.add_argument(
			"start_date", type=str, required=False, help="Start date (optional)"
		)
		parser.add_argument(
			"end_date", type=str, required=False, help="End date (optional)"
		)
		parser.add_argument(
			"budget", type=float, required=False, help="Budget (optional)"
		)
		parser.add_argument(
			"visibility", type=str, required=False, help="Visibility (optional)"
		)
		parser.add_argument(
			"goals", type=str, required=False, help="Campaign goals (optional)"
		)
		parser.add_argument(
			"category", type=str, required=True, help="Category is required"
		)
		parser.add_argument("niche", type=str, required=True, help="Niche is required")
		parser.add_argument(
			"status", type=str, default="Active", help="Status is required"
		)
		args = parser.parse_args()

		new_campaign = Campaign(
			sponsor_id=user_id,
			name=args["name"],
			description=args["description"],
			start_date=args["start_date"],
			end_date=args["end_date"],
			budget=args["budget"],
			visibility=args["visibility"],
			status=args["status"],
			goals=args["goals"],
			category=args["category"],
			niche=args["niche"],
		)
		try:
			db.session.add(new_campaign)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error creating campaign: {str(e)}"}, 500

		return {"message": "Campaign created successfully"}, 201

	# PUT method to update the campaign details
	@marshal_with(output_fields_campaign)
	def put(self, id):
		token, user_id, user_role = check_token_and_user()
		if not token or user_role != "sponsor":
			return {"message": "Unauthorized access"}, 403

		campaign = Campaign.query.get(id)
		if not campaign:
			return {"message": "Campaign not found"}, 404

		# Define request parser for campaign input
		parser = reqparse.RequestParser()
		parser.add_argument("name", type=str, required=True, help="Campaign name is required")
		parser.add_argument("description",type=str,required=True,help="Campaign description is required")
		parser.add_argument("start_date", type=str, required=False, help="Start date (optional)")
		parser.add_argument("end_date", type=str, required=False, help="End date (optional)")
		parser.add_argument("budget", type=float, required=False, help="Budget (optional)")        
		parser.add_argument("visibility", type=str, required=False, help="Visibility (optional)")        
		parser.add_argument("goals", type=str, required=False, help="Campaign goals (optional)")
		parser.add_argument("category", type=str, required=True, help="Category is required")
		parser.add_argument("niche", type=str, required=True, help="Niche is required")
		parser.add_argument("status", type=str, default="Active", help="Status is required")
		args = parser.parse_args()

		# Only update provided fields
		if args["name"]:
			campaign.name = args["name"]
		if args["description"]:
			campaign.description = args["description"]
		if args["start_date"]:
			campaign.start_date = args["start_date"]
		if args["end_date"]:
			campaign.end_date = args["end_date"]
		if args["budget"] is not None:
			campaign.budget = args["budget"]
		if args["visibility"]:
			campaign.visibility = args["visibility"]
		if args["goals"]:
			campaign.goals = args["goals"]
		if args["category"]:
			campaign.category = args["category"]
		if args["niche"]:
			campaign.niche = args["niche"]
		if args["status"]:
			campaign.status = args["status"]
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error updating campaign: {str(e)}"}, 500

		return {"message": "Campaign updated successfully"}, 200

	# DELETE method to delete the campaign
	def delete(self, id):
		token, user_id, user_role = check_token_and_user()
		if user_role != ("admin" or user_id == Campaign.query.get(id).sponsor_id):
			return {"message": "Unauthorized access"}, 403

		campaign = Campaign.query.get(id)
		if not campaign:
			return {"message": "Campaign not found"}, 404

		try:
			db.session.delete(campaign)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error deleting campaign: {str(e)}"}, 500

		return {"message": "Campaign deleted successfully"}, 200

###################### INFLUENCER ########################################

# Output fields for marshalling influencer data
output_fields_influencer = {
	"influencer_id": fields.Integer,
	"name": fields.String,
	"category": fields.String,
	"niche": fields.String,
	"reach": fields.Integer,
}
class InfluencerApi(Resource):
	@marshal_with(output_fields_influencer)

	def get(self):
		# Retrieve influencer by their ID
		influencer = Influencer.query.all()
		if influencer:
			return influencer, 200
		return {"message": "Influencer not found"}, 404

	def post(self):

		
		parser = reqparse.RequestParser()
		parser.add_argument("name", type=str, required=True, help="Influencer name is required")
		parser.add_argument("user_id", type=int, required=True, help="User ID is required")
		parser.add_argument("category", type=str, required=True, help="Category is required")
		parser.add_argument("niche", type=str, required=True, help="Niche is required")
		parser.add_argument("reach", type=int, required=True, help="Reach is required")
		parser.add_argument("social_links", type=str, required=False, help="Social links are optional")
		parser.add_argument("website", type=str, required=False, help="Website is optional")
		args = parser.parse_args()

		# Creatign a new influencer with parsed data
		new_influencer = Influencer(
			user_id=args["user_id"],
			name=args["name"],
			category=args["category"],
			niche=args["niche"],
			reach=args["reach"],
			social_links=args["social_links"],
			website=args["website"],
		)
		try:
			db.session.add(new_influencer)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error creating influencer: {str(e)}"}, 500
		return {"message": "Influencer created successfully"}, 201
	
	def put(self, id):
		token, user_id, user_role = check_token_and_user()
		if not token or user_role != "influencer":
			return {"message": "Unauthorized access"}, 403

		influencer = Influencer.query.get(id)
		if not influencer:
			return {"message": "Influencer not found"}, 404

		parser = reqparse.RequestParser()
		parser.add_argument("name", type=str, required=True, help="Influencer name is required")
		parser.add_argument("category", type=str, required=True, help="Category is required")
		parser.add_argument("niche", type=str, required=True, help="Niche is required")
		parser.add_argument("reach", type=int, required=True, help="Reach is required")
		parser.add_argument("social_links", type=str, required=False, help="Social links are optional")
		parser.add_argument("website", type=str, required=False, help="Website is optional")
		args = parser.parse_args()

		# Only update provided fields
		if args["name"]:
			influencer.name = args["name"]
		if args["category"]:
			influencer.category = args["category"]
		if args["niche"]:
			influencer.niche = args["niche"]
		if args["reach"]:
			influencer.reach = args["reach"]
		if args["social_links"]:
			influencer.social_links = args["social_links"]
		if args["website"]:
			influencer.website = args["website"]
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error updating influencer: {str(e)}"}, 500

		return {"message": "Influencer updated successfully"}, 200
	
	def delete(self, id):
		token, user_id, user_role = check_token_and_user()
		if user_role != "admin" or user_id != Influencer.query.get(id).user_id:
			return {"message": "Unauthorized access"}, 403

		influencer = Influencer.query.get(id)
		if not influencer:
			return {"message": "Influencer not found"}, 404

		try:
			db.session.delete(influencer)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error deleting influencer: {str(e)}"}, 500

		return {"message": "Influencer deleted successfully"}, 200

###################### SPONSOR ########################################

# Output fields for marshalling sponsor data
output_fields_sponsor = {
	"sponsor_id": fields.Integer,
	"name": fields.String,
	"industry": fields.String,
	"budget": fields.Float,
	"company_website": fields.String,
}

class SponsorApi(Resource):
	@marshal_with(output_fields_sponsor)

	def get(self):
		action = request.args.get("action")
		token, user_id, user_role = check_token_and_user()
		if user_role != ("admin" or "sponsor"):
			return {"message": "Unauthorized access"}, 403

		if action == "unapproved":
			# Get all unapproved sponsors
			unapproved_sponsors = Sponsor.query.filter_by(approved=False).all()

			if unapproved_sponsors:
				sponsors_dict = [sponsor.to_dict() for sponsor in unapproved_sponsors]

				return sponsors_dict, 200

			return {"message": "No unapproved sponsors found"}, 404

		elif action == "count":
			# Count total number of sponsors
			total_count = Sponsor.query.count()
			return {"total_sponsors": total_count}, 200

	def post(self):
		# Define request parser for sponsor input
		parser = reqparse.RequestParser()
		parser.add_argument(
			"user_id", type=int, required=True, help="User ID is required"
		)
		parser.add_argument(
			"name", type=str, required=True, help="Sponsor name is required"
		)
		parser.add_argument(
			"industry", type=str, required=True, help="Industry is required"
		)
		parser.add_argument(
			"company_website",
			type=str,
			required=True,
			help="Company Website is required",
		)
		parser.add_argument(
			"notes", type=str, required=False, help="Notes are optional"
		)
		parser.add_argument(
			"approved",
			type=bool,
			default=False,
			help="Approved status is optional",
		)
		parser.add_argument(
			"budget", type=int, required=True, help="Budget is required"
		)

		args = parser.parse_args()

		# Create a new sponsor with parsed data
		new_sponsor = Sponsor(
			user_id=args["user_id"],
			name=args["name"],
			industry=args["industry"],
			budget=args["budget"],
			company_website=args["company_website"],
		)

		# Add the new sponsor to the database and commit
		try:
			db.session.add(new_sponsor)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error creating sponsor: {str(e)}"}, 500
		return {"message": "Sponsor created successfully"}, 201
	
	def put(self, id):
		token, user_id, user_role = check_token_and_user()
		if user_role != "admin":
			return {"message": "Unauthorized access"}, 403

		sponsor = Sponsor.query.get(id)
		if not sponsor:
			return {"message": "Sponsor not found"}, 404

		parser = reqparse.RequestParser()
		# parser.add_argument("name", type=str, required=True, help="Sponsor name is required")
		# parser.add_argument("industry", type=str, required=True, help="Industry is required")
		# parser.add_argument("budget", type=float, required=True, help="Budget is required")
		# parser.add_argument("company_website", type=str, required=True, help="Company Website is required")
		# parser.add_argument("notes", type=str, required=False, help="Notes are optional")
		# parser.add_argument("approved", type=bool, default=False, help="Approved status is optional")
		# args = parser.parse_args()

		# Only update provided fields
		# if args["name"]:
		# 	sponsor.name = args["name"]
		# if args["industry"]:
		# 	sponsor.industry = args["industry"]
		# if args["budget"]:
		# 	sponsor.budget = args["budget"]
		# if args["company_website"]:
		# 	sponsor.company_website = args["company_website"]
		# if args["notes"]:
		# 	sponsor.notes = args["notes"]
		# if args["approved"]:
		sponsor.approved = True
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error updating sponsor: {str(e)}"}, 500

		return {"message": "Sponsor updated successfully"}, 200
	
	def delete(self, id):
		token, user_id, user_role = check_token_and_user()
		if user_role != "admin":
			return {"message": "Unauthorized access"}, 403

		sponsor = Sponsor.query.get(id)
		if not sponsor:
			return {"message": "Sponsor not found"}, 404

		try:
			db.session.delete(sponsor)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error deleting sponsor: {str(e)}"}, 500

		return {"message": "Sponsor deleted successfully"}, 200

###################### AD REQUEST ########################################

# Output fields for marshalling ad request data
output_fields_ad_request = {
	"ad_request_id": fields.Integer,
	"campaign_id": fields.Integer,
	"influencer_id": fields.Integer,
	"messages": fields.String,
	"requirements": fields.String,
	"payment_amount": fields.Float,
	"status": fields.String,  # Pending, Accepted, Rejected
}

######## Will do Further from here #####################
class AdRequestApi(Resource):

	@marshal_with(output_fields_ad_request)
	def get(self):
		# Retrieve ad request by its ID
		ad_request = AdRequest.query.group_by(AdRequest.campaign_id).all()
		if ad_request:
			return ad_request, 200
		return {"message": "Ad Request not found"}, 404

	def post(self, camp_id, inf_id):
		token, user_id, user_role = check_token_and_user()

		# Parse JSON request body
		args = request.get_json()
		print(args)

		if (
			not args
			or "message" not in args
			or "requirements" not in args
			or "payment" not in args
		):
			return {"error": "Missing required fields"}, 400

		# Create a new ad request
		new_ad_request = AdRequest(
			campaign_id=camp_id,
			influencer_id=inf_id,
			messages=args["message"],
			requirements=json.dumps(args["requirements"]),
			payment_amount=args["payment"],
			status=args["status"],
		)
		try:
			db.session.add(new_ad_request)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error creating ad request: {str(e)}"}, 500

		return {"message": "Ad Request created successfully"}, 201


parser_user = reqparse.RequestParser()
parser_user.add_argument("email", type=str, required=True, help="Email is required")
parser_user.add_argument(
	"password", type=str, required=True, help="Password is required"
)
parser_user.add_argument("role", type=str, required=True, help="Role is required")
parser_user.add_argument(
	"active", type=bool, required=False, default=True, help="Active status is required"
)
parser_user.add_argument("name", type=str, required=False, help="Name is optional")


class UserApi(Resource):
	def get(self):

		params = request.args
		if "email" not in params:
			return {"message": "Email parameter is missing"}, 400
		valid_user = datastore.find_user(email=params["email"])

		if valid_user:
			return {"message": "User already exists"}, 400
		else:
			return {"message": "User Available"}, 200

	def post(self):

		args = parser_user.parse_args()
		print(args)
		datastore.create_user(
			email=args["email"],
			password=generate_password_hash(args["password"]),
			roles=[args["role"]],
			name=args["name"],
			active=True,
		)
		datastore.commit()
		newsUser = datastore.find_user(email=args["email"])
		if newsUser:
			return {"userId": newsUser.id}, 201
		else:
			return {"message": "User creation failed"}, 400


class adminApi(Resource):
	def get(self):
		# Give counts related to the users influencer and sponsors
		users = User.query.count()
		influencers = Influencer.query.count()
		sponsors = Sponsor.query.count()
		campaign = Campaign.query.count()

		totalBudget = Sponsor.query.with_entities(Sponsor.budget).all()
		totalBudget = sum([budget[0] for budget in totalBudget])
		return {
			"users": users,
			"influencers": influencers,
			"sponsors": sponsors,
			"totalBudget": totalBudget,
		}, 200


api.add_resource(CampaignApi,"/campaign","/campaign/<int:id>",methods=["GET", "PUT", "POST", "DELETE"],)
api.add_resource(InfluencerApi,"/influencer","/influencer/<int:id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(SponsorApi,"/sponsors","/sponsors/<int:id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(AdRequestApi,"/ad_request", "/ad_request/<int:camp_id>/<int:inf_id>",	methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(UserApi,"/emailcheck","/user","/user/<string:email>" "/user/<int:id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(adminApi, "/adminstats", methods=["GET"])
