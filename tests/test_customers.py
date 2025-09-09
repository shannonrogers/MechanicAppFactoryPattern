from app import create_app
from app.models import Customers, db
import unittest

class TestCustomers(unittest.TestCase):

    def setup(self):
        self.app = create_app('TestingConfig')
        self.customer = Customers(first_name="John", last_name="Diaz", email="john.diaz@email.com", phone="123-456-7890", address="123 Test street")#creating starter
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)#creating starter
            db.session.commit()

        self.client = self.app.test_client()

#important all test functions start with test
def test_create_customer(self): 
    customer_payload = {
        "first_name": "test",
        "last_name": "customer", 
        "email": "test.customer@email.com",
        "phone": "123-456-7890", 
        "address": "123 test street"
    }

    response = self.client.post('/customers', json=customer_payload)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['email'], "test.customer@email.com")
    
def test_invalid_create(self): 
    customers_payload = {
        "username": "test customer"
    }

def test_login(self): 
    login_creds={
        "email": "test"
    }
    response = self.client.post('/users/login', json=login_creds)