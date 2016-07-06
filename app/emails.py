from flask import render_template
from flask.ext.mail import Message
from app import mail
from .decorators import async
from config_secret import ADMINS
from app import app

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def follower_notification(followed, follower):
    send_email("[microblog] %s is now following you!" % follower.nickname,
               ADMINS[0],
               [followed.email],
               render_template("follower_email.txt",
                               user=followed, follower=follower),
               render_template("follower_email.html",
                               user=followed, follower=follower))

def description_notification(user, asset):
    send_email("Description for asset " + asset.name + " is ready.",
               ADMINS[0],
               "hollgam@gmail.com",
               render_template("description_email.txt",
                               user=user, asset=asset),
               render_template("description_email.html",
                               user=user, asset=asset))

def iteration_notification(user, asset):
    send_email("Iteration for asset " + asset.name + " is ready.",
               ADMINS[0],
               "hollgam@gmail.com",
               render_template("iteration_email.txt",
                               user=user, asset=asset),
               render_template("iteration_email.html",
                               user=user, asset=asset))

def validation_notification(user, asset):
    send_email("Validation for asset " + asset.name + " is ready.",
               ADMINS[0],
               "hollgam@gmail.com",
               render_template("validation_email.txt",
                               user=user, asset=asset),
               render_template("validation_email.html",
                               user=user, asset=asset))

def test_notification(user):
    send_email("Test of email.",
               ADMINS[0],
               ["hollgam@gmail.com"],
               render_template("follower_email.txt",
                               user=user, follower=user),
               render_template("follower_email.html",
                               user=user, follower=user)) 
