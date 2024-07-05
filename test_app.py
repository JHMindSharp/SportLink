import unittest
from flask import current_app
from flask_testing import TestCase
from app import create_app, db
from app.models import User


class TestConfig:
    """Specific configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/tmp/uploads'


class BasicTestCase(TestCase):
    """Basic test case using Flask-Testing."""

    def create_app(self):
        """Create an instance of the Flask application for testing."""
        app = create_app()
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        """Set up the test environment before each test."""
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up the test environment after each test."""
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        """Test user registration."""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.email, 'testuser@example.com')

    def test_login_user(self):
        """Test user login."""
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', json={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    def test_search_users(self):
        """Test user search functionality."""
        user1 = User(username='testuser1', email='testuser1@example.com')
        user1.set_password('testpassword1')
        db.session.add(user1)

        user2 = User(username='testuser2', email='testuser2@example.com')
        user2.set_password('testpassword2')
        db.session.add(user2)

        db.session.commit()

        response = self.client.get(
            '/search_users',
            query_string={
                'query': 'testuser'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['username'], 'testuser1')
        self.assertEqual(data[1]['username'], 'testuser2')

    def test_delete_user(self):
        """Test user deletion."""
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # Simulate login to get a JWT token
        response = self.client.post('/login', json={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        token = response.json['access_token']

        # Use the token to delete the user
        response = self.client.delete('/delete_user', headers={
            'Authorization': f'Bearer {token}'
        }, data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully', response.data)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()
