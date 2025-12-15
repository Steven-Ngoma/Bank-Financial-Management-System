from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    employment_years = db.Column(db.Integer, nullable=False)
    credit_score = db.Column(db.Integer, default=650)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    loans = db.relationship('Loan', backref='customer', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, default=5.5)
    status = db.Column(db.String(20), default='pending')
    risk_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)

# Risk Assessment Function
def calculate_risk_score(customer, loan):
    score = 500
    # Credit score impact
    score += (customer.credit_score - 650) * 0.5
    # Loan to income ratio
    loan_to_income = loan.amount / customer.annual_income
    if loan_to_income <= 2: score += 100
    elif loan_to_income <= 3: score += 50
    elif loan_to_income > 4: score -= 100
    # Employment stability
    if customer.employment_years >= 5: score += 50
    elif customer.employment_years >= 2: score += 25
    elif customer.employment_years < 1: score -= 50
    return max(300, min(850, int(score)))

# Create sample data
def create_sample_data():
    if Customer.query.count() == 0:
        customers_data = [
            {'name': 'John Smith', 'email': 'john@email.com', 'phone': '+1-555-0101', 'annual_income': 75000, 'employment_years': 5, 'credit_score': 720},
            {'name': 'Sarah Johnson', 'email': 'sarah@email.com', 'phone': '+1-555-0102', 'annual_income': 65000, 'employment_years': 3, 'credit_score': 680},
            {'name': 'Michael Brown', 'email': 'michael@email.com', 'phone': '+1-555-0103', 'annual_income': 95000, 'employment_years': 8, 'credit_score': 750}
        ]
        
        for data in customers_data:
            customer = Customer(**data)
            db.session.add(customer)
        
        db.session.commit()
        
        # Add sample loans
        customers = Customer.query.all()
        for i, customer in enumerate(customers):
            loan = Loan(
                customer_id=customer.id,
                amount=50000 + (i * 25000),
                purpose=['Home Purchase', 'Car Loan', 'Personal Loan'][i],
                term_months=36,
                status=['approved', 'pending', 'rejected'][i]
            )
            loan.risk_score = calculate_risk_score(customer, loan)
            db.session.add(loan)
        
        db.session.commit()

# Routes
@app.route('/')
def dashboard():
    total_customers = Customer.query.count()
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    approved_loans = Loan.query.filter_by(status='approved').count()
    recent_applications = Loan.query.order_by(Loan.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_customers=total_customers,
                         total_loans=total_loans,
                         pending_loans=pending_loans,
                         approved_loans=approved_loans,
                         recent_applications=recent_applications)

@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/loans')
def loans():
    loans = Loan.query.all()
    return render_template('loans.html', loans=loans)

@app.route('/apply')
def apply_loan():
    return render_template('apply.html')

# API Routes
@app.route('/api/customers', methods=['GET', 'POST'])
def api_customers():
    if request.method == 'POST':
        data = request.json
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            annual_income=data['annual_income'],
            employment_years=data['employment_years'],
            credit_score=data.get('credit_score', 650)
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully', 'id': customer.id})
    
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone,
        'annual_income': c.annual_income, 'employment_years': c.employment_years,
        'credit_score': c.credit_score
    } for c in customers])

@app.route('/api/loans/apply', methods=['POST'])
def api_apply_loan():
    data = request.json
    
    customer = Customer.query.filter_by(email=data['email']).first()
    if not customer:
        customer = Customer(
            name=data['name'], email=data['email'], phone=data['phone'],
            annual_income=data['annual_income'], employment_years=data['employment_years'],
            credit_score=data.get('credit_score', 650)
        )
        db.session.add(customer)
        db.session.flush()
    
    loan = Loan(
        customer_id=customer.id, amount=data['amount'], purpose=data['purpose'],
        term_months=data['term_months'], status='pending'
    )
    db.session.add(loan)
    db.session.commit()
    
    risk_score = calculate_risk_score(customer, loan)
    loan.risk_score = risk_score
    
    if risk_score >= 700:
        loan.status = 'approved'
        loan.approved_at = datetime.utcnow()
    elif risk_score < 400:
        loan.status = 'rejected'
        loan.rejected_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Loan application submitted successfully',
        'loan_id': loan.id, 'risk_score': risk_score, 'status': loan.status
    })

@app.route('/api/loans/<int:loan_id>/decision', methods=['PUT'])
def api_loan_decision(loan_id):
    data = request.json
    loan = Loan.query.get_or_404(loan_id)
    
    if data['decision'] == 'approve':
        loan.status = 'approved'
        loan.approved_at = datetime.utcnow()
    elif data['decision'] == 'reject':
        loan.status = 'rejected'
        loan.rejected_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': f'Loan {data["decision"]}d successfully'})

@app.route('/api/analytics/dashboard')
def api_dashboard_analytics():
    total_customers = Customer.query.count()
    total_loans = Loan.query.count()
    approved_loans = Loan.query.filter_by(status='approved').count()
    rejected_loans = Loan.query.filter_by(status='rejected').count()
    pending_loans = Loan.query.filter_by(status='pending').count()
    
    total_amount = db.session.query(db.func.sum(Loan.amount)).filter_by(status='approved').scalar() or 0
    
    return jsonify({
        'total_customers': total_customers, 'total_loans': total_loans,
        'approved_loans': approved_loans, 'rejected_loans': rejected_loans,
        'pending_loans': pending_loans, 'total_approved_amount': total_amount,
        'approval_rate': round((approved_loans / total_loans * 100) if total_loans > 0 else 0, 2)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5000)