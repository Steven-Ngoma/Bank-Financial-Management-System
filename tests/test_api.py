import unittest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_app import app, db

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.drop_all()
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_dashboard_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_customer_api(self):
        customer_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1-555-0123',
            'annual_income': 75000,
            'employment_years': 3,
            'credit_score': 720
        }
        response = self.app.post('/api/customers',
                               data=json.dumps(customer_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
    
    def test_loan_application_api(self):
        # First create a customer
        customer_data = {
            'name': 'Loan Applicant',
            'email': 'applicant@example.com',
            'phone': '+1-555-0124',
            'annual_income': 80000,
            'employment_years': 5,
            'credit_score': 750
        }
        
        loan_data = {
            **customer_data,
            'amount': 50000,
            'purpose': 'Home Purchase',
            'term_months': 36
        }
        
        response = self.app.post('/api/loans/apply',
                               data=json.dumps(loan_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('loan_id', data)
        self.assertIn('risk_score', data)
        self.assertIn('status', data)
    
    def test_get_customers_api(self):
        response = self.app.get('/api/customers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_dashboard_analytics_api(self):
        response = self.app.get('/api/analytics/dashboard')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_customers', data)
        self.assertIn('total_loans', data)
        self.assertIn('approval_rate', data)

if __name__ == '__main__':
    unittest.main()