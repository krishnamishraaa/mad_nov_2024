from flask_restful import Resource , fields , marshal_with , reqparse , Api, request
from .model import *
from flask import jsonify
from sqlalchemy import desc
from datetime import datetime

api= Api(prefix='/api')

output_fields_campaign = {
	"campaign_id" : fields.Integer,
	"sponsor_id" : fields.Integer,
	"name" : fields.String,
	"description" : fields.String,
	"budget" : fields.String,
	"start_date" : fields.String,
	"end_date" : fields.String,
	"visibility": fields.String,
	"goals": fields.String,
}

# Campaign API resource
class CampaignApi(Resource):
	
	@marshal_with(output_fields_campaign)
	
	
	def get(self):
		# Retrieve the campaign by its ID
		campaign = Campaign.query.all()
		if campaign:
			return campaign, 200
		return {"message": "Campaign not found"}, 404
	
	
	
	def post(self):
		# Define request parser for campaign input
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Campaign name is required")
		parser.add_argument('description', type=str, required=True, help="Campaign description is required")
		parser.add_argument('start_date', type=str, required=False, default=str(datetime.now()), help="Start date (optional)")
		parser.add_argument('end_date', type=str, required=False, default=str(datetime.now()), help="End date (optional)")
		parser.add_argument('budget', type=float, required=False, help="Budget (optional)")
		parser.add_argument('visibility', type=str, required=False, help="Visibility (optional)")
		parser.add_argument('goals', type=str, required=False, help="Campaign goals (optional)")
		args = parser.parse_args()
		print(args)

		# Create a new campaign using parsed arguments
		new_campaign = Campaign(
			name=args['name'],
			description=args['description'],
			start_date=args['start_date'],
			end_date=args['end_date'],
			budget=args['budget'],
			visibility=args['visibility'],
			goals=args['goals']

		)
		db.session.add(new_campaign)
		db.session.commit()

		return {'message': 'Campaign created successfully'}, 201
	
	# PUT method to update the campaign details
	@marshal_with(output_fields_campaign)
	def put(self, id):
		campaign = Campaign.query.get(id)
		if not campaign:
			return {"message": "Campaign not found"}, 404

		# Define request parser for campaign input
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=False)
		parser.add_argument('description', type=str, required=False)
		parser.add_argument('start_date', type=str, required=False)
		parser.add_argument('end_date', type=str, required=False)
		parser.add_argument('budget', type=float, required=False)
		parser.add_argument('visibility', type=str, required=False, choices=['public', 'private'])
		parser.add_argument('goals', type=str, required=False)
		
		args = parser.parse_args()

		# Only update provided fields
		if args['name']:
			campaign.name = args['name']
		if args['description']:
			campaign.description = args['description']
		if args['start_date']:
			campaign.start_date = args['start_date']
		if args['end_date']:
			campaign.end_date = args['end_date']
		if args['budget'] is not None:
			campaign.budget = args['budget']
		if args['visibility']:
			campaign.visibility = args['visibility']
		if args['goals']:
			campaign.goals = args['goals']

		db.session.commit()

		return {'message': 'Campaign updated successfully'}, 200


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
	def get(self, id):
		# Retrieve influencer by their ID
		influencer = Influencer.query.get(id)
		if influencer:
			return influencer, 200
		return {"message": "Influencer not found"}, 404
	
	def post(self):
		# Define request parser for influencer input
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Influencer name is required")
		parser.add_argument('category', type=str, required=True, help="Category is required")
		parser.add_argument('niche', type=str, required=True, help="Niche is required")
		parser.add_argument('reach', type=int, required=True, help="Reach is required")

		args = parser.parse_args()

		# Create a new influencer with parsed data
		new_influencer = Influencer(
			name=args['name'],
			category=args['category'],
			niche=args['niche'],
			reach=args['reach']
		)
		db.session.add(new_influencer)
		db.session.commit()

		return {'message': 'Influencer created successfully'}, 201
	
# Output fields for marshalling sponsor data
output_fields_sponsor = {
	"sponsor_id": fields.Integer,
	"name": fields.String,
	"industry": fields.String,
	"budget": fields.Float,
}

class SponsorApi(Resource):
	@marshal_with(output_fields_sponsor)
	def get(self, id):
		# Retrieve sponsor by their ID
		sponsor = Sponsor.query.get(id)
		if sponsor:
			return sponsor, 200
		return {"message": "Sponsor not found"}, 404
	
	def post(self):
		# Define request parser for sponsor input
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Sponsor name is required")
		parser.add_argument('industry', type=str, required=True, help="Industry is required")
		parser.add_argument('budget', type=float, required=True, help="Budget is required")

		args = parser.parse_args()

		# Create a new sponsor with parsed data
		new_sponsor = Sponsor(
			name=args['name'],
			industry=args['industry'],
			budget=args['budget']
		)
		db.session.add(new_sponsor)
		db.session.commit()

		return {'message': 'Sponsor created successfully'}, 201

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
	def get(self, id):
		# Retrieve ad request by its ID
		ad_request = AdRequest.query.get(id)
		if ad_request:
			return ad_request, 200
		return {"message": "Ad Request not found"}, 404
	
	def post(self):
		# Define request parser for ad request input
		parser = reqparse.RequestParser()
		parser.add_argument('campaign_id', type=int, required=True, help="Campaign ID is required")
		parser.add_argument('influencer_id', type=int, required=True, help="Influencer ID is required")
		parser.add_argument('messages', type=str, required=True, help="Messages are required")
		parser.add_argument('requirements', type=str, required=True, help="Requirements are required")
		parser.add_argument('payment_amount', type=float, required=True, help="Payment amount is required")
		parser.add_argument('status', type=str, required=True, choices=['Pending', 'Accepted', 'Rejected'], help="Status is required")

		args = parser.parse_args()

		# Create a new ad request with parsed data
		new_ad_request = AdRequest(
			campaign_id=args['campaign_id'],
			influencer_id=args['influencer_id'],
			messages=args['messages'],
			requirements=args['requirements'],
			payment_amount=args['payment_amount'],
			status=args['status']
		)
		db.session.add(new_ad_request)
		db.session.commit()

		return {'message': 'Ad Request created successfully'}, 201

api.add_resource(CampaignApi, '/campaign', '/campaign/<int:id>', methods=['GET', 'PUT', 'POST', 'DELETE'])	
api.add_resource(InfluencerApi, '/influencer', '/influencer/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(SponsorApi, '/sponsor', '/sponsor/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(AdRequestApi, '/ad_request', '/ad_request/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])

