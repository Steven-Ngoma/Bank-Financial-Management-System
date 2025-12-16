import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_app import app, db, Customer, Loan, calculate_risk_score

class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
    
    def test_high_credit_score_low_risk(self):
        """Test that high credit score results in lower risk"""
        with app.app_context():
            customer = Customer(
                name="High Credit Customer",
                email="high@test.com",
                phone="123-456-7890",
                annual_income=100000,
                employment_years=5,
                credit_score=780
            )
            loan = Loan(amount=50000, purpose="Home Purchase", term_months=36)
            
            risk_score = calculate_risk_score(customer, loan)
            self.assertGreaterEqual(risk_score, 650, "High credit score should result in good risk score")
    
    def test_low_credit_score_high_risk(self):
        """Test that low credit score results in higher risk"""
        with app.app_context():
            customer = Customer(
                name="Low Credit Customer",
                email="low@test.com",
                phone="123-456-7891",
                annual_income=40000,
                employment_years=1,
                credit_score=500
            )
            loan = Loan(amount=80000, purpose="Personal Loan", term_months=60)
            
            risk_score = calculate_risk_score(customer, loan)
            self.assertLessEqual(risk_score, 500, "Low credit score should result in poor risk score")
    
    def test_employment_stability_impact(self):
        """Test that employment years affect risk score"""
        with app.app_context():
            # Stable employment
            stable_customer = Customer(
                name="Stable Employee",
                email="stable@test.com",
                phone="123-456-7892",
                annual_income=70000,
                employment_years=8,
                credit_score=700
            )
            
            # New employment
            new_customer = Customer(
                name="New Employee",
                email="new@test.com",
                phone="123-456-7893",
                annual_income=70000,
                employment_years=0,
                credit_score=700
            )
            
            loan = Loan(amount=40000, purpose="Car Loan", term_months=48)
            
            stable_score = calculate_risk_score(stable_customer, loan)
            new_score = calculate_risk_score(new_customer, loan)
            
            self.assertGreater(stable_score, new_score, 
                             "Stable employment should result in better risk score")
    
    def test_loan_to_income_ratio_impact(self):
        """Test that loan-to-income ratio affects risk assessment"""
        with app.app_context():
            customer = Customer(
                name="Test Customer",
                email="ratio@test.com",
                phone="123-456-7894",
                annual_income=60000,
                employment_years=3,
                credit_score=680
            )
            
            # Small loan (good ratio)
            small_loan = Loan(amount=30000, purpose="Car Loan", term_months=36)
            # Large loan (poor ratio)
            large_loan = Loan(amount=300000, purpose="Business Loan", term_months=60)
            
            small_score = calculate_risk_score(customer, small_loan)
            large_score = calculate_risk_score(customer, large_loan)
            
            self.assertGreater(small_score, large_score,
                             "Smaller loan-to-income ratio should result in better risk score")
    
    def test_risk_score_bounds(self):
        """Test that risk scores are within expected bounds"""
        with app.app_context():
            customer = Customer(
                name="Boundary Test",
                email="bounds@test.com",
                phone="123-456-7895",
                annual_income=50000,
                employment_years=2,
                credit_score=650
            )
            loan = Loan(amount=25000, purpose="Personal Loan", term_months=24)
            
            risk_score = calculate_risk_score(customer, loan)
            
            self.assertGreaterEqual(risk_score, 300, "Risk score should not be below 300")
            self.assertLessEqual(risk_score, 850, "Risk score should not exceed 850")

if __name__ == '__main__':
    unittest.main()