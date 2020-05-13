from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:p@ssw0rd@localhost:5432/blogly"
app.config["SQLALCHEMY_ECHO"] = False
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""
        print("running setup...")
        User.query.delete()
        db.session.commit()
        db.session.rollback()
        user = User(first_name="TestFirst", last_name="TestLast", image_url=None)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        print("self.user.id --->", self.user_id)

    def tearDown(self):
        """Clean up any fouled transaction."""
        print("running teardown...")
        User.query.delete()
        db.session.commit()
        db.session.rollback()

    def test_create_user(self):
        """Test add user, and Default value added to image_url"""
        print("running test_create_user...")
        user = User.query.get(self.user_id)
        print("loggin user ---> ", user)
        self.assertEqual(user.first_name, "TestFirst")
        self.assertEqual(user.last_name, "TestLast")
        self.assertEqual(user.image_url, "../static/images/placeholder.jpg")

    def test_full_name(self):
        """Test get full name function"""
        print("running test_full_name...")
        self.assertEqual(User.full_name(self.user_id), "TestFirst TestLast")
