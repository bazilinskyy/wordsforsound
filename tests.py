#!flask/bin/python
import unittest
import os

from config import basedir
from app import app, db
from datetime import datetime

from app.emails import send_email, send_email_flask_emails
from app.models import Asset, User, Project, ClientUser, AssetStatus


class TestCase(unittest.TestCase):

		def setUp(self):
			app.config['TESTING'] = True
			app.config['WTF_CSRF_ENABLED'] = False
			app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
			self.app = app.test_client()
			db.create_all()

		def tearDown(self):
			db.session.remove()
			db.drop_all()

		def test_email(self):
			user = ClientUser(nickname="user",
							first_name="user",
							last_name="user",
			                email="user@gmail.com",
			                password="12345678",
			                last_seen=datetime.now(),
			                receive_emails=True)

			project = Project(name="Validation 1",
							description="In this project we will create two assets to validate the newly developed sound design process.",
							filename="validation_description.pdf",
							finished=False,
							user=user,
							timestamp=datetime.now())

			asset = Asset(name="Asset 1A",
							description="Beep-like sound for an urgent take-over request in a critical situation with TTC less than or equal 5 sec (e.g. sudden serious traffic accident in the lane of the automated car). It should sound worthy, with a touch of \"wooden\" sound. The sound should be directional: it should point to the the safest maneuver (right/left). It may include speech.",
			        		status=AssetStatus.iteration.value,
			        		project=project,
			        		finished=False,
			        		iteration_number=0,
			        		timestamp=datetime.now(),
			        		notify_by_email=True)

			db.session.add(user)
			db.session.add(project)
			db.session.add(asset)
			db.session.commit()

			email="dummy_email@gmail.com"
			with app.app_context():
				assert send_email("Test email", email, "Test email. Move on.")

if __name__ == '__main__':
    unittest.main()
