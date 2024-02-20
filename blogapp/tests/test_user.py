import unittest
import json
from blogapp import app, db  
from blogapp.models import User
import base64

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # new temporary test environment
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/cloud'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        with app.app_context():
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        # remove the temp environment once test is done
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_and_get_user(self):
        # Create a new user
        response = self.app.post('/v1/user', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'username': 'john.doe@example.com'
        })

        self.assertEqual(response.status_code, 201)

        # Get the created user
        username = 'john.doe@example.com'
        password = 'password123'
        credentials = f'{username}:{password}'
        base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        response = self.app.get('/v1/user/self', headers={'Authorization': 'Basic ' + base64_credentials})

        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.data.decode('utf-8'))

        # Validate user details
        self.assertEqual(user_data['first_name'], 'John')
        self.assertEqual(user_data['last_name'], 'Doe')
        # Add more validations as needed

    def test_update_and_get_user(self):
        # Create a new user
        response = self.app.post('/v1/user', json={
            'first_name': 'Alice',
            'last_name': 'Smith',
            'password': 'password456',
            'username': 'alice.smith@example.com'
        })

        self.assertEqual(response.status_code, 201)

        # Get the created user
        username = 'alice.smith@example.com'
        password = 'password456'
        credentials = f'{username}:{password}'
        base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        response = self.app.get('/v1/user/self', headers={'Authorization': 'Basic ' + base64_credentials})

        self.assertEqual(response.status_code, 200)
        user_data_before_update = json.loads(response.data.decode('utf-8'))

        # Update the user
        response = self.app.put('/v1/user/self', json={
            'first_name': 'Alice H',
            'last_name': 'Smithsonian'
        }, headers={'Authorization': 'Basic ' + base64_credentials})

        self.assertEqual(response.status_code, 204)

        # Get the updated user
        response = self.app.get('/v1/user/self', headers={'Authorization': 'Basic ' + base64_credentials})

        self.assertEqual(response.status_code, 200)
        user_data_after_update = json.loads(response.data.decode('utf-8'))

        # Validate user details after the update
        self.assertEqual(user_data_after_update['first_name'], 'Alice H')
        self.assertEqual(user_data_after_update['last_name'], 'Smithsonian')
        # Add more validations as needed

if __name__ == '__main__':
    unittest.main()
