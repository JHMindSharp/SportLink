import unittest
from flask import current_app
from flask_testing import TestCase
from app import create_app, db
from app.models import User

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/tmp/uploads'

class BasicTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully!', response.data)

        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('testpassword'))

    def test_login_user(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User logged in successfully!', response.data)
        self.assertIn(b'access_token', response.data)

    def test_search_users(self):
        user1 = User(username='testuser1')
        user1.set_password('testpassword1')
        db.session.add(user1)

        user2 = User(username='testuser2')
        user2.set_password('testpassword2')
        db.session.add(user2)
        
        db.session.commit()

        response = self.client.get('/search_users', query_string={'query': 'testuser'})
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['username'], 'testuser1')
        self.assertEqual(data[1]['username'], 'testuser2')

if __name__ == '__main__':
    unittest.main()
