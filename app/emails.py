from flask import render_template
from flask.ext.mail import Message
from app import mail
import os
from .decorators import async
if not os.environ.get('HEROKU'): 
  from config_secret import GMAIL_USERNAME, GMAIL_PASSWORD
else:
  GMAIL_USERNAME=os.environ.get('GMAIL_USERNAME')
  GMAIL_PASSWORD=os.environ.get('GMAIL_PASSWORD')
from app import app
import yagmail
from models import ClientUser, SupplierUser, AssetStatus

# @async
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


def send_email(subject, recipient, body):
    # msg = Message(subject, sender=sender, recipients=recipients)
    # msg.body = text_body
    # msg.html = html_body
    # send_async_email(app, msg)
    try:
      yag = yagmail.SMTP(GMAIL_USERNAME, GMAIL_PASSWORD)
      yag.send(str(recipient), subject, body)
    except:
      pass

def description_notification(user, asset):
  if user.receive_emails and asset.notify_by_email:
    if user.type == "client_user":
      user_type = "client"
    elif user.type == "supplier_user":
      user_type = "supplier"
    else:
      user_type = "N/A"
    print GMAIL_USERNAME + " " + GMAIL_PASSWORD
    send_email("Description for asset " + asset.name + " is ready.",
               user.email,
               str(render_template("description_email.html",
                               user=user,
                               asset=asset,
                               user_type=user_type)))

def iteration_notification(user, asset):
  if user.receive_emails and asset.notify_by_email:
    if user.type == "client_user":
      user_type = "client"
    elif user.type == "supplier_user":
      user_type = "supplier"
    else:
      user_type = "N/A"
    send_email("Iteration for asset " + asset.name + " is ready.",
               user.email,
               str(render_template("iteration_email.html",
                               user=user,
                               asset=asset,
                               user_type=user_type)))

def verification_notification(user, asset):
  if user.receive_emails and asset.notify_by_email:
    if user.type == "client_user" and asset.status == AssetStatus.verification:
      user_type = "client"
      send_email("Verificartion for asset " + asset.name + " is ready.",
               user.email,
               str(render_template("verification_email.html",
                               user=user,
                               asset=asset,
                               user_type=user_type)))