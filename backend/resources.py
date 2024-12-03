from flask_restful import Resource, fields, marshal_with, reqparse, Api, request
from .model import *
from flask import request, jsonify, json
from datetime import datetime
from .data import datastore
from .instances import cache
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


def convert_to_datetime(date_str):
    if date_str:
        try:
            # Parsing the date string into a datetime object
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Return None if the date string is invalid
            return None
    return None


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
	"niche": fields.String,
	"category": fields.String,
	"requirements": fields.String,
}


class CampaignApi(Resource):

	@marshal_with(output_fields_campaign)
	def get(self):
		token, user_id, user_role = check_token_and_user()
		
		if user_role == "influencer":
			infl_id = User.query.get(user_id).influencer.influencer_id
		if user_role == "sponsor":
			sponsor_id = User.query.get(user_id).sponsor.sponsor_id

		id = request.args.get("id")

		if id != "null" and id is not None:
			campaign = Campaign.query.get(id)
			
			return campaign, 200
		else:
			if user_role == "admin":
				campaign = Campaign.query.all()
				return campaign, 200
			elif user_role == "sponsor":
				campaign = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
				return campaign, 200
			else:
				
				campaign = Campaign.query.all()

				return campaign, 200

	def post(self):

		token, user_id, user_role = check_token_and_user()
		sponsor_id = User.query.get(user_id).sponsor.sponsor_id

		if not token or user_role != "sponsor":
			return {"message": "Unauthorized access"}, 403

		
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
			"visibility", type=bool, required=False, help="Visibility (optional)"
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
		parser.add_argument("requirements", type=str, required=False, help="Requirements are optional")
		args = parser.parse_args()

		start_date = datetime.strptime(args["start_date"], "%Y-%m-%d") if args["start_date"] else None
		end_date = datetime.strptime(args["end_date"], "%Y-%m-%d") if args["end_date"] else None

		new_campaign = Campaign(
			sponsor_id=sponsor_id,
			name=args["name"],
			description=args["description"],
			start_date=start_date,
			end_date=end_date,
			budget=args["budget"],
			visibility=args["visibility"],
			status=args["status"],
			goals=args["goals"],
			category=args["category"],
			requirements=args["requirements"],
			niche=args["niche"],
		)
		try:
			db.session.add(new_campaign)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error creating campaign: {str(e)}"}, 500

		return {"message": "Campaign created successfully"}, 201

	# PUT method to update the campaign details (Currently doing from sposnor_views.py)
	@marshal_with(output_fields_campaign)
	def put(self, id):
		token, user_id, user_role = check_token_and_user()

		if not token or user_role != "sponsor":
			return {"message": "Unauthorized access"}, 403

		campaign = Campaign.query.get(id)
		if not campaign:
			return {"message": "Campaign not found"}, 404

		
		args = request.get_json()
		
		
		if args["name"]:
			campaign.name = args["name"]
		if args["description"]:
			campaign.description = args["description"]
		if args["start_date"]:
			campaign.start_date = (
				datetime.strptime(args["start_date"], "%Y-%m-%d")
				if args["start_date"]
				else None
			)
		if args["end_date"]:
			campaign.end_date = (
				datetime.strptime(args["start_date"], "%Y-%m-%d")
				if args["end_date"]
				else None
			)
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
		if args["requirements"]:
			campaign.requirements = args["requirements"]
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

	@cache.cached(timeout=50)
	def get(self):

		influencer = Influencer.query.all()
		return influencer, 200

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
			
			unapproved_sponsors = Sponsor.query.filter_by(approved=False).all()

			if unapproved_sponsors:
				sponsors_dict = [sponsor.to_dict() for sponsor in unapproved_sponsors]

				return sponsors_dict, 200

			return {"message": "No unapproved sponsors found"}, 200

		elif action == "count":
			
			total_count = Sponsor.query.count()
			return {"total_sponsors": total_count}, 200

	def post(self):
		
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

		
		new_sponsor = Sponsor(
			user_id=args["user_id"],
			name=args["name"],
			industry=args["industry"],
			budget=args["budget"],
			company_website=args["company_website"],
		)

		
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

class AdRequestApi(Resource):

	@marshal_with(output_fields_ad_request)
	def get(self):
		token, user_id, user_role = check_token_and_user()

		if user_role == "admin":
			filter = request.args.get("filter")
			print(filter)
			if filter == "pending":
				ad_request = AdRequest.query.filter_by(status="Pending").all()
			elif filter == "accepted":
				ad_request = AdRequest.query.filter_by(status="Accepted").all()
			elif filter == "rejected":
				ad_request = AdRequest.query.filter_by(status="Rejected").all()
			else:
				ad_request = AdRequest.query.all()
			return ad_request, 200

		elif user_role == "sponsor":
			sponsor_id = User.query.get(user_id).sponsor.sponsor_id
			filter = request.args.get("filter")
			if filter == "pending":
				ad_request = AdRequest.query.join(Campaign).filter(
					Campaign.sponsor_id == sponsor_id, AdRequest.status == "Pending"
				).all()
			elif filter == "accepted":
				ad_request = AdRequest.query.join(Campaign).filter(
					Campaign.sponsor_id == sponsor_id, AdRequest.status == "Accepted"
				).all()
			elif filter == "rejected":
				ad_request = AdRequest.query.join(Campaign).filter(
					Campaign.sponsor_id == sponsor_id, AdRequest.status == "Rejected"
				).all()
			else:
				ad_request = AdRequest.query.join(Campaign).filter(
					Campaign.sponsor_id == sponsor_id
				).all()

			return ad_request, 200

		elif user_role == "influencer":
			infl_id = User.query.get(user_id).influencer.influencer_id
			filter = request.args.get("filter")

			if filter == "pending":
				ad_request = AdRequest.query.filter_by(
					influencer_id=infl_id, status="Pending"
				).all()

			elif filter == "accepted":
				ad_request = AdRequest.query.filter_by(
					influencer_id=infl_id, status="Accepted"
				).all()

			elif filter == "rejected":
				ad_request = AdRequest.query.filter_by(
					influencer_id=infl_id, status="Rejected"
				).all()

			else:
				ad_request = AdRequest.query.filter_by(influencer_id=infl_id).all()

			return ad_request, 200
		return {"message": "Ad Request not found"}, 404

	def post(self, camp_id, inf_id):
		token, user_id, user_role = check_token_and_user()

		
		args = request.get_json()

		if not args or "messages" not in args or "payment_amount" not in args:
			return {"error": "Missing required fields"}, 400

		
		new_ad_request = AdRequest(**args)
		try:
			db.session.add(new_ad_request)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error creating ad request: {str(e)}"}, 500

		return {"message": "Ad Request created successfully"}, 201

	def put(self, id):
		token, user_id, user_role = check_token_and_user()

		ad_request = AdRequest.query.get(id)

		if not ad_request:
			return {"message": "Ad Request not found"}, 404

		# if ad_request.campaign.sponsor_id != user_id or ad_request.influencer.user_id != user_id:
		# 	return {"message": "Unauthorized access"}, 403

		args = request.get_json()
		
		if not args:
			return {"message": "Missing required fields"}, 400
		param = args.get("param")
		if not param:
			return {"message": "Missing 'param' field"}, 400
		try:
			if param == "accept":
				ad_request.status = "Accepted"
				db.session.commit()
				return {"message": "Ad Request accepted successfully"}, 200
			
			elif param == "reject":
				ad_request.status = "Rejected"
				db.session.commit()
				return {"message": "Ad Request rejected successfully"}, 200
			
			elif param == "negotiate":
				amount = args.get("amount")
				if not amount:
					return {"message": "Missing 'amount' field for negotiation"}, 400
				ad_request.payment_amount = amount
				db.session.commit()
				return {"message": "Ad Request negotiated successfully"}, 200
			
			elif param == "message":
				new_message = args.get("message")
				
				if not new_message:
					return {"message": "Missing message data"}, 400
				
				# Initialize or load existing messages
				if ad_request.messages in [None, ""]:
					current_messages = []
				
				else:
					# Attempt to decode JSON if the format matches a list
					if ad_request.messages.startswith("[") and ad_request.messages.endswith("]"):
						try:
							current_messages = json.loads(ad_request.messages)
						except json.JSONDecodeError:
							current_messages = []
					else:
						#Treat the existing string as a single message
						current_messages = [ad_request.messages]
				current_messages.append(new_message)
				ad_request.messages = json.dumps(current_messages)
				db.session.commit()
				return {"message": "Message added successfully"}, 200
			else:
				return {"message": f"Invalid param value: {param}"}, 400
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error updating ad request: {str(e)}"}, 501

	def delete(self, id):
		token, user_id, user_role = check_token_and_user()
		if user_role != "sponsor":
			return {"message": "Unauthorized access"}, 403

		ad_request = AdRequest.query.get(id)
		if not ad_request:
			return {"message": "Ad Request not found"}, 404

		try:
			db.session.delete(ad_request)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error deleting ad request: {str(e)}"}, 500

		return {"message": "Ad Request deleted successfully"}, 200


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
		parser_user = reqparse.RequestParser()
		parser_user.add_argument("email", type=str, required=True, help="Email is required")
		parser_user.add_argument("password", type=str, required=True, help="Password is required")
		parser_user.add_argument("role", type=str, required=True, help="Role is required")
		parser_user.add_argument("active", type=bool, required=False, default=True, help="Active status is required")
		parser_user.add_argument("name", type=str, required=False, help="Name is optional")

		args = parser_user.parse_args()
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

class Profilepage(Resource):

	def get(self):
		params = request.args
		
		if "id" not in params:
			return {"message": "Id parameter is missing"}, 400
		id = params[0]["id"]

		influnecer_details = Influencer.query.get(id)
		return influnecer_details, 200


class Stats(Resource):
	def get(self):
		token, user_id, user_role = check_token_and_user()

		
		users = User.query.count()
		influencers = Influencer.query.count()
		sponsors = Sponsor.query.count()
		campaign = Campaign.query.count()
		adRequest= AdRequest.query.count()
		totalBudget = Sponsor.query.with_entities(Sponsor.budget).all()
		totalBudget = sum([budget[0] for budget in totalBudget])
		pendingAdRequests = AdRequest.query.filter_by(status="Pending").count()
		totalReach=Influencer.query.with_entities(Influencer.reach).all()
		uniquecategories = Campaign.query.with_entities(Campaign.category).distinct().count()
		best_category=Campaign.query.with_entities(Campaign.category).distinct().first()

		if user_role == "admin":
			return {
			"users": users,
			"influencers": influencers,
			"sponsors": sponsors,
			"totalBudget": totalBudget,
			"campaigns": campaign,
			"adRequests": adRequest,
			"pendingAdRequests": pendingAdRequests,
			"totalReach": sum([reach[0] for reach in totalReach]),
			"uniquecategories": uniquecategories,
			"best_category": best_category[0],
			}, 200

		elif user_role == "sponsor":
			sponsor_id = User.query.get(user_id).sponsor.sponsor_id
			campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).count()
			sponsor_campaign_ids = (
				Campaign.query.with_entities(Campaign.campaign_id)
				.filter_by(sponsor_id=sponsor_id)
				.subquery()
			)
			campaigns = Campaign.query.filter(
				Campaign.campaign_id.in_(sponsor_campaign_ids)
			).count()
			adRequests_total = AdRequest.query.filter(
				AdRequest.campaign_id.in_(sponsor_campaign_ids)
			).count()
			adRequests_pending = AdRequest.query.filter(
				AdRequest.campaign_id.in_(sponsor_campaign_ids),
				AdRequest.status == "Pending",
			).count()
			adRequests_accepted = AdRequest.query.filter(
				AdRequest.campaign_id.in_(sponsor_campaign_ids),
				AdRequest.status == "Accepted",
			).count()
			adRequests_rejected = AdRequest.query.filter(
				AdRequest.campaign_id.in_(sponsor_campaign_ids),
				AdRequest.status == "Rejected",
			).count()
			total_sponsor_Budget = (
				Sponsor.query.with_entities(Sponsor.budget)
				.filter_by(sponsor_id=sponsor_id)
				.all()
			)
			spentBudget = (
				AdRequest.query.with_entities(AdRequest.payment_amount)
				.filter(AdRequest.campaign_id.in_(sponsor_campaign_ids))
				.all()
			)
			remainingBudget = sum([budget[0] for budget in total_sponsor_Budget]) - sum(
				[spent[0] for spent in spentBudget]
			)
			return {
				"campaigns": campaigns,
				"adRequests_total": adRequests_total,
				"adRequests_pending": adRequests_pending,
				"adRequests_accepted": adRequests_accepted,
				"adRequests_rejected": adRequests_rejected,
				"totalBudget": sum([budget[0] for budget in total_sponsor_Budget]),
				"remainingBudget": remainingBudget,
			}, 200

		elif user_role == "influencer":
			infl_id = User.query.get(user_id).influencer.influencer_id
			adRequests_total = AdRequest.query.filter_by(influencer_id=infl_id).count()
			adRequests_pending = AdRequest.query.filter_by(
				influencer_id=infl_id, status="Pending"
			).count()
			adRequests_accepted = AdRequest.query.filter_by(
				influencer_id=infl_id, status="Accepted"
			).count()
			adRequests_rejected = AdRequest.query.filter_by(
				influencer_id=infl_id, status="Rejected"
			).count()
			earnings = (
				AdRequest.query.with_entities(AdRequest.payment_amount)
				.filter_by(influencer_id=infl_id)
				.all()
			)
			totalEarnings = sum([earn[0] for earn in earnings if earn[0] is not None])
			EarningThisMonth = (
				AdRequest.query.with_entities(AdRequest.payment_amount)
				.filter_by(influencer_id=infl_id)
				.filter(AdRequest.created_at >= datetime.now().replace(day=1))
				.all()
			)
			return {
				"adRequests_total": adRequests_total,
				"adRequests_pending": adRequests_pending,
				"adRequests_accepted": adRequests_accepted,
				"adRequests_rejected": adRequests_rejected,
				"totalEarnings": totalEarnings,
				"EarningThisMonth": sum(
					[earn[0] for earn in EarningThisMonth if earn[0] is not None]
				),
			}
		else:
			return {"message": "Unauthorized access"}, 403

class Insights(Resource):

	def get(self):
		token, user_id, user_role = check_token_and_user()

		best_category_overall = (
			Campaign.query.with_entities(Campaign.category)
			.order_by(Campaign.budget.desc())
			.distinct()
			.first()
		)
		top_influencers = (
			Influencer.query.order_by(Influencer.reach.desc()).limit(5).all()
		)
		top_influencers = [influencer.to_dict() for influencer in top_influencers]
		highValue_campaigns = (
			Campaign.query.order_by(Campaign.budget.desc()).limit(5).all()
		)
		highValue_campaigns = [campaign.to_dict() for campaign in highValue_campaigns]
		trending_campaigns = (
			Campaign.query.order_by(Campaign.interested_influencers).limit(5).all()
		)
		trending_campaigns = [
			(
				{
					"name": campaign.name,
					"sponsor": Campaign.query.get(campaign.campaign_id).sponsor.name,
				}
			)
			for campaign in trending_campaigns
		]
		today_signups = User.query.filter(
			User.create_datetime >= datetime.now().replace(hour=0, minute=0, second=0)
		).count()

		if user_role == "admin":
			return {
				"top influencers": top_influencers,
				"trending campaigns": trending_campaigns,
				"best category": best_category_overall[0],
				"today signups": today_signups,
			}, 200

		if user_role == "influencer":
			infl_id = User.query.get(user_id).influencer.influencer_id
			earning_this_month = (
				AdRequest.query.with_entities(AdRequest.payment_amount)
				.filter_by(influencer_id=infl_id)
				.filter(AdRequest.created_at >= datetime.now().replace(day=1))
				.all()
			)
			totalEarning = (
				AdRequest.query.with_entities(AdRequest.payment_amount)
				.filter_by(influencer_id=infl_id)
				.all()
			)
			totalEarning = sum(
				[earn[0] for earn in totalEarning if earn[0] is not None]
			)
			earning_this_month = sum([earn[0] for earn in earning_this_month if earn[0] is not None])

			return {
				"top_influencers": top_influencers,
				"trending_campaigns": trending_campaigns,
				"totalEarning": totalEarning,
				"earning_this_month": earning_this_month,
			}, 200

		if user_role == "sponsor":
			sponsor_id = User.query.get(user_id).sponsor.sponsor_id
			best_category = (
				Campaign.query.with_entities(Campaign.category).filter_by(sponsor_id=sponsor_id)
				.order_by(Campaign.budget.desc())
				.distinct()
				.first().category
			)
			totalBudget = (
				Sponsor.query
				.filter_by(sponsor_id=sponsor_id).first().budget
			)

			spentBudgetquery = (
				AdRequest.query.with_entities(AdRequest.payment_amount)
				.filter(
					AdRequest.campaign_id.in_(
						Campaign.query.filter_by(sponsor_id=sponsor_id).with_entities(
							Campaign.campaign_id
						)
					)
				)
				.all()
			)
			spentBudget = sum([spent[0] for spent in spentBudgetquery if spent[0] is not None])
			remainingBudget = totalBudget - spentBudget
			return {
				"top influencers": top_influencers,
				"high Value campaigns": highValue_campaigns,
				"best category": best_category,
				"My Budget": totalBudget,
				"spent Budget": spentBudget,
				"remaining Budget": remainingBudget,
			}, 200


class UpdateCampaign(Resource):
	def put(self, id):
		campaign = Campaign.query.get(id)
		if not campaign:
			return {"message": "Campaign not found"}, 404
		
		args = request.get_json()
		new_influencer = args.get("interested_influencers")
		if not new_influencer or not isinstance(new_influencer, dict):
			return {"message": "Invalid or missing 'interested_influencers' data"}, 400
		
		
		try:
			current_influencers = json.loads(campaign.interested_influencers) if campaign.interested_influencers else []
			
			if not isinstance(current_influencers, list):
				current_influencers = []
		except json.JSONDecodeError:
			current_influencers = []
			# Append the new influencer and serialize back to JSON
		current_influencers.append(new_influencer)
		try:
			campaign.interested_influencers = json.dumps(current_influencers)
		except Exception as e:
			return {"message": f"Error serializing influencer data: {str(e)}"}, 500
		
		 # Commit changes to the database
		try:
			db.session.commit()
			return {"message": "Campaign updated successfully"}, 200
		except Exception as e:
			db.session.rollback()
			return {"message": f"Error updating campaign: {str(e)}"}, 500

class Campaign_Filter(Resource):
	
	def get(self):
		category = request.args.get('category')
		niche = request.args.get('niche')
		budget = request.args.get('budget')
		requirement = request.args.get('requirement')
		
		query = Campaign.query
		
		if category:
			query = query.filter(Campaign.category.ilike(f"%{category}%"))
			
		if niche:
			query = query.filter(Campaign.niche.ilike(f"%{niche}%"))
		
		if budget:
			query = query.filter(Campaign.budget>=budget)
			
		if requirement:
			query = query.filter(Campaign.requirements.ilike(f"%{requirement}%"))
		
		campaigns = query.all()
		
		return {"campaigns": [campaign.to_dict() for campaign in campaigns]}, 200

class ForGraphs(Resource):
	def get(self):
	
		campaigns = Campaign.query.all()
		campaigns = [campaign.to_dict() for campaign in campaigns]

	
		for campaign in campaigns:
			campaign["start_date"] = convert_to_datetime(campaign.get("start_date"))

	
		campaigns = sorted(campaigns, key=lambda x: x["start_date"] or datetime.min)
		
		campaigns_count_over_time = {}
		for campaign in campaigns:
			date = campaign["start_date"]
			if date:
				date_str = date.strftime("%Y-%m-%d") 
				if date_str in campaigns_count_over_time:
					campaigns_count_over_time[date_str] += 1
				else:
					campaigns_count_over_time[date_str] = 1
		
		
		ad_requests = AdRequest.query.all()
		ad_requests = [ad_request.to_dict() for ad_request in ad_requests]

	
		for ad_request in ad_requests:
			ad_request["created_at"] = ad_request.get("created_at")

		
		ad_requests = sorted(ad_requests, key=lambda x: x["created_at"] or datetime.min)
		
		ad_requests_count_over_time = {}
		for ad_request in ad_requests:
			date = ad_request["created_at"]
			if date:
				date_str = date.strftime("%Y-%m-%d")  
				if date_str in ad_requests_count_over_time:
					ad_requests_count_over_time[date_str] += 1
				else:
					ad_requests_count_over_time[date_str] = 1

		
		users = User.query.all()
		users = [user.to_dict() for user in users]

		
		for user in users:
			user["create_datetime"] = user.get("create_datetime")

		
		users = sorted(users, key=lambda x: x["create_datetime"] or datetime.min)
		
		users_count_over_time = {}
		for user in users:
			date = user["create_datetime"]
			if date:
				date_str = date.strftime("%Y-%m-%d") 
				if date_str in users_count_over_time:
					users_count_over_time[date_str] += 1
				else:
					users_count_over_time[date_str] = 1
		
		return {
			"campaigns": campaigns_count_over_time,
			"ad_requests": ad_requests_count_over_time,
			"users": users_count_over_time,
		}, 200


api.add_resource(CampaignApi,"/campaign","/campaign/<int:id>",methods=["GET", "PUT", "POST", "DELETE"])
api.add_resource(InfluencerApi,"/influencer","/influencer/<int:id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(SponsorApi,"/sponsors","/sponsors/<int:id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(AdRequestApi,"/ad_request","/ad_request/<int:id>", "/ad_request/<int:camp_id>/<int:inf_id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(UserApi,"/emailcheck","/user","/user/<string:email>" "/user/<int:id>",methods=["GET", "POST", "PUT", "DELETE"],)
api.add_resource(Stats, "/stats", methods=["GET"])
api.add_resource(Insights, "/insights", methods=["GET"])
api.add_resource(UpdateCampaign, "/request_campaign/<int:id>", methods=["PUT"])
api.add_resource(Profilepage, "/profilepage", methods=["GET"])
api.add_resource(Campaign_Filter, "/campaign_filter", methods=["GET"])
api.add_resource(ForGraphs, "/for_graphs", methods=["GET"])
