from unittest import TestCase

from app import app
from models import db, User

# Use test database and setup your own here....
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:pa$$w@rd@localhost:5432/blogly"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        print("running setup...")
        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast", image_url=None)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        print("self.user.id --->", self.user_id)

    def tearDown(self):
        """Clean up any fouled transaction."""
        print("running tear down...")
        db.session.rollback()
        User.query.delete()
        db.session.commit()

    def test_list_users(self):
        with app.test_client() as client:
            print("running test_list_users...")
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirst", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/show_user/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h3>User name: TestFirst TestLast</h3>", html)
