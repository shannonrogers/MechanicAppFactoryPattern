from app import create_app
from app.models import Mechanics, db
import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token

class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanics(first_name="John", last_name="Diaz", email="john.diaz@email.com", password=generate_password_hash('123'), salary='70000', address="123 Test street")#creating starter
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)#creating starter
            db.session.commit()
        self.token = encode_token(1, 'mechanic')
        self.client = self.app.test_client()

    #important all test functions start with test
    def test_create_mechanic(self): 
        mechanic_payload = {
            "first_name": "test",
            "last_name": "mechanic", 
            "email": "test.mechanic@email.com",
            "password": "123",
            "salary": "60000",
            "address": "123 test street"
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], "test.mechanic@email.com")
        self.assertTrue(check_password_hash(response.json['password'], "123"))
      
        
    def test_invalid_create(self): 
        mechanic_payload = {
            "first_name": "test",
            "last_name": "mechanic", 
            "address": "123 test street"
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)
        
    def test_get_users(self): 
        response = self.client.get('/mechanics')
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["first_name"], "John")
    
    def test_login(self): 
        login_creds = {
            "email": "john.diaz@email.com", 
            "password": "123"
        }

        response = self.client.post('/mechanics/login', json=login_creds)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
    
    def test_delete(self): 
        headers = {'Authorization': 'Bearer ' + self.token}

        response = self.client.delete('/mechanics', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_unauthorized_delete(self): 
        
        response = self.client.delete('/mechanics')
        self.assertEqual(response.status_code, 401)
    
    def test_update(self): 
        mechanic_id = 1
        headers = {'Authorization': 'Bearer ' + self.token}

        update_payload = {
            "first_name": "test",
            "last_name": "mechanic", 
            "email": "new.test.mechanic@email.com",
            "password": "123",
            "salary": "60000",
            "address": "123 test street"
        }

        response = self.client.put(f'/mechanics/{mechanic_id}', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "new.test.mechanic@email.com")

    def test_get_specific_mechanic(self):
        mechanic_id = 1

        response = self.client.get(f'/mechanics/{mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "john.diaz@email.com")

    def test_get_nonexistent_mechanic(self):
    
        response = self.client.get('/mechanics/9999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Mechanic not found.")

