from celery import shared_task
from .model import Campaign, AdRequest, Influencer, User
import flask_excel as excel
from .mail_service import send_message
from jinja2 import Template
import os

@shared_task(ignore_result=False)
def generate_campaign_csv():
    camp = Campaign.query.with_entities(
        Campaign.description, Campaign.campaign_id, Campaign.name, Campaign.budget, Campaign.start_date,Campaign.category, Campaign.niche ).all()
    csv_output = excel.make_response_from_query_sets(camp, ["campaign_id", "name","description", "budget","category", "niche" ],"csv")
    filename="campaign.csv"
    with open(filename, "wb") as f:
        f.write(csv_output.data)
    return filename

@shared_task(ignore_result=False)
def send_email(to, subject):
    # Fetching cintent for email from MOdels
    #  Activity Report( Campaign Details, Ads done, Growth? Budgets Used & remaining)

    campaigns = Campaign.query.all()
    file_path = os.path.join("backend", "monthly_report.html")

    for campaign in campaigns:
        with open(file_path, "r") as f:
            template = Template(f.read())

    formatted_result = [{
        "campaign_id": item.campaign_id,
        "name": item.name,
        "budget": item.budget

    } for item in campaigns]

    send_message(to, subject, template.render(campaigns=formatted_result))
    return "Email sent"


@shared_task(ignore_result=False)
def daily_reminder(subject):
    # peding AD Requests

    ad_requests = AdRequest.query.filter_by(status="Pending").all()
    pending_influencer = []

    for ads in ad_requests:
        pending_influencer.append(ads.influencer_id)
    
    unque_influencer = set(pending_influencer)

    for ui in unque_influencer:
        count = pending_influencer.count(ui)
        user = Influencer.query.get(ui)
        email= User.query.filter_by(id=user.user_id).first().email
        send_message(email, subject, f"You have {count} pending requests")
    return "Email sent"
